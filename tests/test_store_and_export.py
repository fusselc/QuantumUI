import unittest
import sys
import tempfile
from pathlib import Path
from uuid import uuid4

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.models.schemas import ExperimentRecord
from app.services.store import ExperimentStore
from app.services.export import ExportService

class TestStoreAndExport(unittest.TestCase):
    def test_store_crud(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ExperimentStore(storage_dir=Path(tmpdir))
            rec = ExperimentRecord(
                experiment_id=uuid4(),
                prompt_text="Test prompt",
                generated_code="qc = QuantumCircuit(1)"
            )
            saved = store.save(rec)
            self.assertEqual(saved.experiment_id, rec.experiment_id)

            fetched = store.get(rec.experiment_id)
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched.prompt_text, "Test prompt")

            all_recs = store.list_all()
            self.assertEqual(len(all_recs), 1)

            deleted = store.delete(rec.experiment_id)
            self.assertTrue(deleted)
            self.assertIsNone(store.get(rec.experiment_id))

    def test_export_jupyter_notebook(self):
        rec = ExperimentRecord(
            experiment_id=uuid4(),
            prompt_text="Superposition test",
            generated_code="from qiskit import QuantumCircuit\nqc = QuantumCircuit(1)\nqc.h(0)\nqc.measure_all()"
        )
        nb = ExportService.to_jupyter_notebook(rec)
        self.assertIn("cells", nb)
        self.assertTrue(any("Superposition test" in "".join(c.get("source", [])) for c in nb["cells"]))

if __name__ == "__main__":
    unittest.main()
