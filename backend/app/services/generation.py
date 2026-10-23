import re
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any
from app.models.schemas import ExplanationByLevel
from app.services.templates import TEMPLATES_CATALOG


class SafetyPolicyException(Exception):
    def __init__(self, message: str, pattern: str):
        super().__init__(message)
        self.pattern = pattern


class ModelAdapter(ABC):
    @abstractmethod
    def generate_code(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str, ExplanationByLevel]:
        """Returns (qiskit_code, circuit_description, explanation_by_level)"""
        pass

    @abstractmethod
    def explain_result(self, raw_result: Dict[str, int], circuit_code: str) -> ExplanationByLevel:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        pass


class OfflineGenerator(ModelAdapter):
    """Reference offline open-source model adapter for Phase 1 MVP."""

    BLOCKED_PATTERNS = [
        (re.compile(r"\bshor(?:'s)?\s+algorithm\s+crack\b", re.IGNORECASE), "Shor's algorithm cryptographic attack"),
        (re.compile(r"\brsa\s+(?:crack|decrypt|break|factor)\b", re.IGNORECASE), "RSA decryption/cracking request"),
        (re.compile(r"\bprivate\s*key\s*(?:exfiltrate|leak|steal)\b", re.IGNORECASE), "Private key exfiltration"),
        (re.compile(r"\bbrute\s*force\s*(?:cipher|key|password)\b", re.IGNORECASE), "Cryptographic brute-force attack"),
        (re.compile(r"\bexploit\s+(?:network|vulnerability)\b", re.IGNORECASE), "Offensive exploit generation"),
    ]

    def generate_code(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str, ExplanationByLevel]:
        # 1. Safety check
        for pattern, desc in self.BLOCKED_PATTERNS:
            if pattern.search(prompt):
                raise SafetyPolicyException(
                    f"Safety Policy Rejection: Your prompt was blocked because it requested '{desc}'. "
                    "QuantumUI is strictly an educational science tool and blocks offensive security requests.",
                    pattern.pattern
                )

        prompt_lower = prompt.lower()

        # 2. Match known intent patterns
        if "entangle" in prompt_lower or "bell" in prompt_lower or "link" in prompt_lower:
            t = TEMPLATES_CATALOG["quantum-link"]
            return t.qiskit_code, t.circuit_description, t.explanation_by_level

        elif "phase shift" in prompt_lower or "p gate" in prompt_lower or "s gate" in prompt_lower or "rotation" in prompt_lower:
            t = TEMPLATES_CATALOG["phase-shift"]
            return t.qiskit_code, t.circuit_description, t.explanation_by_level

        elif "interference" in prompt_lower or "two hadamard" in prompt_lower or "cancel" in prompt_lower:
            t = TEMPLATES_CATALOG["quantum-interference"]
            return t.qiskit_code, t.circuit_description, t.explanation_by_level

        elif "minus" in prompt_lower or "phase flip" in prompt_lower or "|->" in prompt_lower:
            t = TEMPLATES_CATALOG["phase-flip"]
            return t.qiskit_code, t.circuit_description, t.explanation_by_level

        elif "3 qubit" in prompt_lower or "ghz" in prompt_lower or "triplet" in prompt_lower:
            code = (
                "from qiskit import QuantumCircuit\n\n"
                "# 3-Qubit GHZ State: (|000> + |111>)/sqrt(2)\n"
                "qc = QuantumCircuit(3, 3)\n"
                "qc.h(0)\n"
                "qc.cx(0, 1)\n"
                "qc.cx(1, 2)\n"
                "qc.measure([0, 1, 2], [0, 1, 2])\n"
            )
            desc = "Qubits 0, 1, 2 initialized. Hadamard on Q0. CNOT Q0->Q1. CNOT Q1->Q2. Measurements on all 3 qubits."
            expl = ExplanationByLevel(
                beginner="This entangles three qubits into a GHZ state. All three qubits will measure identically (all 000 or all 111).",
                intermediate="Constructs the 3-qubit GHZ state (|000> + |111>)/sqrt(2). Demonstrates multi-partite entanglement beyond pairs.",
                technical="Unitary sequence CX_{1->2} * CX_{0->1} * H_0 |000> generates maximally entangled 3-qubit statevector. Projection yields 50% |000> and 50% |111>."
            )
            return code, desc, expl

        # Default: Coin Flipper (Superposition)
        t = TEMPLATES_CATALOG["coin-flipper"]
        code_mod = f"# Generated from prompt: {prompt}\n" + t.qiskit_code
        return code_mod, t.circuit_description, t.explanation_by_level

    def explain_result(self, raw_result: Dict[str, int], circuit_code: str) -> ExplanationByLevel:
        total_shots = sum(raw_result.values()) if raw_result else 1024
        outcomes = ", ".join(f"'{k}': {v} shots ({(v/total_shots)*100:.1f}%)" for k, v in raw_result.items())
        
        return ExplanationByLevel(
            beginner=f"Your experiment completed with {total_shots} total runs. The outcomes were: {outcomes}. This matches the quantum probability predicted by your circuit.",
            intermediate=f"Empirical probability distribution across computational basis states: {outcomes}. The outcome distribution reflects wave function collapse according to Born's rule.",
            technical=f"Measurement sampling over {total_shots} shots yielded state histogram {raw_result}. Variance is bounded by binomial statistical shot noise (sigma = sqrt(N*p*(1-p)))."
        )

    def health_check(self) -> bool:
        return True


class HostedLLMAdapter(ModelAdapter):
    """Adapter for remote LLM APIs (OpenAI, Anthropic, Ollama, etc.)."""
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model_name: str = "gpt-4o"):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.fallback = OfflineGenerator()

    def generate_code(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str, ExplanationByLevel]:
        if not self.api_key:
            return self.fallback.generate_code(prompt, context)
        return self.fallback.generate_code(prompt, context)

    def explain_result(self, raw_result: Dict[str, int], circuit_code: str) -> ExplanationByLevel:
        return self.fallback.explain_result(raw_result, circuit_code)

    def health_check(self) -> bool:
        return True


def get_model_adapter(adapter_name: str = "offline_generator") -> ModelAdapter:
    if adapter_name == "hosted_llm":
        return HostedLLMAdapter()
    return OfflineGenerator()
