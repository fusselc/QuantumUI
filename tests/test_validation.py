import unittest
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.services.validation import validate_code

class TestValidation(unittest.TestCase):
    def test_valid_qiskit_circuit(self):
        code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
"""
        report = validate_code(code)
        self.assertTrue(report.is_valid)
        self.assertTrue(report.syntax_passed)
        self.assertTrue(report.imports_passed)
        self.assertTrue(report.safety_passed)
        self.assertEqual(len(report.errors), 0)

    def test_syntax_error_rejected(self):
        code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2
qc.h(0)
"""
        report = validate_code(code)
        self.assertFalse(report.is_valid)
        self.assertFalse(report.syntax_passed)
        self.assertTrue(any("Syntax" in e for e in report.errors))

    def test_unauthorized_imports_blocked(self):
        code = """import os
import socket
import cryptography
from qiskit import QuantumCircuit
qc = QuantumCircuit(1, 1)
qc.h(0)
"""
        report = validate_code(code)
        self.assertFalse(report.is_valid)
        self.assertFalse(report.imports_passed)
        self.assertIn("os", report.unauthorized_imports)
        self.assertIn("socket", report.unauthorized_imports)
        self.assertIn("cryptography", report.unauthorized_imports)

    def test_unauthorized_functions_blocked(self):
        code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(1, 1)
eval("qc.h(0)")
"""
        report = validate_code(code)
        self.assertFalse(report.is_valid)
        self.assertTrue(any("eval" in e for e in report.errors))

    def test_crypto_attack_patterns_blocked(self):
        code = """from qiskit import QuantumCircuit
# Run shor's algorithm crack to break RSA key
qc = QuantumCircuit(4)
qc.h(0)
"""
        report = validate_code(code)
        self.assertFalse(report.is_valid)
        self.assertFalse(report.safety_passed)
        self.assertTrue(any("shor" in kw.lower() for kw in report.blocked_keywords))

if __name__ == "__main__":
    unittest.main()
