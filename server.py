#!/usr/bin/env python3
import sys, os, subprocess, json, http.server, urllib.parse, time

PORT = 8080
DIR  = os.path.dirname(os.path.abspath(__file__))

print(f"\n  Song Analyzer")
print(f"  Python: {sys.version.split()[0]}")
print(f"  Folder: {DIR}")
print()

# ── Auto-install dependencies ────────────────────────────────
def pip_install(pkg):
    print(f"  Installing {pkg}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"], timeout=120)

try:
    import youtube_transcript_api as _y
except ImportError:
    pip_install("youtube-transcript-api")
    import youtube_transcript_api as _y

# youtube-transcript-api v1.x uses instance + cookies
from youtube_transcript_api import YouTubeTranscriptApi

# ── Cookie file (optional) ───────────────────────────────────
# Export cookies from your browser using extension "Get cookies.txt LOCALLY"
# Save as cookies.txt in the same folder as server.py
COOKIES_FILE = os.path.join(DIR, "cookies.txt")

def make_api():
    """Create API instance, with cookies if available."""
    if os.path.exists(COOKIES_FILE):
        print(f"  Using cookies: {COOKIES_FILE}")
        try:
            return YouTubeTranscriptApi(cookie_path=COOKIES_FILE)
        except TypeError:
            # older signature
            try:
                return YouTubeTranscriptApi(cookies=COOKIES_FILE)
            except:
                pass
    return YouTubeTranscriptApi()

def get_transcript(vid):
    errors = []

    # Style 1: instance .fetch(vid) — v1.x
    try:
        api = make_api()
        result = api.fetch(vid)
        segs = _to_segs(result)
        if segs:
            print(f"  OK Style1: {len(segs)} segments")
            return segs, "en"
    except Exception as e:
        errors.append(f"Style1: {e}")

    # Style 2: instance .list(vid) → pick transcript → .fetch()
    try:
        api = make_api()
        tlist = api.list(vid)
        t = _pick_english(list(tlist))
        fetched = t.fetch()
        segs = _to_segs(fetched)
        if segs:
            lc = getattr(t, 'language_code', 'en')
            print(f"  OK Style2: {len(segs)} segments, lang={lc}")
            return segs, lc
    except Exception as e:
        errors.append(f"Style2: {e}")

    raise RuntimeError(" | ".join(errors))


def _to_segs(data):
    segs = []
    for s in data:
        if isinstance(s, dict):
            segs.append({"start": round(float(s.get('start',0)),2),
                         "dur":   round(float(s.get('duration',2)),2),
                         "text":  str(s.get('text',''))})
        else:
            segs.append({"start": round(float(getattr(s,'start',0)),2),
                         "dur":   round(float(getattr(s,'duration',2)),2),
                         "text":  str(getattr(s,'text',str(s)))})
    return segs

def _pick_english(items):
    for t in items:
        lc = getattr(t,'language_code','')
        if lc.startswith('en') and not getattr(t,'is_generated',True):
            return t
    for t in items:
        if getattr(t,'language_code','').startswith('en'):
            return t
    return items[0]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)

    def log_message(self, fmt, *args):
        pass  # silence request logs

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/test":
            self._json(200, {"status": "ok"})
            return

        if parsed.path == "/subtitles":
            qs  = urllib.parse.parse_qs(parsed.query)
            vid = (qs.get("v") or [""])[0].strip()
            print(f"  Fetching subtitles: {vid}")
            if not vid:
                self._json(400, {"error": "Missing ?v=VIDEO_ID"})
                return
            try:
                segs, lang = get_transcript(vid)
                self._json(200, {"segments": segs, "lang": lang, "count": len(segs)})
            except Exception as e:
                print(f"  ERROR: {e}")
                self._json(404, {"error": str(e)})
            return

        super().do_GET()

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header("Content-Type",   "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


if not os.path.exists(COOKIES_FILE):
    print("  TIP: To fix YouTube blocking, export cookies from Chrome/Firefox")
    print("  using extension 'Get cookies.txt LOCALLY', save as cookies.txt")
    print("  in the same folder as server.py")
    print()

print(f"  Running at: http://localhost:{PORT}/lyrics-translator.html")
print(f"  Press Ctrl+C to stop.\n")

try:
    http.server.HTTPServer(("", PORT), Handler).serve_forever()
except KeyboardInterrupt:
    print("\n  Stopped.")
except OSError:
    print(f"\n  ERROR: Port {PORT} is busy. Close other server and try again.")
    input("  Press Enter...")
