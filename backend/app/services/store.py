import json
import os
from pathlib import Path
from typing import List, Optional, Dict
from uuid import UUID
from app.models.schemas import ExperimentRecord

class ExperimentStore:
    def __init__(self, storage_dir: Optional[Path] = None):
        if storage_dir is None:
            self.storage_dir = Path(os.getenv("QUANTUMUI_DATA_DIR", "/tmp/quantumui_data/experiments"))
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, ExperimentRecord] = {}

    def _file_path(self, experiment_id: UUID) -> Path:
        return self.storage_dir / f"{experiment_id}.json"

    def save(self, record: ExperimentRecord) -> ExperimentRecord:
        record_id_str = str(record.experiment_id)
        self._memory_cache[record_id_str] = record
        
        filepath = self._file_path(record.experiment_id)
        temp_filepath = filepath.with_suffix(".tmp")
        
        # Atomic file write
        with open(temp_filepath, "w") as f:
            f.write(record.dump_json(indent=2))
        temp_filepath.replace(filepath)
        
        return record

    def get(self, experiment_id: UUID) -> Optional[ExperimentRecord]:
        record_id_str = str(experiment_id)
        if record_id_str in self._memory_cache:
            return self._memory_cache[record_id_str]

        filepath = self._file_path(experiment_id)
        if not filepath.exists():
            return None

        with open(filepath, "r") as f:
            data = json.load(f)
            record = ExperimentRecord.load_dict(data)
            self._memory_cache[record_id_str] = record
            return record

    def list_all(self, limit: int = 50) -> List[ExperimentRecord]:
        records: List[ExperimentRecord] = []
        for filepath in self.storage_dir.glob("*.json"):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    records.append(ExperimentRecord.load_dict(data))
            except Exception:
                continue
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]

    def delete(self, experiment_id: UUID) -> bool:
        record_id_str = str(experiment_id)
        self._memory_cache.pop(record_id_str, None)
        filepath = self._file_path(experiment_id)
        if filepath.exists():
            filepath.unlink()
            return True
        return False
