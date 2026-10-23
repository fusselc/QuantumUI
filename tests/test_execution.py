import unittest
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.models.schemas import ExecutionConfig, ExecutionStatus
from app.services.execution import ExecutionService

class TestExecution(unittest.TestCase):
    def test_simulate_hadamard(self):
        code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
"""
        config = ExecutionConfig(shots=1000)
        result = ExecutionService.execute(code, config)
        self.assertEqual(result.status, ExecutionStatus.COMPLETE)
        self.assertIsNotNone(result.raw_result)
        self.assertIn("0", result.raw_result)
        self.assertIn("1", result.raw_result)
        self.assertTrue(350 <= result.raw_result["0"] <= 650)
        self.assertTrue(350 <= result.raw_result["1"] <= 650)

    def test_simulate_bell_state(self):
        code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
"""
        config = ExecutionConfig(shots=1000)
        result = ExecutionService.execute(code, config)
        self.assertEqual(result.status, ExecutionStatus.COMPLETE)
        self.assertIn("00", result.raw_result)
        self.assertIn("11", result.raw_result)
        self.assertEqual(result.raw_result.get("01", 0), 0)
        self.assertEqual(result.raw_result.get("10", 0), 0)

    def test_hardware_execution_safety_gate(self):
        code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
"""
        config = ExecutionConfig(backend_id="ibm_sherbrooke", shots=1000)
        result = ExecutionService.execute(code, config, hardware_confirmed=False)
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertIn("Hardware Safety Block", result.error_message)

if __name__ == "__main__":
    unittest.main()
