import ast
import re
from typing import List, Set
from app.models.schemas import ValidationReport

UNAUTHORIZED_MODULES: Set[str] = {
    "cryptography", "socket", "subprocess", "os", "sys", "requests", "urllib", "http",
    "shutil", "importlib", "builtins", "ctypes", "pty", "platform", "pickle", "multiprocessing",
    "threading", "asyncio", "signal", "tempfile"
}

UNAUTHORIZED_FUNCTIONS: Set[str] = {
    "eval", "exec", "open", "compile", "getattr", "setattr", "delattr",
    "globals", "locals", "__import__"
}

BLOCKED_CRYPTO_PATTERNS: List[re.Pattern] = [
    re.compile(r"\bshor(?:'s)?\s+algorithm\s+crack\b", re.IGNORECASE),
    re.compile(r"\brsa\s+(?:crack|decrypt|break|factor)\b", re.IGNORECASE),
    re.compile(r"\bprivate\s*key\s*(?:exfiltrate|leak|steal|extract)\b", re.IGNORECASE),
    re.compile(r"\bbrute\s*force\s*(?:cipher|key|password)\b", re.IGNORECASE),
    re.compile(r"\bbreak\s+(?:cryptography|encryption|ciphers)\b", re.IGNORECASE),
    re.compile(r"\bexploit\s+(?:network|vulnerability|system)\b", re.IGNORECASE),
    re.compile(r"\bkey\s+breaking\b", re.IGNORECASE),
    re.compile(r"\belliptic\s+curve\s+(?:crack|break)\b", re.IGNORECASE)
]


class CodeValidator:
    @staticmethod
    def validate_code(code_str: str) -> ValidationReport:
        errors: List[str] = []
        unauthorized_imports: List[str] = []
        blocked_keywords: List[str] = []

        # 1. Check blocked security / offensive patterns in raw text
        for pattern in BLOCKED_CRYPTO_PATTERNS:
            match = pattern.search(code_str)
            if match:
                blocked_keywords.append(match.group(0))
                errors.append(
                    f"Safety Boundary Triggered: Found prohibited cryptographic attack pattern '{match.group(0)}'. "
                    "QuantumUI is strictly an educational science tool and blocks offensive security requests."
                )

        # 2. Syntax check via AST parsing
        syntax_passed = True
        tree = None
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            syntax_passed = False
            errors.append(f"Python Syntax Error on line {e.lineno}: {e.msg}")

        # 3. AST Inspection for imports and forbidden calls
        imports_passed = True
        has_quantum_circuit = False
        has_measurement = False

        if tree:
            for node in ast.walk(tree):
                # Import statement checks: import x
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base_mod = alias.name.split(".")[0]
                        if base_mod in UNAUTHORIZED_MODULES:
                            unauthorized_imports.append(alias.name)
                            imports_passed = False
                            errors.append(f"Security Violation: Import of '{alias.name}' is strictly prohibited.")

                # From import checks: from x import y
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        base_mod = node.module.split(".")[0]
                        if base_mod in UNAUTHORIZED_MODULES:
                            unauthorized_imports.append(node.module)
                            imports_passed = False
                            errors.append(f"Security Violation: Import from '{node.module}' is strictly prohibited.")

                # Forbidden builtin function calls: eval(), exec(), open()
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in UNAUTHORIZED_FUNCTIONS:
                            imports_passed = False
                            errors.append(f"Security Violation: Built-in function '{node.func.id}()' is prohibited.")

                # Detect Qiskit circuit instantiation & measurement
                if isinstance(node, ast.Name) and "QuantumCircuit" in node.id:
                    has_quantum_circuit = True
                if isinstance(node, ast.Attribute) and node.attr in ("measure", "measure_all"):
                    has_measurement = True

        safety_passed = len(blocked_keywords) == 0 and len(unauthorized_imports) == 0
        circuit_valid = ("QuantumCircuit" in code_str) and (syntax_passed)

        is_valid = syntax_passed and imports_passed and safety_passed and circuit_valid

        return ValidationReport(
            is_valid=is_valid,
            syntax_passed=syntax_passed,
            imports_passed=imports_passed,
            safety_passed=safety_passed,
            circuit_valid=circuit_valid,
            errors=errors,
            unauthorized_imports=unauthorized_imports,
            blocked_keywords=blocked_keywords
        )


def validate_code(code_str: str) -> ValidationReport:
    return CodeValidator.validate_code(code_str)
