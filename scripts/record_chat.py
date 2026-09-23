"""Record three real chat.py interactions in a PTY, with offline playback.

Run with the project .venv. The supplied chat.py writes its own transcript;
this helper never substitutes generated text for terminal output or modifies
the transcript. Evidence must be saved outside corpus/ in a new directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import time

import pexpect

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = [
    "the customer",
    "at the station the gate is not closed but",
    "explain quantum teleportation",
]


class Recording:
    """Write only observed PTY output and actual sent input, with real timing."""

    def __init__(self, output_dir, header):
        self.started = time.monotonic()
        self.events = []
        self.cast = (output_dir / "terminal.cast").open("x", encoding="utf-8")
        self.output = (output_dir / "terminal.txt").open("x", encoding="utf-8")
        self.cast.write(json.dumps(header) + "\n")
        self.cast.flush()

    def event(self, kind, data):
        event = [round(time.monotonic() - self.started, 6), kind, data]
        self.events.append(event)
        self.cast.write(json.dumps(event, ensure_ascii=False) + "\n")
        self.cast.flush()

    def write(self, data):
        # pexpect logfile_read calls this only for text read from the PTY.
        self.event("o", data)
        self.output.write(data)
        self.output.flush()

    def flush(self):
        self.cast.flush()
        self.output.flush()

    def close(self):
        self.cast.close()
        self.output.close()


def write_player(path, header, events):
    # Escape HTML-sensitive characters inside JSON to keep the offline player
    # safe even when a future model emits text containing a script end tag.
    payload = json.dumps({"header": header, "events": events}, ensure_ascii=False)
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Expanded nanoGPT — real terminal recording</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#10151b;color:#e5eef5}
body{margin:0 auto;padding:28px;max-width:1100px}h1{font-size:1.5rem;margin:0 0 10px}
p{line-height:1.5;color:#b6c5d0}button{font:inherit;padding:8px 16px;border:1px solid
#6b8599;border-radius:6px;background:#1c2a35;color:inherit;cursor:pointer}
button:focus-visible{outline:3px solid #88dbb5;outline-offset:3px}
.controls{display:flex;align-items:center;gap:12px;margin:20px 0}#time{font-variant-numeric:tabular-nums}
pre{padding:20px;background:#03090e;border:1px solid #405362;border-radius:8px;
min-height:28em;white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 ui-monospace,
SFMono-Regular,Consolas,monospace;color:#b7f5cb}a{color:#8dddc1}code{overflow-wrap:anywhere}
</style></head><body>
<h1>Expanded nanoGPT: real terminal recording</h1>
<p>Actual <code>chat.py</code> output and input echo captured from a pseudoterminal.
Playback uses the original event timing. This is a recording, not a screenshot.
No network connection is needed.</p>
<p id="metadata"></p><div class="controls">
<button id="play" type="button">Play</button><button id="restart" type="button">Restart</button>
<span id="time">0.0 s</span></div>
<pre id="terminal" aria-label="Recorded terminal output" tabindex="0"></pre>
<p><a href="terminal.cast">Original asciinema v2 recording</a> ·
<a href="terminal.txt">Plain terminal output</a> ·
<a href="transcript.json">Native chat transcript</a> ·
<a href="verification.json">Run and model verification</a></p>
<script id="recording" type="application/json">__PAYLOAD__</script>
<script>
"use strict";
const recording=JSON.parse(document.getElementById('recording').textContent);
const events=recording.events.filter(event=>event[1]==='o');
const duration=recording.events.length?recording.events[recording.events.length-1][0]:0;
const terminal=document.getElementById('terminal'),play=document.getElementById('play');
const clock=document.getElementById('time');
document.getElementById('metadata').textContent=
  new Date(recording.header.timestamp*1000).toISOString()+' · '+recording.header.command;
let position=0,index=0,running=false,base=0,frame=null;
function draw(){
  while(index<events.length && events[index][0]<=position){
    // chat.py emits plain lines. Preserve its text; CRLF is a single newline.
    terminal.textContent+=events[index++][2].replace(/\\r\\n/g,'\\n').replace(/\\r/g,'');
  }
  clock.textContent=position.toFixed(1)+' / '+duration.toFixed(1)+' s';
}
function tick(now){
  position=Math.min(duration,(now-base)/1000);draw();
  if(position>=duration){running=false;play.textContent='Replay';frame=null;return;}
  frame=requestAnimationFrame(tick);
}
function pause(){running=false;cancelAnimationFrame(frame);frame=null;play.textContent='Play';}
function reset(){pause();position=0;index=0;terminal.textContent='';draw();}
function start(){
  if(position>=duration)reset();running=true;play.textContent='Pause';
  base=performance.now()-position*1000;frame=requestAnimationFrame(tick);
}
play.addEventListener('click',()=>running?pause():start());
document.getElementById('restart').addEventListener('click',()=>{reset();start();});
draw();
</script></body></html>
"""
    path.write_text(page.replace("__PAYLOAD__", payload), encoding="utf-8")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    model_path = args.model.resolve()
    output_dir = args.output_dir.resolve()
    if not model_path.is_file():
        parser.error("--model must be an existing saved model file.")
    if output_dir == ROOT / "corpus" or ROOT / "corpus" in output_dir.parents:
        parser.error("Save chat evidence outside corpus/.")
    if output_dir.exists():
        parser.error("Choose a new --output-dir to preserve earlier recordings.")

    transcript_path = output_dir / "transcript.json"
    command = [sys.executable, "-u", "chat.py", "--model", str(model_path),
               "--transcript", str(transcript_path)]
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "4"
    env["TERM"] = "xterm-256color"
    header = {"version": 2, "width": 100, "height": 32,
              "timestamp": int(time.time()),
              "title": "Expanded nanoGPT — real chat.py PTY recording",
              "command": shlex.join(command),
              "env": {"TERM": env["TERM"], "OMP_NUM_THREADS": env["OMP_NUM_THREADS"]}}
    output_dir.mkdir(parents=True, exist_ok=False)
    recording = Recording(output_dir, header)
    child = None
    try:
        child = pexpect.spawn(command[0], command[1:], cwd=str(ROOT), env=env,
                              encoding="utf-8", timeout=180, echo=True,
                              dimensions=(header["height"], header["width"]))
        child.logfile_read = recording
        for prompt in PROMPTS:
            child.expect_exact("You: ")
            recording.event("i", prompt + "\n")
            child.sendline(prompt)
        child.expect_exact("You: ")
        recording.event("i", "/quit\n")
        child.sendline("/quit")
        child.expect(pexpect.EOF)
        child.close()
        if child.exitstatus != 0:
            raise RuntimeError(f"chat.py exited with status {child.exitstatus}; signal {child.signalstatus}")
    finally:
        if child is not None and child.isalive():
            child.close(force=True)
        recording.close()
        write_player(output_dir / "playback.html", header, recording.events)

    transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
    if [turn["prompt"] for turn in transcript["turns"]] != PROMPTS:
        raise RuntimeError("The native transcript does not contain the three expected turns.")
    # Check the transcript's identity against the actual saved model using the
    # supplied implementation, and keep this check separate from the recording.
    os.environ["OMP_NUM_THREADS"] = "4"
    sys.path.insert(0, str(ROOT))
    from run_evals import load_model, model_hash
    model, _, saved = load_model(model_path)
    identity = model_hash(model)
    if transcript["model_sha256"] != identity:
        raise RuntimeError("Transcript model hash differs from the saved model.")
    if transcript["completed_steps"] != saved.get("completed_steps"):
        raise RuntimeError("Transcript training step count differs from the saved model.")
    verification = {
        "status": "passed", "capture": "actual PTY output and echoed input",
        "native_chat_source_sha256": file_hash(ROOT / "chat.py"),
        "model": str(model_path), "run_directory": str(model_path.parent),
        "model_file_sha256": file_hash(model_path), "model_sha256": identity,
        "completed_steps": saved.get("completed_steps"),
        "turn_count": len(transcript["turns"]), "prompts": PROMPTS,
        "command": command, "cwd": str(ROOT), "OMP_NUM_THREADS": "4",
        "recording_seconds": recording.events[-1][0] if recording.events else 0,
        "event_count": len(recording.events),
        "artifacts_sha256": {name: file_hash(output_dir / name) for name in
                             ["transcript.json", "terminal.cast", "terminal.txt", "playback.html"]},
    }
    (output_dir / "verification.json").write_text(
        json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded and verified {len(transcript['turns'])} turns: {output_dir}")
    print(f"Model SHA-256: {identity}")


if __name__ == "__main__":
    main()
