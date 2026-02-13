import json
from datetime import datetime
from utils.logger import log

class TimelineGenerator:
    def __init__(self, file_list):
        self.file_list = file_list
        self.timeline = []

    def build(self):
        """Generates a chronological timeline of file events."""
        log.info("[bold cyan]Building timeline...[/bold cyan]")
        
        for file in self.file_list:
            self.timeline.append({
                "timestamp": file["created"],
                "formatted_time": datetime.fromtimestamp(file["created"]).strftime('%Y-%m-%d %H:%M:%S'),
                "type": "CREATED",
                "file": file["path"]
            })
            self.timeline.append({
                "timestamp": file["modified"],
                "formatted_time": datetime.fromtimestamp(file["modified"]).strftime('%Y-%m-%d %H:%M:%S'),
                "type": "MODIFIED",
                "file": file["path"]
            })
            self.timeline.append({
                "timestamp": file["accessed"],
                "formatted_time": datetime.fromtimestamp(file["accessed"]).strftime('%Y-%m-%d %H:%M:%S'),
                "type": "ACCESSED",
                "file": file["path"]
            })

        # Sort by timestamp
        self.timeline.sort(key=lambda x: x["timestamp"])
        
        log.info(f"[bold green]Timeline built with {len(self.timeline)} events.[/bold green]")
        return self.timeline

    def export_json(self, output_path):
        """Exports the timeline to a JSON file."""
        try:
            with open(output_path, "w") as f:
                json.dump(self.timeline, f, indent=4)
            log.info(f"[bold green]Timeline exported to {output_path}[/bold green]")
        except Exception as e:
            log.error(f"Failed to export timeline: {e}")
