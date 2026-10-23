import re
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# Pydantic v1 / v2 compatibility helper
class CompatBaseModel(BaseModel):
    def dump_json(self, indent: Optional[int] = None) -> str:
        if hasattr(self, "model_dump_json"):
            return self.model_dump_json(indent=indent)
        return self.json(indent=indent)

    def dump_dict(self) -> Dict[str, Any]:
        if hasattr(self, "model_dump"):
            return self.model_dump()
        return self.dict()

    @classmethod
    def load_dict(cls, data: Dict[str, Any]):
        if hasattr(cls, "model_validate"):
            return cls.model_validate(data)
        return cls.parse_obj(data)

    class Config:
        extra = "ignore"
        use_enum_values = True


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class PrimitiveType(str, Enum):
    SAMPLER = "Sampler"
    ESTIMATOR = "Estimator"


class ExecutionStatus(str, Enum):
    DRAFT = "Draft"
    VALIDATING = "Validating"
    READY = "Ready"
    RUNNING_SIMULATOR = "Running (Simulator)"
    RUNNING_HARDWARE = "Running (Hardware)"
    COMPLETE = "Complete"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class ExplanationByLevel(CompatBaseModel):
    beginner: str = Field(..., description="Intuitive, jargon-free explanation for beginners.")
    intermediate: str = Field(..., description="Statevector, amplitude, and wave-function explanation.")
    technical: str = Field(..., description="Formal quantum mechanics notation, operators, and density matrices.")


class Template(CompatBaseModel):
    template_id: str = Field(..., description="Unique slug for the template.")
    name: str = Field(..., description="Human-readable title.")
    description: str = Field(..., description="Short single-sentence overview.")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    category: str = Field(..., description="Foundations, Protocols, or Applications.")
    prompt_text: str = Field(..., description="Natural language starter prompt.")
    suggestion_chips: List[str] = Field(default_factory=list)
    qiskit_code: str = Field(..., description="Verified Qiskit circuit code.")
    circuit_description: str = Field(..., description="Text-alternative operational breakdown.")
    explanation_by_level: ExplanationByLevel


class ValidationReport(CompatBaseModel):
    is_valid: bool = Field(..., description="True if code passes syntax, AST import, and safety policy checks.")
    syntax_passed: bool = Field(..., description="Syntax valid Python.")
    imports_passed: bool = Field(..., description="No unauthorized modules imported.")
    safety_passed: bool = Field(..., description="No cryptographic attacks or blocked patterns detected.")
    circuit_valid: bool = Field(..., description="Valid Qiskit circuit construction.")
    errors: List[str] = Field(default_factory=list)
    unauthorized_imports: List[str] = Field(default_factory=list)
    blocked_keywords: List[str] = Field(default_factory=list)


class TranspilerSettings(CompatBaseModel):
    optimization_level: int = Field(default=1, ge=0, le=3)
    coupling_map: Optional[List[List[int]]] = None
    basis_gates: Optional[List[str]] = None


class ExecutionConfig(CompatBaseModel):
    primitive_type: PrimitiveType = Field(default=PrimitiveType.SAMPLER)
    backend_id: str = Field(default="aer_simulator", description="Target backend identifier.")
    shots: int = Field(default=1024, ge=1, le=100000)
    mode: str = Field(default="job", description="job, session, or batch")
    transpiler_settings: TranspilerSettings = Field(default_factory=TranspilerSettings)


class ExecutionResult(CompatBaseModel):
    raw_result: Optional[Dict[str, int]] = Field(default=None, description="Measurement outcome counts (e.g. {'00': 512, '11': 512}).")
    backend_metadata: Dict[str, Any] = Field(default_factory=dict)
    status: ExecutionStatus = Field(default=ExecutionStatus.DRAFT)
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None
    timestamps: Dict[str, str] = Field(default_factory=dict)


class SharingState(CompatBaseModel):
    private: bool = Field(default=True, description="Private by default.")
    repository: bool = Field(default=False)
    dataset: bool = Field(default=False)
    social: bool = Field(default=False)
    research_package: bool = Field(default=False)
    consent_timestamps: Dict[str, str] = Field(default_factory=dict)


class Provenance(CompatBaseModel):
    qiskit_version: str = Field(default="1.2.0")
    qiskit_aer_version: str = Field(default="0.15.0")
    adapter_used: str = Field(default="offline_generator")
    schema_version: str = Field(default="1.0.0")
    hardware_confirmed: bool = Field(default=False)


class ExperimentRecord(CompatBaseModel):
    experiment_id: UUID = Field(default_factory=uuid4)
    owner_id: str = Field(default="anonymous_local")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prompt_text: str = Field(..., description="User's natural-language prompt.")
    template_id: Optional[str] = None
    generated_code: str = Field(..., description="Qiskit circuit code generated by AI.")
    user_edited_code: Optional[str] = None
    code_version_history: List[Dict[str, Any]] = Field(default_factory=list)
    circuit_description: Optional[str] = None
    validation_report: Optional[ValidationReport] = None
    execution_config: ExecutionConfig = Field(default_factory=ExecutionConfig)
    execution_result: ExecutionResult = Field(default_factory=ExecutionResult)
    explanation_by_level: Optional[ExplanationByLevel] = None
    sharing_state: SharingState = Field(default_factory=SharingState)
    provenance: Provenance = Field(default_factory=Provenance)


# Request & Response API DTOs
class CreateExperimentRequest(CompatBaseModel):
    prompt_text: Optional[str] = None
    template_id: Optional[str] = None


class GenerateRequest(CompatBaseModel):
    prompt_text: Optional[str] = None
    model_adapter: Optional[str] = None


class ValidateCodeRequest(CompatBaseModel):
    code: str = Field(..., description="Python Qiskit code to validate.")


class ExecuteExperimentRequest(CompatBaseModel):
    execution_config: Optional[ExecutionConfig] = None
    hardware_confirmation_token: Optional[str] = None


class UpdateSharingRequest(CompatBaseModel):
    repository: Optional[bool] = None
    dataset: Optional[bool] = None
    social: Optional[bool] = None
    research_package: Optional[bool] = None


class ProblemDetails(CompatBaseModel):
    type: str = Field(default="about:blank")
    title: str
    status: int
    detail: str
    instance: Optional[str] = None
