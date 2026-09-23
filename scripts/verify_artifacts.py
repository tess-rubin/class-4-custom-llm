#!/usr/bin/env python3
"""Read-only integrity checks for the two completed classroom experiments.

Run with the project virtual environment. This script reads saved artifacts and
initializes a seed-42 reference model; it never trains, edits, or writes results.
The exact-prefix leakage check cannot certify absence of semantic leakage.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stdout
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import random
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from nanogpt_model import GPT, GPTConfig
from run_evals import load_suite, matching_cases, model_hash, suite_hash, word_tokens

FIXED_FILES = {
    "nanogpt_model.py": "7c01703240dbec5d554527dc666e35b3df8391d0b117fddc07afcf325a21d11c",
    "run_evals.py": "da87f28d128344807512e2bac1cfc662b37ac2c7e4a32b84c09f1950e92d67a0",
    "chat.py": "6152c8b7780f3b46fef5de38461adfc4b1a55df70ed106ca73ec5e9aded86d25",
    "evals/language_evals.json": "e8affcd72841e3ed7da5c0b6b116327fe9f69c9abd66a1180d1d88ceaa3e17f7",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def close(actual, expected, label, tolerance=1e-9):
    require(math.isfinite(actual) and math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance),
            f"{label}: {actual!r} != {expected!r}")


def state_hash(state):
    result = hashlib.sha256()
    for name, tensor in sorted(state.items()):
        result.update(name.encode())
        result.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return result.hexdigest()


def verify_summary(rows, reported, label):
    correct = sum(row["score"] for row in rows)
    scorable = sum(row["status"] in {"scored", "tied"} for row in rows)
    require(reported["correct"] == correct and reported["total"] == len(rows)
            and reported["scorable"] == scorable, f"{label}: summary counts disagree")
    close(reported["success_rate_all_cases"], correct / len(rows), label + " all-case success")
    close(reported["coverage"], scorable / len(rows), label + " coverage")
    if scorable:
        close(reported["accuracy_scorable_cases"], correct / scorable, label + " scorable accuracy")
    else:
        require(reported["accuracy_scorable_cases"] is None, f"{label}: undefined accuracy must be null")


def verify_eval(folder, suite, vocabulary, identity, stage):
    saved_suite = read_json(folder / "eval_cases.json")
    rows = read_json(folder / "eval_results.json")
    summary = read_json(folder / "eval_summary.json")
    cases = suite["cases"]
    require(saved_suite == suite, f"{folder}: saved suite differs")
    require([row["id"] for row in rows] == [case["id"] for case in cases],
            f"{folder}: missing, reordered, or duplicate eval IDs")
    require(summary["suite_sha256"] == suite_hash(suite), f"{folder}: suite hash differs")
    require(summary["model_sha256"] == identity, f"{folder}: model hash differs")
    require(summary["stage"] == stage, f"{folder}: incorrect stage")
    require(summary["settings"] == {"seed": 2026, "temperature": .8, "max_tokens": 24},
            f"{folder}: inference settings changed")
    known = set(vocabulary)
    for index, (case, row) in enumerate(zip(cases, rows)):
        label = f"{folder.name}/{case['id']}"
        for key in ("group", "category", "prompt", "choices", "reason"):
            require(row[key] == case[key], f"{label}: changed {key}")
        require(row["expected"] == case["answer"] and row["stage"] == stage,
                f"{label}: changed answer or stage")
        tokens = word_tokens(case["prompt"])
        unknown = sorted(set(tokens) - known)
        unknown_choices = [choice for choice in case["choices"] if word_tokens(choice)[0] not in known]
        require(row["unknown_prompt_words"] == unknown and row["unknown_choices"] == unknown_choices,
                f"{label}: vocabulary audit disagrees")
        require(row["sample_seed"] == 2026 + index and isinstance(row["generated_text"], str),
                f"{label}: missing free continuation or wrong sampling seed")
        require(row["prompt_truncated"] == (len(tokens) + 1 > 48), f"{label}: context audit disagrees")
        expected_status = "context_too_long" if len(tokens) + 1 > 48 else (
            "out_of_vocabulary" if unknown or unknown_choices else None)
        probs = row["choice_probabilities"]
        if expected_status:
            require(row["status"] == expected_status and row["score"] == 0
                    and row["predicted_choice"] is None and not probs, f"{label}: unscorable case gained credit")
        else:
            require(set(probs) == set(case["choices"]), f"{label}: missing choice probabilities")
            require(all(math.isfinite(p) and 0 <= p <= 1 for p in probs.values())
                    and sum(probs.values()) <= 1 + 1e-6, f"{label}: invalid full-vocabulary probabilities")
            ranked = sorted(probs, key=probs.get, reverse=True)
            tied = abs(probs[ranked[0]] - probs[ranked[1]]) <= 1e-10
            require(row["status"] == ("tied" if tied else "scored"), f"{label}: tie status disagrees")
            require(row["predicted_choice"] == (None if tied else ranked[0]), f"{label}: prediction disagrees")
            require(row["score"] == int(not tied and ranked[0] == case["answer"]), f"{label}: score disagrees")
    verify_summary(rows, summary["overall"], str(folder))
    for dimension in ("group", "category"):
        groups = {row[dimension] for row in rows}
        require(set(summary[f"by_{dimension}"]) == groups, f"{folder}: omitted {dimension}")
        for group in groups:
            verify_summary([row for row in rows if row[dimension] == group],
                           summary[f"by_{dimension}"][group], f"{folder}/{group}")
    with (folder / "eval_results.csv").open(newline="", encoding="utf-8") as file:
        csv_rows = list(csv.DictReader(file))
    require(len(csv_rows) == len(rows), f"{folder}: CSV row count differs")
    for csv_row, row in zip(csv_rows, rows):
        for key, value in row.items():
            expected = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else (
                "" if value is None else str(value))
            require(csv_row[key] == expected, f"{folder}/{row['id']}: CSV {key} differs from JSON")
    return summary, rows


def verify_notebook(path, run):
    notebook = read_json(path)
    code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code" and "".join(cell["source"]).strip()]
    require(code, f"{path}: no code cells")
    for index, cell in enumerate(code):
        require(isinstance(cell.get("execution_count"), int), f"{path}: unexecuted code cell {index}")
        require(all(output.get("output_type") != "error" for output in cell.get("outputs", [])),
                f"{path}: error output in code cell {index}")
    outputs = json.dumps([cell.get("outputs", []) for cell in code], ensure_ascii=False)
    require(run.name in outputs, f"{path}: outputs do not identify run {run.name}")
    require("image/svg+xml" in outputs, f"{path}: loss plot output absent")
    return len(code)


def verify_run(run, notebook, suite, expected_steps, rerun=None):
    config = read_json(run / "config.json")
    training = read_json(run / "training_summary.json")
    history = read_json(run / "history.json")
    split = read_json(run / "split.json")
    manifest = read_json(run / "corpus_manifest.json")
    separation = read_json(run / "eval_separation.json")
    vocab_report = read_json(run / "vocabulary_report.json")
    tokenization = read_json(run / "tokenization.json")
    inspection = read_json(run / "inspection.json")
    checkpoint = read_json(run / "checkpoint.json")
    vocab = tokenization["vocabulary"]
    for key, expected in {"training_steps": expected_steps, "learning_rate": .001, "seed": 42,
                          "n_embd": 64, "n_head": 4, "n_layer": 2, "block_size": 48,
                          "batch_size": 32, "device": "cpu", "corpus_mode": "classroom"}.items():
        require(config[key] == expected, f"{run}: unexpected {key}: {config[key]!r}")
    require(training["completed_steps"] == expected_steps and training["interrupted"] is False,
            f"{run}: main run incomplete or interrupted")
    require(math.isfinite(training["elapsed_seconds"]) and training["elapsed_seconds"] > 0,
            f"{run}: invalid runtime")
    require(config["language_eval_suite_sha256"] == suite_hash(suite)
            and separation["suite_sha256"] == suite_hash(suite), f"{run}: suite hashes disagree")
    require(config["reserved_eval_passages"] == separation["excluded_passages"] > 0,
            f"{run}: missing reserved classroom passage evidence")
    corpus_bytes = (run / "corpus.txt").read_bytes()
    require(config["corpus_sha256"] == digest(corpus_bytes), f"{run}: corpus bytes changed")
    raw_documents = corpus_bytes.decode("utf-8").splitlines()
    require(not matching_cases(corpus_bytes.decode("utf-8"), suite), f"{run}: exact eval prefix in corpus")
    documents = sorted(set(raw_documents))
    random.Random(42).shuffle(documents)
    cut = int(.9 * len(documents))
    require(split["train"] == documents[:cut] and split["validation"] == documents[cut:],
            f"{run}: saved split differs from seed-42 deduplicated 90/10 split")
    require(not (set(split["train"]) & set(split["validation"])), f"{run}: train/validation overlap")
    require(manifest["unique_passages"] == len(documents)
            and manifest["duplicates_removed"] == len(raw_documents) - len(documents), f"{run}: dedup counts disagree")
    for side, panel_seed in (("train", 123), ("validation", 456)):
        panel = split[f"evaluation_{side}"]
        require(panel == random.Random(panel_seed).sample(split[side], min(20, len(split[side]))),
                f"{run}: fixed {side} panel disagrees")
        require(config[f"{side}_documents"] == len(split[side])
                and config["evaluation_panel_size"][side] == len(panel) <= 20, f"{run}: panel/document counts disagree")
    counts = Counter(token for doc in split["train"] for token in word_tokens(doc))
    retained = sorted((token for token in counts if len(token) <= 128), key=lambda token: (-counts[token], token))[:509]
    require(vocab == ["<UNK>", "<BOS>", "<EOS>"] + sorted(retained), f"{run}: vocabulary not built from training split")
    require(config["vocabulary_size"] == len(vocab) and checkpoint["vocabulary"] == vocab,
            f"{run}: vocabulary sizes/identities disagree")
    known = set(vocab)
    for side, key in (("train", "training_unknown_rate"), ("validation", "validation_unknown_rate")):
        tokens = [token for doc in split[side] for token in word_tokens(doc)]
        rate = sum(token not in known for token in tokens) / max(1, len(tokens))
        close(config[key], rate, f"{run}: {key}")
        close(vocab_report[key], rate, f"{run}: report {key}")
    require(vocab_report["training_types"] == len(counts) and vocab_report["retained_types"] == len(retained)
            and vocab_report["omitted_types"] == sorted(set(counts) - set(retained)), f"{run}: vocabulary report disagrees")
    expected_timeline = [0, max(1, expected_steps // 2), expected_steps]
    require([row["step"] for row in history] == expected_timeline, f"{run}: missing baseline/halfway/final loss")
    with (run / "training.csv").open(newline="") as file:
        training_csv = list(csv.DictReader(file))
    require(len(training_csv) == len(history), f"{run}: training CSV row count differs")
    for row, csv_row in zip(history, training_csv):
        require(int(csv_row["step"]) == row["step"], f"{run}: training CSV step differs")
        for key in ("training_loss", "validation_loss"):
            require(math.isfinite(row[key]) and row[key] >= 0, f"{run}: invalid loss")
            close(float(csv_row[key]), row[key], f"{run}: CSV {key}")
        # split('\n') preserves empty generated samples, including the final one.
        samples = (run / "samples" / f"step_{row['step']:04d}.txt").read_text().split("\n")
        require(len(samples) == 4, f"{run}: sample timeline must preserve all four strings")
    temps = read_json(run / "temperature_comparison.json")
    require(set(temps) == {"0.3", "0.8", "1.2"}
            and all(len(rows) == 4 and all(isinstance(row, str) for row in rows) for rows in temps.values()),
            f"{run}: incomplete temperature comparison")
    require((run / "training_curves.svg").is_file(), f"{run}: loss plot missing")
    summaries, rows_by_stage, hashes = {}, {}, {}
    args = None
    for stage, filename, step in (("untrained", "model_untrained.pt", 0), ("final", "model.pt", expected_steps)):
        saved = torch.load(run / filename, map_location="cpu", weights_only=True)
        require(saved["vocabulary"] == vocab and saved["completed_steps"] == step,
                f"{run}/{filename}: vocabulary or training budget disagrees")
        require(saved["model_args"] == (args or saved["model_args"]), f"{run}: architecture changed during training")
        args = saved["model_args"]
        for field in ("n_embd", "n_head", "n_layer", "block_size", "vocab_size"):
            expected = len(vocab) if field == "vocab_size" else config[field]
            require(args[field] == expected, f"{run}: saved {field} disagrees")
        hashes[stage] = state_hash(saved["model"])
        embedding = saved["model"]["transformer.wte.weight"].tolist()
        probe_id = inspection["token_id"]
        require(vocab[probe_id] == inspection["token"] and len(embedding[probe_id]) == 64,
                f"{run}: inspected token/vector mismatch")
        key = "embedding_before" if stage == "untrained" else "embedding_after"
        require(embedding[probe_id] == inspection[key], f"{run}: inspected vector differs from saved model")
        viewer_embeddings = checkpoint["initial_embeddings"] if stage == "untrained" else checkpoint["weights"]["wte"]
        require(viewer_embeddings == embedding, f"{run}: viewer embeddings differ from saved model")
        probabilities = inspection["probabilities_before" if stage == "untrained" else "probabilities_after"]
        require(len(probabilities) == len(vocab) and all(math.isfinite(p) and 0 <= p <= 1 for p in probabilities),
                f"{run}: incomplete inspected probability vector")
        close(sum(probabilities), 1, f"{run}: inspected probability sum", tolerance=1e-6)
        summaries[stage], rows_by_stage[stage] = verify_eval(run / "language_evals" / stage, suite, vocab, hashes[stage], stage)
    require(hashes["untrained"] != hashes["final"], f"{run}: trained weights equal untrained weights")
    torch.manual_seed(42)
    # nanoGPT prints its parameter count during initialization; keep stdout JSON.
    with redirect_stdout(io.StringIO()):
        fresh = GPT(GPTConfig(**args))
    require(model_hash(fresh) == hashes["untrained"], f"{run}: baseline is not the fresh seed-42 model")
    require(sum(parameter.numel() for parameter in fresh.parameters()) == config["parameters"], f"{run}: parameter count disagrees")
    first = inspection["first_update"]
    require(first["token"] == inspection["token"] and first["coordinate"] == 0
            and first["before"] == inspection["embedding_before"][0], f"{run}: first-update coordinate disagrees")
    require(all(math.isfinite(first[key]) for key in ("before", "gradient", "after"))
            and first["before"] != first["after"], f"{run}: absent or invalid first update")
    warmup = min(100, max(1, expected_steps // 10))
    close(first["learning_rate"], .001 / warmup, f"{run}: first warmup learning rate")
    require(read_json(run / "language_eval_comparison.json") == summaries, f"{run}: comparison summaries disagree")
    if rerun:
        rerun_summary, rerun_rows = verify_eval(rerun, suite, vocab, hashes["final"], read_json(rerun / "eval_summary.json")["stage"])
        # Stage labels may identify reruns; every other saved value must reproduce.
        normalized = [{key: value for key, value in row.items() if key != "stage"} for row in rerun_rows]
        expected = [{key: value for key, value in row.items() if key != "stage"} for row in rows_by_stage["final"]]
        require(normalized == expected, f"{run}: saved-model rerun differs from final notebook eval")
    archive = run.with_suffix(".zip")
    with zipfile.ZipFile(archive) as zipped:
        require(zipped.testzip() is None, f"{archive}: corrupt ZIP member")
        for path in run.rglob("*"):
            if path.is_file():
                name = path.relative_to(run).as_posix()
                require(name in zipped.namelist() and zipped.read(name) == path.read_bytes(),
                        f"{archive}: missing or stale member {name}")
    return {"run": str(run), "notebook": str(notebook), "executed_code_cells": verify_notebook(notebook, run),
            "completed_steps": expected_steps, "suite_sha256": suite_hash(suite), "model_hashes": hashes,
            "all_case_results": {stage: summary["overall"] for stage, summary in summaries.items()},
            "zip": str(archive), "saved_model_rerun_verified": rerun is not None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starter-run", type=Path, required=True)
    parser.add_argument("--expanded-run", type=Path, required=True)
    parser.add_argument("--starter-notebook", type=Path, required=True)
    parser.add_argument("--expanded-notebook", type=Path, required=True)
    parser.add_argument("--starter-rerun", type=Path)
    parser.add_argument("--expanded-rerun", type=Path)
    parser.add_argument("--expected-steps", type=int, default=3000)
    arguments = parser.parse_args()
    torch.set_num_threads(min(4, torch.get_num_threads()))
    try:
        for filename, expected in FIXED_FILES.items():
            require(digest((ROOT / filename).read_bytes()) == expected, f"Fixed source changed: {filename}")
        suite = load_suite(ROOT / "evals/language_evals.json")
        require(len(suite["cases"]) == 48, "The fixed suite must contain all 48 cases")
        require(arguments.starter_run.resolve() != arguments.expanded_run.resolve(), "Experiments must have separate run folders")
        results = [verify_run(arguments.starter_run, arguments.starter_notebook, suite, arguments.expected_steps, arguments.starter_rerun),
                   verify_run(arguments.expanded_run, arguments.expanded_notebook, suite, arguments.expected_steps, arguments.expanded_rerun)]
        print(json.dumps({"status": "PASS", "fixed_sources_unchanged": True, "experiments": results,
                          "limitation": "Exact-prefix separation is checked; semantic leakage and the student's explanations require human review."}, indent=2))
    except (AssertionError, KeyError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
