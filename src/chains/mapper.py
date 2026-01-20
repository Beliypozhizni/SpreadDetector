from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Dict

from src.utils.logger import logger


class ChainsMapper:
    def __init__(self, map_path: Path):
        self._path = map_path
        self._lock = threading.Lock()
        self._mapping: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        with self._lock:
            if not self._path.exists():
                logger.warning(f"Chains map file not found: {self._path}. Using empty mapping.")
                self._mapping = {}
                return

            try:
                with self._path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        raise ValueError("chains_map.json must be an object {input_name: desired_name}")
                    self._mapping = {str(k): str(v) for k, v in data.items()}
            except Exception as e:
                logger.error(f"Failed to load {self._path}: {e}")
                self._mapping = {}

    def _save(self) -> None:
        with self._lock:
            self._path.parent.mkdir(parents=True, exist_ok=True)

            tmp_path = self._path.with_suffix(self._path.suffix + ".tmp")
            try:
                with tmp_path.open("w", encoding="utf-8") as f:
                    json.dump(self._mapping, f, ensure_ascii=False, indent=2)
                tmp_path.replace(self._path)
            except Exception as e:
                logger.error(f"Failed to save {self._path}: {e}")
                try:
                    if tmp_path.exists():
                        tmp_path.unlink()
                except Exception:
                    pass

    def get_map(self) -> dict[str, str]:
        with self._lock:
            return dict(self._mapping)

    def get_aggregated_map(self) -> dict[str, list[str]]:
        with self._lock:
            agg: dict[str, list[str]] = {}
            for input_name, desired_name in self._mapping.items():
                agg.setdefault(desired_name, []).append(input_name)

        return {k: sorted(v) for k, v in sorted(agg.items(), key=lambda x: x[0])}

    def add(self, input_name: str, desired_name: str) -> bool:
        input_name = input_name.strip()
        desired_name = desired_name.strip()
        if not input_name or not desired_name:
            return False

        with self._lock:
            if input_name in self._mapping:
                return False
            self._mapping[input_name] = desired_name

        self._save()
        return True

    def remove(self, input_name: str) -> bool:
        input_name = input_name.strip()
        with self._lock:
            if input_name not in self._mapping:
                return False
            del self._mapping[input_name]

        self._save()
        return True

    def resolve(self, input_name: str) -> str:
        with self._lock:
            mapped = self._mapping.get(input_name)
        if mapped is None:
            logger.warning(f"Chain {input_name} not found")
            return input_name
        return mapped
