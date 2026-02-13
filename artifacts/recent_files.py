import os
import time
from utils.logger import log

class RecentFilesScanner:
    def __init__(self):
        self.recent_files = []

    def scan_recent(self, days=7):
        """Scans for files modified in the last N days in user directory."""
        user_dir = os.path.expanduser('~')
        cutoff_time = time.time() - (days * 86400)
        
        log.info(f"[bold cyan]Scanning for files modified in the last {days} days in {user_dir}...[/bold cyan]")

        # Limit depth and skip hidden folders for speed/privacy in this artifact check
        for root, dirs, files in os.walk(user_dir):
            # Skip hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                try:
                    full_path = os.path.join(root, file)
                    mtime = os.path.getmtime(full_path)
                    
                    if mtime > cutoff_time:
                        self.recent_files.append({
                            "path": full_path,
                            "modified": mtime
                        })
                except Exception:
                    continue
        
        log.info(f"[bold green]Found {len(self.recent_files)} recent files.[/bold green]")
        return self.recent_files
