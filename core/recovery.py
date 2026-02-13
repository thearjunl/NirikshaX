import os
import shutil
from utils.logger import log

class RecoveryEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def recover_files(self, file_list, extensions=None):
        """Copies identified files to the recovery directory."""
        log.info(f"[bold cyan]Starting recovery to {self.output_dir}[/bold cyan]")
        
        recovered_count = 0
        
        for file_info in file_list:
            if extensions:
                # Filter by detected type if available, else claimed
                ext = file_info.get("extension_detected") or file_info.get("extension_claimed")
                if ext not in extensions:
                    continue
            
            try:
                dest_path = os.path.join(self.output_dir, os.path.basename(file_info["path"]))
                
                # Handle duplicate filenames
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(os.path.basename(file_info["path"]))
                    dest_path = os.path.join(self.output_dir, f"{base}_{int(file_info['created'])}{ext}")

                shutil.copy2(file_info["path"], dest_path)
                recovered_count += 1
                log.info(f"Recovered: {file_info['path']}")
                
            except Exception as e:
                log.error(f"Failed to recover {file_info['path']}: {e}")

        log.info(f"[bold green]Recovery complete. Recovered {recovered_count} files.[/bold green]")
        return recovered_count
