# SPDX-License-Identifier: GPL-2.0-or-later
"""Ravn: the visual Windows launcher. Serves ravn/index.html to Ravn.exe and starts run.py.

Modelled on the Kagekidan launcher of Sakura-Wars-PS4RT-Windows. The game itself is prepared
and started by run.py, exactly as the in-game "Apply and restart" does; this host only keeps
the paths, merges the launcher's graphics choices into ps4rt.ini, and opens a console for the log.
"""
import base64
import json
import os
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent


def port_root():
    """The folder that holds run.py: the package root, or the repository root."""
    for folder in (HERE, *HERE.parents):
        if (folder / "run.py").is_file():
            return folder
    return HERE.parent


ROOT = port_root()
sys.path.insert(0, str(ROOT / "scripts"))
import graphics_options  # noqa: E402  (scripts/ is only on the path from here)
try:
    from trophy_trp import read_trp, read_unlocks, write_card_cache
except ImportError:  # the trophy reader is optional
    read_trp = read_unlocks = write_card_cache = None

PAGE = HERE / "index.html"
BRAND = HERE / "brand"
MEDIA_DIR = HERE / "media"
STATE = ROOT / "launcher-state.json"
LOG = ROOT / "launcher.log"
PORT_FILE = ROOT / "launcher.port"
CONFIG = ROOT / "ps4rt.ini"
LOCK = threading.Lock()
PROCESS = {"handle": None}
TROPHY_CACHE = {"path": "", "stamp": 0.0, "catalog": None}

# ps4rt.ini values (gpu/shim/ps4rt_settings.cpp, ps4rt_graphics.h).
OUTPUTS = ("1920x1080", "2560x1440", "3840x2160")
DISPLAY_MODES = ("windowed", "borderless", "fullscreen")
RENDER_RESOLUTIONS = ("native", "720p", "1440p", "1800p", "4K")
ENGINE_FPS = (60, 120, 240)
ANISOTROPY = (0, 2, 4, 8, 16)
# PS4 system language numbers the runtime returns to the game (PS4RT_LANGUAGE).
GAME_LANGUAGES = {"en": 1, "ja": 0, "fr": 2, "es": 3, "de": 4, "it": 5, "zh-Hant": 10, "ko": 9}

DEFAULT = {
    "settings": {
        "outputRes": "1920x1080",
        "displayMode": "windowed",
        "renderResolution": "native",
        "engineFps": 120,
        "anisotropy": 0,
        "sharpness": 0,
        "musicVolume": 0.55,
        "gameLang": "",
    },
    "paths": {"game": "", "update": ""},
}


def load_state():
    state = json.loads(json.dumps(DEFAULT))
    try:
        saved = json.loads(STATE.read_text(encoding="utf-8"))
        state["settings"].update(saved.get("settings") or {})
        paths = saved.get("paths") or {}
        state["paths"]["game"] = str(paths.get("game") or "")
        state["paths"]["update"] = str(paths.get("update") or "")
    except (OSError, json.JSONDecodeError, AttributeError):
        pass
    # The in-game menu writes the same ps4rt.ini: what it holds now is what the launcher shows.
    state["settings"].update(settings_from_ini(graphics_options.read_ini(CONFIG)))
    return state


def settings_from_ini(ini):
    found = {}
    if ini.get("output_res") in OUTPUTS:
        found["outputRes"] = ini["output_res"]
    if ini.get("display_mode") in DISPLAY_MODES:
        found["displayMode"] = ini["display_mode"]
    if ini.get("render_resolution") in RENDER_RESOLUTIONS:
        found["renderResolution"] = ini["render_resolution"]
    for key, name, allowed in (("engine_fps", "engineFps", ENGINE_FPS), ("anisotropy", "anisotropy", ANISOTROPY)):
        try:
            if int(ini.get(key, "")) in allowed:
                found[name] = int(ini[key])
        except ValueError:
            pass
    try:
        if "sharpen" in ini:
            found["sharpness"] = max(0.0, min(1.0, float(ini.get("sharpness") or 0))) if ini["sharpen"] == "1" else 0
    except ValueError:
        pass
    return found


def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def media_info():
    return {"track": (MEDIA_DIR / "theme.mp3").is_file()}


def pick(value, allowed, default):
    return value if value in allowed else default


def ini_updates(settings):
    """Only the keys the launcher shows. The rest of ps4rt.ini (in-game choices) is kept."""
    try:
        fps = int(settings.get("engineFps") or 120)
    except (TypeError, ValueError):
        fps = 120
    try:
        aniso = int(settings.get("anisotropy") or 0)
    except (TypeError, ValueError):
        aniso = 0
    try:
        sharp = max(0.0, min(1.0, float(settings.get("sharpness") or 0)))
    except (TypeError, ValueError):
        sharp = 0.0
    return {
        "output_res": pick(settings.get("outputRes"), OUTPUTS, "1920x1080"),
        "display_mode": pick(settings.get("displayMode"), DISPLAY_MODES, "windowed"),
        "render_resolution": pick(settings.get("renderResolution"), RENDER_RESOLUTIONS, "native"),
        "engine_fps": str(pick(fps, ENGINE_FPS, 120)),
        "anisotropy": str(pick(aniso, ANISOTROPY, 0)),
        "sharpen": "1" if sharp > 0 else "0",
        "sharpness": "{:.2f}".format(sharp),
    }


