"""Serve the bundled lab on loopback only. No third-party Python packages."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

class LabHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Referrer-Policy', 'no-referrer')
        super().end_headers()
    def log_message(self, fmt, *args):
        # Avoid logging query strings that might contain authentication artifacts.
        pass

if __name__ == '__main__':
    os.chdir(Path(__file__).resolve().parent)
    try:
        server=ThreadingHTTPServer(('localhost',3000),LabHandler)
    except OSError:
        raise SystemExit('Port 3000 is unavailable. Stop the other server, then retry. Keep the registered redirect URI unchanged.')
    print('Gotham OIDC Lab: http://localhost:3000/lab.html')
    print('Keep this window open. Stop with Ctrl+C.')
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
