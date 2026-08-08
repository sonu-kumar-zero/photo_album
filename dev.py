from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


PROJECT_ROOT = Path(__file__).parent
ENTRY_POINT = PROJECT_ROOT / "main.py"

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}


class ReloadHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.process: subprocess.Popen[bytes] | None = None
        self.last_restart = 0.0
        self.restart()

    def should_reload(self, path: str) -> bool:
        file_path = Path(path)

        if file_path.suffix != ".py":
            return False

        if any(part in IGNORED_DIRECTORIES for part in file_path.parts):
            return False

        return True

    def restart(self) -> None:
        now = time.monotonic()

        # Prevent multiple restart events from firing immediately.
        if now - self.last_restart < 0.5:
            return

        self.last_restart = now

        if self.process is not None:
            print("Stopping application...")
            self.process.terminate()

            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        print("Starting application...")

        self.process = subprocess.Popen(
            [sys.executable, str(ENTRY_POINT)],
            cwd=PROJECT_ROOT,
        )

    def on_modified(self, event) -> None:
        if event.is_directory:
            return

        if self.should_reload(event.src_path):
            print(f"\nChanged: {event.src_path}")
            self.restart()

    def on_created(self, event) -> None:
        if event.is_directory:
            return

        if self.should_reload(event.src_path):
            print(f"\nCreated: {event.src_path}")
            self.restart()

    def on_deleted(self, event) -> None:
        if event.is_directory:
            return

        if self.should_reload(event.src_path):
            print(f"\nDeleted: {event.src_path}")
            self.restart()


def main() -> None:
    handler = ReloadHandler()

    observer = Observer()
    observer.schedule(
        handler,
        str(PROJECT_ROOT),
        recursive=True,
    )

    observer.start()

    print("================================")
    print(" Photo Gallery Development Mode")
    print("================================")
    print("Watching Python files...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        observer.stop()

        if handler.process is not None:
            handler.process.terminate()

            try:
                handler.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                handler.process.kill()

        observer.join()


if __name__ == "__main__":
    main()