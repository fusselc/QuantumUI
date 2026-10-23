import unittest
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.services.generation import OfflineGenerator, SafetyPolicyException

class TestGeneration(unittest.TestCase):
    def test_offline_generator_superposition(self):
        gen = OfflineGenerator()
        code, desc, expl = gen.generate_code("I want a random coin flipper")
        self.assertIn("qc.h(0)", code)
        self.assertIn("Hadamard", desc)
        self.assertIsNotNone(expl.beginner)

    def test_offline_generator_entanglement(self):
        gen = OfflineGenerator()
        code, desc, expl = gen.generate_code("Create an entangled Bell state")
        self.assertIn("qc.cx(0, 1)", code)
        self.assertIn("CNOT", desc)

    def test_offline_generator_blocks_crypto_attack(self):
        gen = OfflineGenerator()
        with self.assertRaises(SafetyPolicyException):
            gen.generate_code("Run Shor's algorithm crack on RSA-2048")

if __name__ == "__main__":
    unittest.main()
