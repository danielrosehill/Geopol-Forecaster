"""Minimal stdlib web UI for running geopol forecasts and streaming logs.

Run:  uv run python scripts/webui.py
Open: http://localhost:8765
"""
from __future__ import annotations

import os
import shlex
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8765

PAGE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Geopol Forecaster</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }
  textarea { width: 100%; height: 140px; font: 14px/1.4 ui-monospace, monospace; }
  button { padding: .6rem 1.2rem; font-size: 1rem; cursor: pointer; }
  button:disabled { opacity: .5; cursor: not-allowed; }
  label { display: flex; gap: .5rem; align-items: center; margin: .5rem 0; }
  pre { background: #0b0b0b; color: #c8f0c8; padding: 1rem; border-radius: 6px;
        height: 520px; overflow: auto; white-space: pre-wrap; font: 12px/1.4 ui-monospace, monospace; }
  .row { display: flex; gap: 1rem; align-items: center; margin: .5rem 0; }
</style>
</head>
<body>
<h1>Geopol Forecaster</h1>
<form id="f">
  <label>Prompt<br>
    <textarea id="q" placeholder="Enter forecast question..."></textarea>
  </label>
  <div class="row">
    <label><input type="checkbox" id="skip_pdf"> skip PDF</label>
    <button id="go" type="submit">Run forecast</button>
    <span id="status"></span>
  </div>
</form>
<h3>Log</h3>
<pre id="log"></pre>

<script>
const f = document.getElementById('f');
const log = document.getElementById('log');
const go = document.getElementById('go');
const status = document.getElementById('status');

f.addEventListener('submit', async (e) => {
  e.preventDefault();
  log.textContent = '';
  go.disabled = true;
  status.textContent = 'running...';
  const body = new URLSearchParams({
    question: document.getElementById('q').value,
    skip_pdf: document.getElementById('skip_pdf').checked ? '1' : '',
  });
  try {
    const res = await fetch('/run', { method: 'POST', body });
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      log.textContent += dec.decode(value, { stream: true });
      log.scrollTop = log.scrollHeight;
    }
    status.textContent = 'done';
  } catch (err) {
    status.textContent = 'error: ' + err;
  } finally {
    go.disabled = false;
  }
});
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quiet
        pass

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/run":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode()
        from urllib.parse import parse_qs

        form = parse_qs(raw)
        question = (form.get("question") or [""])[0].strip()
        skip_pdf = bool((form.get("skip_pdf") or [""])[0])
        if not question:
            self.send_error(400, "missing question")
            return

        cmd = ["uv", "run", "geopol", "forecast", question]
        if skip_pdf:
            cmd.append("--skip-pdf")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        def chunk(data: bytes) -> None:
            self.wfile.write(f"{len(data):X}\r\n".encode() + data + b"\r\n")
            self.wfile.flush()

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        chunk(f"$ {' '.join(shlex.quote(c) for c in cmd)}\n\n".encode())
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                text=True,
                env=env,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                chunk(line.encode("utf-8", "replace"))
            proc.wait()
            chunk(f"\n[exit {proc.returncode}]\n".encode())
        except Exception as e:
            chunk(f"[webui error] {e}\n".encode())
        finally:
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()


def main() -> None:
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Geopol web UI on http://localhost:{PORT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
