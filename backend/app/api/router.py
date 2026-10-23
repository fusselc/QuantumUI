from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Header, HTTPException, Request, Response, status, Query
from fastapi.responses import JSONResponse

from app.models.schemas import (
    Template,
    ExperimentRecord,
    CreateExperimentRequest,
    GenerateRequest,
    ValidateCodeRequest,
    ExecuteExperimentRequest,
    UpdateSharingRequest,
    ExecutionStatus,
    ProblemDetails
)
from app.services.templates import list_templates, get_template
from app.services.generation import get_model_adapter, SafetyPolicyException
from app.services.validation import validate_code
from app.services.execution import ExecutionService
from app.services.explanation import ExplanationService
from app.services.store import ExperimentStore
from app.services.export import ExportService

router = APIRouter(prefix="/v1")
store = ExperimentStore()


# RFC 9457 Problem Details Exception Helper
def make_problem_exception(status_code: int, title: str, detail: str, problem_type: str = "about:blank"):
    return HTTPException(
        status_code=status_code,
        detail={
            "type": problem_type,
            "title": title,
            "status": status_code,
            "detail": detail
        }
    )


@router.get("/templates", response_model=List[Template])
def get_all_templates(response: Response):
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = "99"
    return list_templates()


@router.get("/templates/{template_id}", response_model=Template)
def get_single_template(template_id: str):
    t = get_template(template_id)
    if not t:
        raise make_problem_exception(
            status_code=404,
            title="Template Not Found",
            detail=f"Template '{template_id}' was not found in the catalog."
        )
    return t


