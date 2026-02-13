import platform
import os
import socket
from utils.logger import log

def get_system_info():
    """Collects basic system information."""
    info = {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "user": os.getlogin()
    }
    log.info(f"[bold green]System Info collected: {info['hostname']} ({info['os']})[/bold green]")
    return info
