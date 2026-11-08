# -*- coding: utf-8 -*-
import os, sys, time, threading, http.server, webbrowser
from pathlib import Path

APP_TITLE = "听力刷题 · 连做版"


def base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


HTML = (Path(base_dir()) / "index.html").read_bytes()


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        # 只接受本机 Host，挡住 DNS rebinding 类的跨站读取
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]").lower()
        if host not in ("127.0.0.1", "localhost"):
            self.send_error(403)
            return
        if self.path.startswith("/favicon"):
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(HTML)

    def log_message(self, *args):
        pass


def start_server():
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port


def work_area():
    """返回桌面可用区域（逻辑像素），失败时退回 1280x800。"""
    try:
        import ctypes
        from ctypes import wintypes
        r = wintypes.RECT()
        if ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(r), 0):
            return r.right - r.left, r.bottom - r.top
    except Exception:
        pass
    return 1280, 800


def main():
    url = "http://127.0.0.1:%d/" % start_server()
    sw, sh = work_area()
    win_w = min(470, max(360, sw - 60))
    win_h = min(880, max(540, sh - 80))
    try:
        import webview
        webview.create_window(
            APP_TITLE, url,
            width=win_w, height=win_h,
            min_size=(360, 520),
            background_color="#F6F3EC",
            text_select=True,
        )
        webview.start()
    except Exception:
        webbrowser.open(url)
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()
