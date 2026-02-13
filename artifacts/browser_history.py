import os
import sqlite3
import shutil
from utils.logger import log

class BrowserHistoryExtractor:
    def __init__(self):
        self.history_data = []

    def get_chrome_history(self):
        """Extracts Chrome history."""
        # Windows path for Chrome User Data
        history_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"
        if not os.path.exists(history_path):
            log.warning("Chrome history file not found.")
            return

        # Copy to temp location to avoid lock
        temp_path = "temp_chrome_history"
        try:
            shutil.copy2(history_path, temp_path)
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
            
            for row in cursor.fetchall():
                self.history_data.append({
                    "browser": "Chrome",
                    "url": row[0],
                    "title": row[1],
                    "timestamp": row[2]
                })
            
            conn.close()
            os.remove(temp_path)
            log.info(f"[bold green]Parsed Chrome history ({len(self.history_data)} entries).[/bold green]")
        except Exception as e:
            log.error(f"Failed to extract Chrome history: {e}")

    def get_firefox_history(self):
        # Placeholder for Firefox - logic is similar but different path/query
        pass

    def get_all_history(self):
        self.get_chrome_history()
        return self.history_data
