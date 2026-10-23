import unittest
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "QuantumUI Core Engine")

    def test_get_templates(self):
        resp = self.client.get("/v1/templates")
        self.assertEqual(resp.status_code, 200)
        templates = resp.json()
        self.assertGreaterEqual(len(templates), 5)
        self.assertTrue(any(t["template_id"] == "coin-flipper" for t in templates))
        self.assertTrue(any(t["template_id"] == "quantum-link" for t in templates))

    def test_create_experiment_from_template(self):
        resp = self.client.post("/v1/experiments", json={"template_id": "quantum-link"})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["template_id"], "quantum-link")
        self.assertTrue("circuit.cx" in data["generated_code"] or "qc.cx" in data["generated_code"])
        self.assertTrue(data["validation_report"]["is_valid"])

    def test_create_experiment_safety_blocked(self):
        resp = self.client.post("/v1/experiments", json={"prompt_text": "Please run Shor's algorithm crack on RSA"})
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"]["title"], "Safety Policy Rejection")

    def test_execute_experiment_simulator(self):
        resp = self.client.post("/v1/experiments", json={"template_id": "coin-flipper"})
        self.assertEqual(resp.status_code, 201)
        exp_id = resp.json()["experiment_id"]

        exec_payload = {
            "execution_config": {
                "primitive_type": "Sampler",
                "backend_id": "aer_simulator",
                "shots": 500
            }
        }
        resp = self.client.post(f"/v1/experiments/{exp_id}/execute", json=exec_payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["execution_result"]["status"], "Complete")
        self.assertIn("0", data["execution_result"]["raw_result"])
        self.assertIsNotNone(data["explanation_by_level"]["beginner"])

    def test_execute_hardware_without_token_blocked(self):
        resp = self.client.post("/v1/experiments", json={"template_id": "coin-flipper"})
        exp_id = resp.json()["experiment_id"]

        exec_payload = {
            "execution_config": {
                "backend_id": "ibm_sherbrooke",
                "shots": 1024
            }
        }
        resp = self.client.post(f"/v1/experiments/{exp_id}/execute", json=exec_payload)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Hardware Confirmation Required", str(resp.json()))

    def test_sharing_consent_toggles(self):
        resp = self.client.post("/v1/experiments", json={"template_id": "coin-flipper"})
        exp_id = resp.json()["experiment_id"]

        resp = self.client.post(f"/v1/experiments/{exp_id}/sharing", json={"dataset": True})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["sharing_state"]["dataset"])
        self.assertFalse(data["sharing_state"]["repository"])

    def test_export_notebook(self):
        resp = self.client.post("/v1/experiments", json={"template_id": "coin-flipper"})
        exp_id = resp.json()["experiment_id"]

        resp = self.client.get(f"/v1/experiments/{exp_id}/export/notebook")
        self.assertEqual(resp.status_code, 200)
        nb = resp.json()
        self.assertEqual(nb["nbformat"], 4)
        self.assertGreaterEqual(len(nb["cells"]), 4)

    def test_export_colab_link(self):
        resp = self.client.post("/v1/experiments", json={"template_id": "coin-flipper"})
        exp_id = resp.json()["experiment_id"]

        resp = self.client.get(f"/v1/experiments/{exp_id}/export/colab")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("colab_url", resp.json())

    def test_list_providers(self):
        resp = self.client.get("/v1/providers")
        self.assertEqual(resp.status_code, 200)
        providers = resp.json()
        self.assertTrue(any(p["id"] == "aer_simulator" for p in providers))
        self.assertTrue(any(p["requires_confirmation"] is True for p in providers if p["type"] == "hardware"))

if __name__ == "__main__":
    unittest.main()
