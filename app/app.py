import os
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

PAGE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>my-app</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0;
           display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
    .card {{ background: #1e293b; padding: 2.5rem 3rem; border-radius: 1rem; min-width: 22rem; }}
    h1 {{ margin: 0 0 1.5rem; font-size: 1.5rem; color: #38bdf8; }}
    dt {{ color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
    dd {{ margin: 0.2rem 0 1.2rem; font-size: 1.3rem; font-family: ui-monospace, monospace; }}
    .version {{ font-size: 3rem; color: #4ade80; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>my-app</h1>
    <dl>
      <dt>version</dt><dd class="version">{version}</dd>
      <dt>pod</dt><dd>{hostname}</dd>
      <dt>password from secret</dt><dd>{password}</dd>
    </dl>
  </div>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = PAGE.format(
            version=os.environ.get("APP_VERSION", "?"),
            hostname=socket.gethostname(),
            password=os.environ.get("APP_PASSWORD", "&lt;not set&gt;"),
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())


HTTPServer(("", 8080), Handler).serve_forever()
