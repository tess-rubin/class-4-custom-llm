"""Execute a fresh copy of the supplied notebook, preserving every output.

Run from the repository root with its .venv. Optional gates pause after the
baseline and trained inspection while the kernel and all experiment state live.
"""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=["setup", "starter", "expanded"])
    parser.add_argument("--guided", action="store_true")
    parser.add_argument("--output-root", type=Path,
                        help="New directory for rerun notebook and execution record; preserves submitted evidence")
    args = parser.parse_args()
    os.chdir(ROOT)
    experiment = args.experiment
    output = (args.output_root / f"{experiment}.executed.ipynb" if args.output_root else
              ROOT / "notebooks" / f"{experiment}.executed.ipynb")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        parser.error(f"Preserve existing evidence: {output} already exists; archive it before rerunning.")
    evidence = args.output_root.resolve() if args.output_root else ROOT / "evidence" / experiment
    evidence.mkdir(parents=True, exist_ok=True)
    nb = nbformat.read(ROOT / "custom_llm.ipynb", as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
            if 'CORPUS_FOLDER = "corpus"' in cell.source:
                cell.source = cell.source.replace('CORPUS_FOLDER = "corpus"', f'CORPUS_FOLDER = "corpus/{experiment}"')
                if experiment == "setup":
                    cell.source = cell.source.replace('TRAINING_STEPS = 3000', 'TRAINING_STEPS = 10')
        elif "### My prediction" in cell.source:
            cell.source = cell.source.replace(
                "Replace this text with your choices, reasons, and expected changes in generated\ntext, validation loss, and neighbors of a word you choose to inspect.",
                (ROOT / "evidence/provenance/PREDICTION.md").read_text() +
                f"\nExperiment: **{experiment}**; imports only `corpus/{experiment}/`.\n")
    # The kernel is explicitly this project environment, without installing a
    # user-wide kernelspec or depending on a global Jupyter installation.
    nb.metadata.kernelspec = {"name": "python3", "display_name": "Project .venv (Python 3)", "language": "python"}
    client = NotebookClient(nb, timeout=7200, resources={"metadata": {"path": str(ROOT)}})
    client.create_kernel_manager()
    client.km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    started = time.time()
    async with client.async_setup_kernel():
        for index, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            print(f"Executing {experiment} cell {index + 1}/{len(nb.cells)}", flush=True)
            try:
                await client.async_execute_cell(cell, index)
            finally:
                nbformat.write(nb, output)
            for result in cell.get("outputs", []):
                if result.output_type == "stream":
                    print(result.text, end="", flush=True)
            checkpoint = None
            if 'baseline_language_summary = evaluate_suite' in cell.source:
                checkpoint = "baseline"
            if 'save_json("inspection.json"' in cell.source:
                checkpoint = "inspection"
            if args.guided and checkpoint:
                flag = evidence / f"continue-{checkpoint}"
                print(f"LEARNING CHECKPOINT: {checkpoint}; waiting for {flag.relative_to(ROOT)}", flush=True)
                while not flag.exists():
                    await asyncio.sleep(1)
    # The notebook reports its exact new timestamped run folder in cell output.
    saves = [o.text for c in nb.cells if c.cell_type == "code" for o in c.outputs
             if o.output_type == "stream" and "Saved: llm_runs/" in o.text]
    import re
    run = re.search(r"Saved: (llm_runs/\S+)", "\n".join(saves)).group(1)
    record = {"experiment":experiment, "notebook":str(output.relative_to(ROOT)),
              "run_dir":run, "zip":run+".zip", "wall_seconds":time.time()-started,
              "notebook_sha256":hashlib.sha256(output.read_bytes()).hexdigest(),
              "python_executable":sys.executable}
    (evidence / "execution.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record, indent=2), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