def write_ini(settings):
    graphics_options.write_keys(str(CONFIG), ini_updates(settings))


def game_language(settings, available):
    """The chosen language when the game folder offers it, else the first one it offers."""
    chosen = str(settings.get("gameLang") or "")
    if chosen in available:
        return chosen
    return available[0] if available else "en"


def powershell(script):
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-STA", "-Command", script],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    return (completed.stdout or "").strip()


def browse(kind):
    if os.name != "nt":
        raise RuntimeError("picker-unavailable")
    title = {
        "game": "Extracted CUSA06810 folder (eboot.bin, sce_sys)",
        "update": "Extracted update folder (eboot.bin, sce_sys)",
    }.get(kind)
    if not title:
        raise RuntimeError("picker-unavailable")
    script = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$d = New-Object System.Windows.Forms.FolderBrowserDialog; "
        f"$d.Description = '{title}'; "
        "if ($d.ShowDialog() -eq 'OK') { [Console]::Out.Write($d.SelectedPath) }"
    )
    chosen = powershell(script)
    return {kind: chosen} if chosen else {}


def console_python():
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe" and exe.with_name("python.exe").is_file():
        return str(exe.with_name("python.exe"))
    return str(exe)


def trophy_file(game, update=""):
    for folder in (update, game):
        if folder:
            candidate = Path(folder) / "sce_sys" / "trophy" / "trophy00.trp"
            if candidate.is_file():
                return candidate
    return None


def trophy_catalog(trp):
    stamp = trp.stat().st_mtime
    with LOCK:
        if TROPHY_CACHE["path"] != str(trp) or TROPHY_CACHE["stamp"] != stamp:
            TROPHY_CACHE["catalog"] = read_trp(trp)
            TROPHY_CACHE["path"] = str(trp)
            TROPHY_CACHE["stamp"] = stamp
        return TROPHY_CACHE["catalog"]


def available_languages(paths):
    """The game languages this folder can show: those its trophy file carries, in our list."""
    trp = trophy_file(paths.get("game"), paths.get("update")) if read_trp else None
    if not trp:
        return ["en"]
    try:
        codes = [item["id"] for item in trophy_catalog(trp)["languages"]]
    except (OSError, ValueError, KeyError):
        return ["en"]
    return [code for code in codes if code in GAME_LANGUAGES] or ["en"]


def user_dir():
    return ROOT / "user"


def trophy_view(paths):
    if not read_trp:
        raise RuntimeError("missing-trp")
    trp = trophy_file(paths.get("game"), paths.get("update"))
    if not trp:
        raise RuntimeError("missing-trp")
    catalog = trophy_catalog(trp)
    unlocks = read_unlocks(user_dir() / "trophies.json")
    rows = []
    for item in catalog["trophies"]:
        trophy_id = str(item["id"]).zfill(3)
        unlocked = unlocks.get(trophy_id, "")
        icon = ""
        if item["icon"] and (not item["hidden"] or unlocked):
            icon = "data:image/png;base64," + base64.b64encode(item["icon"]).decode("ascii")
        rows.append({"id": trophy_id, "grade": item["grade"], "hidden": item["hidden"],
                     "icon": icon, "text": item["text"], "when": unlocked})
    rows.sort(key=lambda row: (bool(row["when"]), row["when"]), reverse=True)
    return {"languages": catalog["languages"], "trophies": rows}


