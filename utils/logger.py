import logging
from rich.console import Console
from rich.theme import Theme

# Custom theme for professional DFIR look
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "critical": "bold white on red"
})

console = Console(theme=custom_theme)

class DFIRLogger:
    def info(self, message):
        console.print(f"[bold cyan][*][/bold cyan] {message}")

    def success(self, message):
        console.print(f"[bold green][+][/bold green] {message}")

    def warning(self, message):
        console.print(f"[bold yellow][!][/bold yellow] {message}")
    
    def error(self, message):
        console.print(f"[bold red][!][/bold red] {message}")

log = DFIRLogger()
