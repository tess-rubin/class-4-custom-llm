"""Identify the saved run, then launch the unchanged supplied terminal interface."""
from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
from run_evals import load_model, model_hash

record = json.loads((ROOT / "evidence/expanded/execution.json").read_text())
model_path = Path(record["run_dir"]) / "model.pt"
model, _, saved = load_model(model_path)
print("Class 4: expanded experiment | CPU | seed 42", flush=True)
print("Run:", record["run_dir"], flush=True)
print("Model SHA-256:", model_hash(model), flush=True)
print("Completed training steps:", saved["completed_steps"], flush=True)
os.execv(sys.executable, [sys.executable, "chat.py", "--model", str(model_path),
                        "--transcript", "evidence/expanded/terminal_chat.json"])