def launch(state):
    game = str(state["paths"].get("game") or "").strip()
    if not game:
        raise RuntimeError("need-game")
    if not (Path(game) / "eboot.bin").is_file():
        raise RuntimeError("missing-game")
    update = str(state["paths"].get("update") or "").strip()
    # The game folder entered again as its own update means no update.
    if update and os.path.normcase(os.path.realpath(update)) == os.path.normcase(os.path.realpath(game)):
        update = ""
    if update and not (Path(update) / "eboot.bin").is_file():
        raise RuntimeError("missing-update")
    if PROCESS["handle"] is not None and PROCESS["handle"].poll() is None:
        raise RuntimeError("already-running")
    write_ini(state["settings"])
    save_state(state)
    env = dict(os.environ)
    env["PS4RT_GAME_DIR"] = game
    env.pop("PS4RT_PATCH_DIR", None)
    if update:
        env["PS4RT_PATCH_DIR"] = update
    env["PS4RT_DATA_DIR"] = str(ROOT)
    env["PS4RT_CONFIG"] = str(CONFIG)
    # Temporal upscaling is not calibrated for this game (run.py); it stays off here.
    env["PS4RT_EXPERIMENTAL_UPSCALER"] = "0"
    lang = game_language(state["settings"], available_languages(state["paths"]))
    env["PS4RT_LANGUAGE"] = str(GAME_LANGUAGES.get(lang, 1))
    env["PS4RT_TROPHY_LANG"] = lang
    env["PS4RT_TROPHY_FILE"] = str(user_dir() / "trophies.json")
    trp = trophy_file(game, update)
    if trp and write_card_cache:
        # The in-game card reads its names and icons from this local cache, in the chosen language.
        try:
            card_dir = user_dir() / "trophy-card"
            write_card_cache(trp, card_dir, lang)
            env["PS4RT_TROPHY_CARD_DIR"] = str(card_dir)
        except (OSError, ValueError, KeyError):
            pass
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    command = [console_python(), str(ROOT / "run.py")]
    bat = ROOT / "ravn-play.bat"
    quoted = " ".join('"' + str(part).replace('"', '""') + '"' for part in command)
    bat.write_text(
        "@echo off\r\n"
        "cd /d \"%~dp0\"\r\n"
        "title Ravn\r\n"
        f"{quoted}\r\n"
        "echo.\r\n"
        "echo Exit code %ERRORLEVEL%\r\n"
        "pause\r\n",
        encoding="ascii", errors="replace",
    )
    with LOG.open("ab") as log:
        log.write(b"\n--- play ---\n")
    flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    PROCESS["handle"] = subprocess.Popen(["cmd.exe", "/c", str(bat)], cwd=str(ROOT), env=env, creationflags=flags)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def send_json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, file, kind, cache=True):
        body = file.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        if not cache:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > 1_000_000:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self.send_file(PAGE, "text/html; charset=utf-8", cache=False)
            return
        if path.startswith("/brand/"):
            name = path.rsplit("/", 1)[-1]
            kind = {"fond-loop.mp4": "video/mp4", "logo.png": "image/png"}.get(name)
            if kind and (BRAND / name).is_file():
                self.send_file(BRAND / name, kind)
                return
        if path == "/media/theme.mp3" and (MEDIA_DIR / "theme.mp3").is_file():
            self.send_file(MEDIA_DIR / "theme.mp3", "audio/mpeg")
            return
        if path == "/api/state":
            state = load_state()
            state["media"] = media_info()
            state["languages"] = available_languages(state["paths"])
            self.send_json(200, state)
            return
        if path == "/api/trophies":
            state = load_state()
            try:
                self.send_json(200, trophy_view(state["paths"]))
            except (OSError, RuntimeError, ValueError, KeyError) as error:
                self.send_json(404, {"error": str(error) or "missing-trp"})
            return
        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self.read_json()
            with LOCK:
                if path == "/api/state":
                    state = load_state()
                    if isinstance(payload.get("settings"), dict):
                        state["settings"].update(payload["settings"])
                    if isinstance(payload.get("paths"), dict):
                        state["paths"].update(payload["paths"])
                    save_state(state)
                    self.send_json(200, state)
                    return
                if path == "/api/browse":
                    found = browse(str(payload.get("kind") or ""))
                    state = load_state()
                    state["paths"].update(found)
                    save_state(state)
                    self.send_json(200, {**state["paths"], "languages": available_languages(state["paths"])})
                    return
            if path == "/api/play":
                with LOCK:
                    state = load_state()
                    if isinstance(payload.get("settings"), dict):
                        state["settings"].update(payload["settings"])
                    if isinstance(payload.get("paths"), dict):
                        state["paths"].update(payload["paths"])
                launch(state)
                self.send_json(200, {"ok": True})
                return
        except Exception as error:
            self.send_json(400, {"error": str(error)})
            return
        self.send_error(404)


def serve(open_page=True):
    if PORT_FILE.is_file():
        try:
            existing = int(PORT_FILE.read_text(encoding="utf-8").strip())
            import urllib.request
            with urllib.request.urlopen(f"http://127.0.0.1:{existing}/api/state", timeout=0.4) as response:
                if response.status == 200:
                    if open_page:
                        open_browser(existing)
                    return
        except (OSError, ValueError):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    PORT_FILE.write_text(str(port), encoding="utf-8")
    if open_page:
        threading.Timer(0.4, open_browser, args=(port,)).start()
    try:
        server.serve_forever()
    finally:
        try:
            PORT_FILE.unlink()
        except OSError:
            pass


def open_browser(port):
    url = f"http://127.0.0.1:{port}/"
    try:
        if os.name == "nt":
            os.startfile(url)
            return
        webbrowser.open(url)
    except OSError:
        return


if __name__ == "__main__":
    try:
        serve(open_page="--no-browser" not in sys.argv)
    except Exception as error:
        (ROOT / "launcher-error.txt").write_text(str(error), encoding="utf-8")
        raise
