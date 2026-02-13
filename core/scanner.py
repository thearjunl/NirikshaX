import os
import time
from core.signatures import get_file_type
from utils.logger import log

class Scanner:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.scan_results = []
        self.suspicious_files = []

    def scan(self, progress_callback=None):
        """Recursively scans the directory for files and identifies them."""
        # log.info(f"Starting scan on: {self.target_dir}") # Moved logging to CLI for cleaner output control
        
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_info = self.analyze_file(file_path)
                    if file_info:
                        self.scan_results.append(file_info)
                        self.check_suspicious(file_info)
                        
                        if progress_callback:
                            progress_callback(file_info)
                            
                except Exception as e:
                    # log.error(f"Error scanning {file_path}: {e}")
                    pass # Suppress individual file errors during scan to keep CLI clean

        # log.success(f"Scan complete. Found {len(self.scan_results)} files.")
        return self.scan_results

    def analyze_file(self, file_path):
        """Extracts metadata and identifies file type using magic bytes."""
        try:
            stats = os.stat(file_path)
            file_size = stats.st_size
            created = stats.st_ctime
            modified = stats.st_mtime
            accessed = stats.st_atime
            
            # Read magic bytes
            with open(file_path, "rb") as f:
                header = f.read(32)
            
            detected_type = get_file_type(header)
            extension = os.path.splitext(file_path)[1].lower().replace(".", "")

            return {
                "path": file_path,
                "size": file_size,
                "created": created,
                "modified": modified,
                "accessed": accessed,
                "extension_claimed": extension,
                "extension_detected": detected_type,
                "suspicious": False
            }
        except PermissionError:
            log.warning(f"Permission denied: {file_path}")
            return None
        except Exception:
            return None

    def check_suspicious(self, file_info):
        """Checks for suspicious indicators."""
        # Check for double extensions
        if file_info["path"].count(".") > 1:
             # loose check for double extension like .jpg.exe
             parts = file_info["path"].lower().split(".")
             if len(parts) >= 3:
                 # Check if the second to last part is a common file extension
                 known_exts = {"jpg", "jpeg", "png", "pdf", "docx", "txt", "zip"}
                 if parts[-2] in known_exts and parts[-1] in {"exe", "bat", "ps1", "vbs"}:
                     file_info["suspicious"] = True
                     file_info["reason"] = "Double extension detected"
                     self.suspicious_files.append(file_info)
                     log.warning(f"[bold red]Suspicious file detecting (Double Extension): {file_info['path']}[/bold red]")

        # Check for mismatched extensions
        if file_info["extension_detected"] and file_info["extension_detected"] != file_info["extension_claimed"]:
             # Verify it's not just a specificity issue (e.g. docx is a zip)
             if file_info["extension_detected"] == "zip" and file_info["extension_claimed"] in ["docx", "xlsx", "pptx", "apk", "jar"]:
                 pass # benign
             else:
                 file_info["suspicious"] = True
                 file_info["reason"] = f"Extension Mismatch (Claimed: {file_info['extension_claimed']}, Detected: {file_info['extension_detected']})"
                 self.suspicious_files.append(file_info)
                 log.warning(f"[bold red]Suspicious file detected (Mismatch): {file_info['path']}[/bold red]")
