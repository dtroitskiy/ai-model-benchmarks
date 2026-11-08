"""Graceful stop: finish the attempts already running, start no new ones.

Two triggers:
  * press `Q` in the terminal running the benchmark (press again to cancel the request);
  * run `bench stop <name>` from any other terminal, which creates a STOP file in the run folder.
Ctrl+C still aborts immediately.
"""
from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

STOP_FILE = "STOP"


class StopControl:
    def __init__(self, run_path: Path):
        self.stop_file = run_path / STOP_FILE
        self._event = threading.Event()
        self._done = threading.Event()
        self._thread: threading.Thread | None = None
        self._restore = None

    # ------------------------------------------------------------------ public
    @property
    def requested(self) -> bool:
        if not self._event.is_set() and self.stop_file.exists():
            self._event.set()
            print("\n>>> Stop requested via 'bench stop': finishing current attempt(s), "
                  "then stopping.", flush=True)
        return self._event.is_set()

    def __enter__(self) -> "StopControl":
        self.stop_file.unlink(missing_ok=True)  # stale request from an earlier session
        if sys.stdin is not None and sys.stdin.isatty():
            self._thread = threading.Thread(target=self._watch_keys, daemon=True)
            self._thread.start()
            print("(press Q to stop after the current attempt(s); Ctrl+C aborts immediately)",
                  flush=True)
        else:
            print("(run 'bench stop <name>' to stop after the current attempt(s))", flush=True)
        return self

    def __exit__(self, *exc) -> None:
        self._done.set()
        if self._thread:
            self._thread.join(timeout=1)
        if self._restore:
            self._restore()
        self.stop_file.unlink(missing_ok=True)

    # ------------------------------------------------------------------ keys
    def _toggle(self) -> None:
        if self._event.is_set():
            self._event.clear()
            self.stop_file.unlink(missing_ok=True)
            print("\n>>> Stop cancelled, continuing.", flush=True)
        else:
            self._event.set()
            print("\n>>> Stop requested: finishing current attempt(s), then stopping. "
                  "Press Q again to cancel.", flush=True)

    def _watch_keys(self) -> None:
        try:
            if sys.platform == "win32":
                import msvcrt
                while not self._done.is_set():
                    if msvcrt.kbhit():
                        if msvcrt.getwch().lower() == "q":
                            self._toggle()
                    else:
                        time.sleep(0.1)
            else:
                import select
                import termios
                import tty
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                tty.setcbreak(fd)
                self._restore = lambda: termios.tcsetattr(fd, termios.TCSADRAIN, old)
                while not self._done.is_set():
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        if sys.stdin.read(1).lower() == "q":
                            self._toggle()
        except Exception as e:  # never let the key watcher break a benchmark
            print(f"(key watcher disabled: {e}; use 'bench stop <name>' instead)", flush=True)
