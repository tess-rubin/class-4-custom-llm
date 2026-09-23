"""Execute every cell with the current Python environment and retain real outputs.

Run from the repository root. Notebook paths may be elsewhere; companion sources
and corpus paths are always resolved relative to the repository root.
"""
import argparse
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.notebook.resolve() == args.output.resolve():
        parser.error("Use a different output filename to preserve the existing notebook.")
    if args.output.exists():
        parser.error("Output already exists; use a new filename.")
    notebook = nbformat.read(args.notebook, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    manager = KernelManager(kernel_name="python3")
    # Avoid accidentally using a global Python kernel instead of this .venv.
    manager.kernel_spec.argv[0] = sys.executable
    client = NotebookClient(notebook, km=manager, timeout=1800,
                            resources={"metadata": {"path": str(ROOT)}})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    try:
        with client.setup_kernel(cleanup_kc=True, cwd=str(ROOT)):
            for index, cell in enumerate(notebook.cells):
                if cell.cell_type == "code":
                    print(f"Executing cell {index + 1}/{len(notebook.cells)}", flush=True)
                    client.execute_cell(cell, index)
                    for output in cell.outputs:
                        if output.output_type == "stream":
                            print(output.text, end="", flush=True)
                nbformat.write(notebook, args.output)
    finally:
        nbformat.write(notebook, args.output)
    print(f"Saved {args.output}; wall time {time.monotonic() - started:.1f}s", flush=True)


if __name__ == "__main__":
    main()
