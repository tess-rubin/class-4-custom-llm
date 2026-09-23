"""Build the current report from saved artifacts, without training or inference."""
import csv
import hashlib
import io
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(cell(x) for x in row) + " |" for row in rows])


def pct(value):
    return "undefined" if value is None else f"{value:.2%}"


def link(path, label):
    return f"[{label}]({path})"


def main():
    experiments = read("experiments.json")
    runs = {label: Path(experiments[label]["run"]) for label in ("starter", "expanded")}
    config = {k: read(p / "config.json") for k, p in runs.items()}
    summaries = {(label, stage): read(path / "language_evals" / stage / "eval_summary.json")
                 for label, path in runs.items() for stage in ("untrained", "final")}
    results = {(label, stage): read(path / "language_evals" / stage / "eval_results.json")
               for label, path in runs.items() for stage in ("untrained", "final")}
    assert [summaries[k]["overall"]["correct"] for k in summaries] == [9, 20, 7, 24]
    acceptance = read("evidence/current-acceptance.json")
    assert acceptance["status"] == "PASS"
    chat = read("evidence/current-chat/transcript.json")
    assert chat["model_sha256"] == summaries[("expanded", "final")]["model_sha256"]
    assert len(chat["turns"]) == 3
    parts = ["# Class 4: learning to train a tiny language model\n",
             "The classroom model improved from **9/48 to 20/48** on the fixed four-choice tests. "
             "The fresh expanded model improved from **7/48 to 24/48**. Its added opposites and "
             "negation lessons did **not** produce a successful extension-test answer: two opposites "
             "cases became scorable but remained wrong, and all negation cases remained unscorable. "
             "The higher final total came from the familiar-word rephrasing tests. These are "
             "**public development tests**, not an unseen test of general understanding.\n",
             "[Executed classroom notebook](custom_llm.ipynb) · "
             "[Executed expanded notebook](custom_llm_expanded.ipynb) · "
             "[Acceptance checks](evidence/current-acceptance.json) · "
             "[All 192 case results and continuations](docs/all-evals.md) · "
             "[Real terminal recording](evidence/current-chat/terminal.cast)\n",
             "**Which results are current?** This README describes only the two runs in "
             "[experiments.json](experiments.json). Earlier experiments already existed in this "
             "repository and remain preserved. Their [prior report](https://github.com/tess-rubin/"
             "class-4-custom-llm/blob/a52ef411ee9f80ce50deb658039cdf7b645421a4/README.md) belongs "
             "to that earlier revision; its scores and corpus are not substituted for this session's results.\n",
             "## Four complete result sets\n"]
    rows = []
    comparison = []
    for (label, stage), summary in summaries.items():
        overall = summary["overall"]
        folder = runs[label] / "language_evals" / stage
        rows.append([label, stage, f"{overall['correct']}/48 ({pct(overall['success_rate_all_cases'])})",
                     f"{overall['correct']}/{overall['scorable']} ({pct(overall['accuracy_scorable_cases'])})",
                     f"{overall['scorable']}/48 ({pct(overall['coverage'])})",
                     " / ".join(link(folder / file, title) for file, title in
                                [("eval_results.json", "JSON"), ("eval_results.csv", "CSV"),
                                 ("eval_summary.json", "summary")])])
        comparison.append({"experiment": label, "stage": stage, **overall})
    parts.append(table(["Experiment", "Stage", "All-case success", "Scorable accuracy", "Case coverage", "Complete evidence"], rows))
    parts.append("""
**Four-choice scores:** the model receives only the prefix. The unchanged scorer
compares the probabilities of four possible next words, then checks its selection
against the answer key. The key and choices never enter the model input. Ties
receive zero. The four probabilities are entries from the full vocabulary, not
probabilities rescaled to sum to one across those four words.

**Free continuations:** a separate sampling step writes an unrestricted reply.
That reply does not determine the four-choice score. A correct choice can coexist
with a poor reply, and an empty reply is retained when the end token is sampled.

**Coverage:** a case is scorable only if every prompt word and every choice is in
the saved vocabulary and the prompt fits the context. Unscorable cases still
count as zero out of all 48. Scorable accuracy uses a smaller denominator. This
case-level coverage is different from the fraction of unknown individual tokens
in the training or validation text. Coverage does not change during a run because
training changes weights, not that run's fixed vocabulary.

## Choices and prediction, recorded before training

The user selected local CPU execution, **3,000 weight updates**, a configured
learning rate of **0.001**, and **opposites plus negation**. The
[pretraining prediction](experiment_plan.json) was that training loss would fall,
samples would become more corpus-like, validation loss might improve, and added
data might improve coverage and some scores while failures remained. The
prediction was supported for loss and familiar templates, but the targeted
extension tests did not show success.

A step is one batch update, not a whole pass through the corpus. The selected
budget and rate are the assignment's starting suggestions. Too large a rate can
cause unstable updates; too small a rate can make learning slow. The supplied
100-step warmup and cosine decay remain unchanged. The first actual rate is
0.00001, with a peak setting of 0.001 and decay toward one tenth of that setting.

Both runs use seed 42, CPU with up to four threads, two transformer blocks, four
attention heads, 64-number embeddings, 48-token context, batches of 32, no dropout,
and AdamW with its supplied clipping and regularization. The expanded model starts
fresh; it does not continue the starter's weights. Seeds/settings stay the same,
but a larger vocabulary changes tensor dimensions and IDs, so initial models are
not identical. Splits and loss panels stay fixed **within** each experiment.

## Teaching data and separation

The starter reads an empty `corpus/starter/` folder and uses the supplied classroom
generator. The expanded run reads only `corpus/expanded/`, adding exactly
[120 opposites passages](corpus/expanded/opposites.txt) and
[120 negation passages](corpus/expanded/negation.txt). They are newly composed,
AI-assisted, shareable text with invented people and ordinary situations, not
private records or copied third-party material. See the
[source choices and review](docs/corpus-design.md) and
[pretraining extraction audit](evidence/extension_pretraining_review.json).

Contextual contrasts could teach relationships such as heavy/light and noisy/quiet.
Negation examples distinguish rejected actions from what actually happens. Each
line is one sentence, with semicolons where needed to keep a correction together;
the supplied loader extracts exactly 240 unique passages, each at most 19 tokens.
There are no PDFs, OCR claims, or extraction warnings. This small addition does
not guarantee coverage of the particular words used in every public test.

The classroom reservation removes 160 generated passages containing exact test
prefixes before deduplication, the 90/10 split, or vocabulary construction. Imported
files and final passages also pass the supplied prefix guard. All teaching text
was additionally reviewed for copied test stories, close story paraphrases,
answer lists, and outputs; none were identified. Exact matching alone cannot
prove semantic separation, so both source files are public for inspection.

Evals, answer keys, reports, source notes, transcripts, and result folders stay
outside both corpus inputs. Vocabulary comes only from the training split. A
source file can contribute passages to both train and validation; this is not a
test on unseen source files. Classroom validation shares templates with training.
""")
    data_rows = []
    for label, path in runs.items():
        c = config[label]
        m = read(path / "corpus_manifest.json")
        v = read(path / "vocabulary_report.json")
        data_rows.append([label, m["unique_passages"], c["train_documents"], c["validation_documents"],
                          c["vocabulary_size"], v["training_types"], len(v["omitted_types"]),
                          pct(c["training_unknown_rate"]), pct(c["validation_unknown_rate"])])
    parts.append(table(["Corpus", "Unique passages", "Train", "Validation", "Vocab incl. specials", "Training types", "Omitted train types", "Train UNK", "Validation UNK"], data_rows))
    parts.append("The expansion contributes **216 training passages and 24 validation passages**. "
                 "The 495 expanded training token types all fit below the 509-type cap; its "
                 "validation UNK rate comes from words absent from training. The 240 added passages "
                 "are about 5% of all 4,832 unique passages. No vocabulary entries were inserted "
                 "from eval text.\n")
    parts.append("## Group and category breakdowns\n\nEach entry is **correct / total (scorable)**. Every case remains in its denominator.\n")
    for dimension in ("group", "category"):
        keys = sorted(summaries[("starter", "untrained")][f"by_{dimension}"])
        values = []
        for key in keys:
            row = [key]
            for summary in summaries.values():
                s = summary[f"by_{dimension}"][key]
                row.append(f"{s['correct']}/{s['total']} ({s['scorable']})")
            values.append(row)
        parts.append(table([dimension.title(), "Starter untrained", "Starter final", "Expanded untrained", "Expanded final"], values))
    parts.append("""
The four additional final successes are rephrasing cases that were already
scorable in the starter. Their score improvement is therefore not just a change
in vocabulary coverage. However, the changed corpus also changes the split and
initialization dimensions, so one seed does not isolate a causal effect of the
new teaching patterns.

The two newly scorable opposites cases remain wrong: `lang_28` selects **heavy**
instead of **cold**, and `lang_29` selects **early** instead of **full**. This is
coverage improvement without successful answer selection. The third opposites
case still lacks the distractor `round`. All three negation cases remain
unscorable: the teaching material does not supply all their color, purchase, or
door-state words. More training on the unchanged vocabulary could not fix those
missing words. We preserve these failures rather than tuning the corpus after
seeing them or claiming successful negation learning.

### Actual continuations, including failures
""")
    selected = []
    for label, case_ids in [("starter", ["lang_18", "lang_28"]), ("expanded", ["lang_18", "lang_21", "lang_28", "lang_29", "lang_31", "lang_33"])]:
        lookup = {r["id"]: r for r in results[(label, "final")]}
        for case_id in case_ids:
            row = lookup[case_id]
            selected.append([label, case_id, row["prompt"], row["predicted_choice"] or "unscorable",
                             row["expected"], row["generated_text"] or "[empty response]"])
    parts.append(table(["Model", "Case", "Prompt", "Choice", "Expected", "Actual free continuation"], selected))
    parts.append("For example, the expanded bus case gets the choice `route` right but freely "
                 "continues with “taxi was in the truck .” A four-choice success is a narrow "
                 "measurement, not evidence of a good unrestricted response. "
                 "[Every prompt, status, missing word, score, and continuation](docs/all-evals.md) is retained.\n")
    parts.append("## Losses and every saved sample\n\nThese are **fixed panels of 20 training and 20 validation documents** per run, "
                 "averaging non-padding next-token targets, including EOS. They are small estimates, "
                 "not full-corpus losses. Different corpora and vocabularies make raw loss values "
                 "unsuitable for ranking the two models. The expanded training panel contains zero "
                 "extension passages and its validation panel contains only one, so the curves are "
                 "weak evidence about the added skills.\n")
    for label, path in runs.items():
        parts.append(f"### {label.title()}\n\n![{label} fixed-panel loss]({path}/training_curves.svg)\n")
        history = read(path / "history.json")
        parts.append(table(["Step", "Training panel loss", "Validation panel loss"],
                           [[r["step"], repr(r["training_loss"]), repr(r["validation_loss"])] for r in history]))
        parts.append(f"Full measured table: [history.json]({path}/history.json), [training.csv]({path}/training.csv).\n")
        for step in (0, 1500, 3000):
            sample_path = path / "samples" / f"step_{step:04d}.txt"
            samples = (ROOT / sample_path).read_text().split("\n")
            assert len(samples) == 4
            parts.append(f"**Step {step}** — [full saved file]({sample_path})\n\n```text\n" +
                         "\n".join(sample if sample else "[empty sample]" for sample in samples) + "\n```\n")
    parts.append("Both runs change from unstructured word sequences to familiar classroom "
                 "templates by step 1,500. Some starter samples are unchanged at step 3,000; "
                 "additional steps do not require every seeded sample to change. These plausible "
                 "templates coexist with the extension failures above.\n")
    parts.append("## How learning works, using this run\n\nThis is an **assisted explanatory draft**. The student selected settings and "
                 "categories; Codex helped execute, inspect, and explain the experiments. "
                 "It is not a claim that the student independently wrote the teaching corpus "
                 "or has already explained every concept. [Plain-language study guide](docs/learning-guide.md).\n")
    p = runs["starter"]
    inspection = read(p / "inspection.json")
    tokenization = read(p / "tokenization.json")
    first = inspection["first_update"]
    parts.append(f"A **corpus** is the collection of practice sentences. This model splits words "
                 f"and punctuation into **tokens**. The token `customer` has **ID {inspection['token_id']}**, "
                 "an arbitrary lookup number, not an amount of meaning. Its **embedding** is "
                 "the row of 64 learned numbers selected by that ID. The network combines these "
                 "numbers using learned weights to predict the next token.\n")
    parts.append(f"[Tokenization and IDs]({p}/tokenization.json) · [Actual inspection]({p}/inspection.json)\n")
    for state in ("before", "after"):
        vector = inspection[f"embedding_{state}"]
        formatted = "[\n" + ",\n".join("  " + ", ".join(repr(v) for v in vector[i:i+4]) for i in range(0,64,4)) + "\n]"
        parts.append(f"<details>\n<summary>All 64 customer embedding coordinates {state} training</summary>\n\n```json\n{formatted}\n```\n\n</details>\n")
    vocabulary = tokenization["vocabulary"]
    prob_rows = []
    for word in ["customer", "reviewed", "recommended", "ordered", "selected", "compared"]:
        i = vocabulary.index(word)
        prob_rows.append([word, pct(inspection["probabilities_before"][i]), pct(inspection["probabilities_after"][i])])
    parts.append("For the same prefix **“the customer”**, these are next-token probabilities "
                 "before sampling temperature is applied:\n")
    parts.append(table(["Possible next token", "Before training", "After training"], prob_rows))
    parts.append("The trained model assigns probability to purchase-related verbs because those "
                 "continuations recur in the teaching text. A probability is a model estimate, "
                 "not a truth score. Sampling chooses a token from the resulting distribution, "
                 "appends it to the context, and repeats until EOS or the output limit.\n")
    parts.append(table(["First update of customer coordinate 0", "Measured value"],
                       [["Before", repr(first["before"])], ["Recorded gradient (before clipping)", repr(first["gradient"])],
                        ["Actual warmup learning rate", repr(first["learning_rate"])], ["After", repr(first["after"])],
                        ["Change: after − before", repr(first["after"] - first["before"])]]))
    parts.append("**Loss** measures how poorly the predicted probabilities match the actual next "
                 "tokens in the practice sentences. Backpropagation computes **gradients**, which "
                 "describe how changes to weights affect loss locally. AdamW uses those gradients "
                 "to make **weight updates**. Repeating this process changes later predictions. "
                 "The recorded gradient is before norm clipping; AdamW also uses adaptive scaling, "
                 "momentum and weight decay. The measured change therefore is not simply minus "
                 "the displayed gradient times the configured 0.001. The first small update is "
                 "different from the total change across 3,000 steps.\n\n"
                 "**Attention** lets each position combine information from earlier tokens; the "
                 "causal mask prevents looking at future answers. Learned token and position "
                 "embeddings, attention blocks, and other weights work together. The saved "
                 "attention rows show one head, not a full explanation of a decision.\n")
    neighbors = []
    for label, path in runs.items():
        checkpoint = read(path / "checkpoint.json")
        words = checkpoint["vocabulary"]
        index = words.index("customer")
        for stage, matrix in [("before",checkpoint["initial_embeddings"]),("after",checkpoint["weights"]["wte"])]:
            matrix = np.asarray(matrix)
            unit = matrix / np.linalg.norm(matrix,axis=1,keepdims=True)
            similarities = unit @ unit[index]
            similarities[index] = -np.inf
            neighbors.append([label,stage,", ".join(f"{words[j]} ({similarities[j]:.4f})" for j in np.argsort(-similarities)[:3])])
    parts.append(table(["Run", "Stage", "Three cosine neighbors of customer in full 64D"], neighbors))
    parts.append("The trained neighbors share classroom contexts; this supports a narrow "
                 "distributional pattern, not broad word understanding. Open "
                 "[embedding-viewer.html](embedding-viewer.html) locally and load a run's "
                 "`checkpoint.json` to inspect the vectors. The 3D PCA projection compresses "
                 "64 dimensions; it can distort apparent distances. Cosine neighbors above use all 64.\n")
    parts.append("## Temperature changes sampling, not weights\n\nThe comparisons use temperatures "
                 "**0.3, 0.8, 1.2**, the same BOS starting token, and sampling seed 2026. "
                 "Lower temperature concentrates probabilities; higher temperature spreads them "
                 "out. Neither retrains the network. The baseline sample timeline also uses "
                 "temperature 0.8 and seed 2026, with four samples of up to 32 new tokens. "
                 "Eval/chat generation instead uses a prefix, up to 24 new tokens, per-case/turn "
                 "seeds, and masks generated BOS. These two supplied generators are preserved.\n")
    temp_rows = []
    temp_doc = ["# Every temperature sample\n\nSaved text is shown verbatim, with empty strings explicitly marked. No retraining occurs between temperatures.\n"]
    for label,path in runs.items():
        temperatures=read(path / "temperature_comparison.json")
        parts.append(f"{label.title()}: [complete temperature data]({path}/temperature_comparison.json).\n")
        for temperature,samples in temperatures.items():
            temp_rows.append([label,temperature,samples[0] or "[empty sample]"])
            temp_doc.append(f"## {label}, temperature {temperature}\n\n```text\n"+'\n'.join(s or '[empty sample]' for s in samples)+'\n```\n')
    parts.append(table(["Run", "Temperature", "First actual sample"],temp_rows))
    parts.append("The expanded 1.2 sample becomes garbled, while its lower-temperature samples "
                 "follow classroom patterns. The starter's complete 0.8 and 1.2 sample sets happen "
                 "to be identical for this seed; higher temperature does not guarantee different "
                 "text on each draw. [All temperature samples](docs/temperature-samples.md).\n")
    parts.append("## Working chat and real interaction evidence\n\nThe unchanged [chat.py](chat.py) "
                 "loads the expanded run's full `model.pt` and vocabulary. It is a tiny "
                 "continuation model, not an instruction-trained assistant. Every prompt starts "
                 "fresh, with a 48-token context. It reports unknown words and truncation; it "
                 "does not update weights or put chats into the corpus.\n")
    parts.append(f"Run: `{runs['expanded']}`. Model-state SHA-256: `{chat['model_sha256']}`.\n")
    parts.append(table(["Purpose", "Actual prompt", "Actual reply", "Unknown prompt words", "Seed"],
                       [[purpose,t["prompt"],t["response"] or "[empty response]",", ".join(t["unknown_prompt_words"]) or "none",t["seed"]]
                        for purpose,t in zip(["Familiar", "Extension-related", "Limitation"],chat["turns"])]))
    parts.append("The familiar prompt yields a purchase-template continuation. The extension "
                 "prompt contains unknown `gate` and `closed` and produces an incoherent "
                 "response. The quantum prompt contains two unknown words and receives "
                 "irrelevant classroom text. None of these replies is replaced by a canned answer.\n\n"
                 "[Native transcript](evidence/current-chat/transcript.json) · "
                 "[Actual terminal output](evidence/current-chat/terminal.txt) · "
                 "[Asciinema v2 recording](evidence/current-chat/terminal.cast) · "
                 "[Offline playback page](evidence/current-chat/playback.html) · "
                 "[Recording verification](evidence/current-chat/verification.json)\n\n"
                 "The recording captures real PTY output and echoed input with timestamps. "
                 "The helper enters three prompts into the running interface; it does not "
                 "construct replies. To watch, download/open `playback.html` in a browser and "
                 "press Play. It is self-contained and needs no network. The `.cast` is also "
                 "usable in an asciinema player. This is a recording, not a simulated screenshot. "
                 "It is stored separately from the notebook's complete results ZIP.\n")
    parts.append("## Runtime and complete artifact links\n\nMeasured locally on "
                 f"`{config['starter']['hardware']}`, Python 3.13.15, PyTorch 2.14.0, NumPy 2.5.3. "
                 "CPU was explicitly selected; no pretrained weights or external model API "
                 "were used. Training times below include milestone panel/sample checks, "
                 "but exclude separate before/after language eval cells. They are measurements "
                 "of these runs, not a runtime guarantee for another machine.\n")
    runtime_rows=[]
    for label,path in runs.items():
        t=read(path / 'training_summary.json')
        runtime_rows.append([label,t['completed_steps'],config[label]['parameters'],repr(t['elapsed_seconds']),t['interrupted']])
    parts.append(table(['Run','Completed steps','Parameters','Training-loop seconds','Interrupted'],runtime_rows))
    parts.append("The [separate 10-step setup notebook](evidence/setup/custom_llm_10_steps.ipynb) "
                 "completed before either main run and is not included in the four-row results. "
                 "A first setup attempt could not start its kernel inside the sandbox; no cells "
                 "trained in that attempt. The successful rerun used local loopback kernel access. "
                 "[Setup test log](evidence/setup/tests.txt) records all 14 supplied tests passing.\n")
    for label,path in runs.items():
        parts.append(f"**{label.title()}:** " + " · ".join([
            link(experiments[label]['notebook'],'executed notebook'),link(path,'complete run folder'),link(str(path)+'.zip','complete ZIP')]+[
            link(path/file,title) for file,title in [('config.json','config'),('training_summary.json','training summary'),
            ('training.csv','loss CSV'),('history.json','loss JSON'),('tokenization.json','tokens and IDs'),
            ('inspection.json','vectors, probabilities and update'),('temperature_comparison.json','temperatures'),
            ('corpus_manifest.json','corpus manifest'),('vocabulary_report.json','vocabulary'),('split.json','split and panels'),
            ('eval_separation.json','separation'),('corpus.txt','training-source text before split'),
            ('model.pt','trained weights'),('model_untrained.pt','untrained weights'),('checkpoint.json','viewer embeddings')]])+'\n')
    parts.append("The ZIPs and executed notebooks are separate files; both complete ZIPs are "
                 "retained locally and published. `checkpoint.json` is for the embedding viewer; "
                 "`model.pt` is the inference network. Neither contains all optimizer/random "
                 "state for exact training resume. Notebook FileLink outputs retain real local "
                 "paths; use this README's repository links when browsing on GitHub.\n")
    parts.append("## Reproduce the notebook, evaluation and chat\n\nRun from the repository root. "
                 "The input notebooks differ from the preserved upstream notebook only in "
                 "experiment settings and the recorded prediction. The runner explicitly uses "
                 "the current Python interpreter for its kernel, saves real outputs after each "
                 "cell, and rejects an existing output notebook. Each training run also creates "
                 "a new timestamped run folder and ZIP.\n\n```sh\n"
                 "python3 -m venv .venv\n"
                 ".venv/bin/python -m pip install -r requirements-local.txt\n"
                 ".venv/bin/python -m unittest test_language_evals test_corpus\n"
                 ".venv/bin/python scripts/execute_notebook.py notebooks/setup.ipynb --output results/new-setup.ipynb\n"
                 ".venv/bin/python scripts/execute_notebook.py notebooks/starter.ipynb --output results/new-starter.ipynb\n"
                 ".venv/bin/python scripts/execute_notebook.py notebooks/expanded.ipynb --output results/new-expanded.ipynb\n```\n\n"
                 "The [complete environment lock](requirements-lock.txt) records the exact installed "
                 "versions. `requirements-local.txt` adds NumPy because the supplied scorer uses "
                 "`tensor.numpy()`, plus notebook execution tooling. The original requirements remain intact.\n")
    parts.append('```sh\n'+ '\n'.join(
        f'.venv/bin/python run_evals.py --model {path}/{filename} --stage {stage} --output results/new-{label}-{stage}'
        for label,path in runs.items() for stage,filename in [('untrained','model_untrained.pt'),('final','model.pt')])+'\n'+
        f'.venv/bin/python chat.py --model {runs["expanded"]}/model.pt --transcript results/my-chat.json\n```\n')
    parts.append("Enter a prompt and press Enter; `/quit` saves the transcript and exits. Use a "
                 "new transcript filename and new evaluation output directories. All four "
                 "saved-model commands were exercised in [separate rerun folders](evidence/current-reruns/); "
                 "every saved case, probability, score and continuation exactly matches its "
                 "original notebook result. [Rerun verification](evidence/current-reruns/verification.json).\n")
    parts.append(f"```sh\n.venv/bin/python scripts/verify_artifacts.py --starter-run {runs['starter']} "
                 f"--expanded-run {runs['expanded']} --starter-notebook custom_llm.ipynb "
                 "--expanded-notebook custom_llm_expanded.ipynb "
                 "--starter-rerun evidence/current-reruns/starter/final "
                 "--expanded-rerun evidence/current-reruns/expanded/final\n```\n")
    parts.append("This verifier confirms all 192 case records, CSV/JSON consistency, untouched "
                 "fixed sources, the seeded training-only vocabularies and splits, saved initial "
                 "and trained models, both executed notebooks, and complete ZIP contents. "
                 "The [source provenance](provenance.json) identifies starter revision "
                 "`9e04ddb6aacb8efcb790e70c62550ca55e0f2a75` and the pinned nanoGPT revision "
                 "`3adf61e154c3fe3fca428ad6bc3818b27a3b8291`. "
                 "[Original README](STARTER_README.md) · [nanoGPT license](NANOGPT_LICENSE) · "
                 "[Unchanged 48-case suite](evals/language_evals.json) · [Unchanged runner](run_evals.py).\n")
    parts.append("## Limitation and next experiment\n\nThe model learns repeated classroom "
                 "patterns much better than unfamiliar tasks. More known words do not guarantee "
                 "correct relationships, as both newly scorable opposites failures demonstrate. "
                 "The tiny loss panels mostly represent the original classroom text. One seed "
                 "and changing splits/vocabularies limit causal conclusions.\n\n"
                 "A next experiment would add a more substantial, independently written set "
                 "of varied relational and negation lessons, inspect vocabulary coverage from "
                 "training material, and evaluate the added skills with balanced panels and "
                 "multiple seeds. Keep these public tests as development tests and create an "
                 "additional untouched holdout before further tuning. More steps alone cannot "
                 "add missing vocabulary. No minimum score is required; completeness and honest "
                 "interpretation matter more than reporting only successes.\n")
    (ROOT/'README.md').write_text('\n\n'.join(parts).rstrip()+'\n')
    (ROOT/'docs/temperature-samples.md').write_text('\n'.join(temp_doc))
    review=['# Complete current evaluation review\n\nAll 48 unchanged cases at all four stages. Empty strings remain explicit. The scoring key is evidence only and never training data.\n']
    for (label,stage),rows in results.items():
        review.append(f'## {label} / {stage}\n')
        for r in rows:
            review.append(f"### {r['id']} — {r['category']}\n\nPrompt: `{r['prompt']}`\n\n"
                          f"Status: **{r['status']}**; score **{r['score']}**; selected **{r['predicted_choice']}**; expected **{r['expected']}**.\n\n"
                          f"Unknown prompt words: {', '.join(r['unknown_prompt_words']) or 'none'}. "
                          f"Unknown choices: {', '.join(r['unknown_choices']) or 'none'}.\n\n"
                          f"Actual continuation (seed {r['sample_seed']}):\n\n```text\n{r['generated_text'] or '[empty response]'}\n```\n")
    (ROOT/'docs/all-evals.md').write_text('\n'.join(review))
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(comparison[0]));writer.writeheader();writer.writerows(comparison)
    (ROOT/'evidence/current-comparison.csv').write_text(stream.getvalue())
    print('Built README, all-case review, temperature samples, and comparison CSV from current measured evidence.')


if __name__ == '__main__':
    main()