@router.post("/experiments", response_model=ExperimentRecord, status_code=status.HTTP_201_CREATED)
def create_experiment(req: CreateExperimentRequest):
    adapter = get_model_adapter("offline_generator")
    
    # 1. If created from template
    if req.template_id:
        t = get_template(req.template_id)
        if not t:
            raise make_problem_exception(
                status_code=404,
                title="Template Not Found",
                detail=f"Template '{req.template_id}' not found."
            )
        prompt = req.prompt_text or t.prompt_text
        code = t.qiskit_code
        desc = t.circuit_description
        expl = t.explanation_by_level
    elif req.prompt_text:
        prompt = req.prompt_text
        try:
            code, desc, expl = adapter.generate_code(prompt)
        except SafetyPolicyException as e:
            raise make_problem_exception(
                status_code=400,
                title="Safety Policy Rejection",
                detail=str(e),
                problem_type="https://quantumui.org/errors/safety-policy-violation"
            )
    else:
        raise make_problem_exception(
            status_code=400,
            title="Invalid Request",
            detail="Either prompt_text or template_id must be provided."
        )

    val_report = validate_code(code)

    record = ExperimentRecord(
        experiment_id=uuid4(),
        prompt_text=prompt,
        template_id=req.template_id,
        generated_code=code,
        circuit_description=desc,
        validation_report=val_report,
        explanation_by_level=expl,
        code_version_history=[{
            "version": 1,
            "code": code,
            "author": "ai",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]
    )
    store.save(record)
    return record


@router.get("/experiments", response_model=List[ExperimentRecord])
def list_experiments(limit: int = Query(default=50, ge=1, le=100)):
    return store.list_all(limit=limit)


@router.get("/experiments/{experiment_id}", response_model=ExperimentRecord)
def get_experiment(experiment_id: UUID):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(
            status_code=404,
            title="Experiment Not Found",
            detail=f"No experiment record found with ID {experiment_id}"
        )
    return record


@router.post("/experiments/{experiment_id}/generate", response_model=ExperimentRecord)
def regenerate_code(experiment_id: UUID, req: Optional[GenerateRequest] = None):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(404, "Experiment Not Found", f"Experiment {experiment_id} not found.")

    prompt = (req and req.prompt_text) or record.prompt_text
    adapter_name = (req and req.model_adapter) or "offline_generator"
    adapter = get_model_adapter(adapter_name)

    try:
        code, desc, expl = adapter.generate_code(prompt)
    except SafetyPolicyException as e:
        raise make_problem_exception(400, "Safety Policy Rejection", str(e))

    val_report = validate_code(code)

    record.generated_code = code
    record.user_edited_code = None
    record.circuit_description = desc
    record.validation_report = val_report
    record.explanation_by_level = expl
    record.updated_at = datetime.now(timezone.utc)
    record.code_version_history.append({
        "version": len(record.code_version_history) + 1,
        "code": code,
        "author": "ai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    store.save(record)
    return record


@router.post("/experiments/{experiment_id}/validate", response_model=ExperimentRecord)
def validate_user_code(experiment_id: UUID, req: ValidateCodeRequest):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(404, "Experiment Not Found", f"Experiment {experiment_id} not found.")

    report = validate_code(req.code)
    record.user_edited_code = req.code
    record.validation_report = report
    record.updated_at = datetime.now(timezone.utc)
    record.code_version_history.append({
        "version": len(record.code_version_history) + 1,
        "code": req.code,
        "author": "user",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    store.save(record)
    return record


@router.post("/experiments/{experiment_id}/execute", response_model=ExperimentRecord)
def execute_experiment(
    experiment_id: UUID,
    req: Optional[ExecuteExperimentRequest] = None,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(404, "Experiment Not Found", f"Experiment {experiment_id} not found.")

    if req and req.execution_config:
        record.execution_config = req.execution_config

    code_to_run = record.user_edited_code or record.generated_code
    is_hardware = record.execution_config.backend_id != "aer_simulator"

    # Hardware validation
    if is_hardware:
        if not req or not req.hardware_confirmation_token:
            raise make_problem_exception(
                status_code=400,
                title="Hardware Confirmation Required",
                detail="Physical quantum hardware execution requires explicit user confirmation and token."
            )
        if not idempotency_key:
            raise make_problem_exception(
                status_code=400,
                title="Missing Idempotency-Key",
                detail="Hardware execution requests require an 'Idempotency-Key' header to prevent accidental duplicate submissions."
            )

    result = ExecutionService.execute(
        code_str=code_to_run,
        config=record.execution_config,
        hardware_confirmed=is_hardware,
        confirmation_token=req.hardware_confirmation_token if req else None
    )

    record.execution_result = result
    record.updated_at = datetime.now(timezone.utc)

    if result.status == ExecutionStatus.COMPLETE:
        record.explanation_by_level = ExplanationService.generate_explanation(
            prompt=record.prompt_text,
            circuit_code=code_to_run,
            result=result,
            backend_id=record.execution_config.backend_id
        )

    store.save(record)
    return record


@router.post("/experiments/{experiment_id}/sharing", response_model=ExperimentRecord)
def update_sharing_consent(experiment_id: UUID, req: UpdateSharingRequest):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(404, "Experiment Not Found", f"Experiment {experiment_id} not found.")

    now_iso = datetime.now(timezone.utc).isoformat()
    if req.repository is not None:
        record.sharing_state.repository = req.repository
        if req.repository:
            record.sharing_state.consent_timestamps["repository"] = now_iso
    if req.dataset is not None:
        record.sharing_state.dataset = req.dataset
        if req.dataset:
            record.sharing_state.consent_timestamps["dataset"] = now_iso
    if req.social is not None:
        record.sharing_state.social = req.social
        if req.social:
            record.sharing_state.consent_timestamps["social"] = now_iso
    if req.research_package is not None:
        record.sharing_state.research_package = req.research_package
        if req.research_package:
            record.sharing_state.consent_timestamps["research_package"] = now_iso

    record.updated_at = datetime.now(timezone.utc)
    store.save(record)
    return record


@router.get("/experiments/{experiment_id}/export/notebook")
def export_notebook(experiment_id: UUID):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(404, "Experiment Not Found", f"Experiment {experiment_id} not found.")

    notebook_data = ExportService.to_jupyter_notebook(record)
    return JSONResponse(
        content=notebook_data,
        headers={"Content-Disposition": f"attachment; filename=quantumui_exp_{experiment_id}.ipynb"}
    )


@router.get("/experiments/{experiment_id}/export/colab")
def export_colab_link(experiment_id: UUID):
    record = store.get(experiment_id)
    if not record:
        raise make_problem_exception(404, "Experiment Not Found", f"Experiment {experiment_id} not found.")

    colab_url = ExportService.get_google_colab_url(record)
    return {"experiment_id": str(experiment_id), "colab_url": colab_url}


@router.get("/providers")
def list_providers():
    return [
        {
            "id": "aer_simulator",
            "name": "Qiskit Aer Simulator (Local)",
            "type": "simulator",
            "status": "online",
            "description": "Instant, noise-free local quantum simulator. Default execution target.",
            "requires_confirmation": False
        },
        {
            "id": "ibm_sherbrooke",
            "name": "IBM Sherbrooke (Eagle r3 - 127 Qubits)",
            "type": "hardware",
            "status": "available",
            "description": "Physical superconducting quantum processor. Real environmental noise.",
            "requires_confirmation": True
        },
        {
            "id": "ibm_brisbane",
            "name": "IBM Brisbane (Eagle r3 - 127 Qubits)",
            "type": "hardware",
            "status": "available",
            "description": "Physical superconducting quantum processor. Cloud queue applies.",
            "requires_confirmation": True
        }
    ]
