import logging
from rich.logging import RichHandler
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

def setup_logger():
    """Configures and returns a rich logger."""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, markup=True)]
    )
    log = logging.getLogger("rich")
    return log, console

log, console = setup_logger()
