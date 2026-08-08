
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart()
        
    def restart(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            
        self.process = subprocess.Popen(['python', 'main.py'])
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Restarting...")
            self.restart()
        
handler = RestartHandler()

observer = Observer()
observer.schedule(handler, path='.', recursive=True)
observer.start()

try: 
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    if handler.process:
        handler.process.terminate()
        handler.process.wait()

observer.join()    
    