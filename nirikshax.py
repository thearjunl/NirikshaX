import argparse
import sys
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.scanner import Scanner
from core.recovery import RecoveryEngine
from core.timeline import TimelineGenerator
from artifacts.system_info import get_system_info
from artifacts.recent_files import RecentFilesScanner
from artifacts.browser_history import BrowserHistoryExtractor
from utils.logger import log, console

def print_banner():
    banner = """
    [bold cyan]
    ███╗   ██╗██╗██████╗ ██╗██╗  ██╗███████╗██╗  ██╗ █████╗ ██╗  ██╗
    ████╗  ██║██║██╔══██╗██║██║ ██╔╝██╔════╝██║  ██║██╔══██╗╚██╗██╔╝
    ██╔██╗ ██║██║██████╔╝██║█████╔╝ ███████╗███████║███████║ ╚███╔╝ 
    ██║╚██╗██║██║██╔══██╗██║██╔═██╗ ╚════██║██╔══██║██╔══██║ ██╔██╗ 
    ██║ ╚████║██║██║  ██║██║██║  ██╗███████║██║  ██║██║  ██║██╔╝ ██╗
    ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    [/bold cyan]
    [bold white]Digital Forensic Recovery & Investigation Tool[/bold white]
    [red]AUTHORIZED USE ONLY[/red]
    """
    console.print(Panel(banner, border_style="bold blue"))

def cmd_scan(args):
    """Handles the scan command."""
    log.info(f"Starting scan on: {args.target}")
    scanner = Scanner(args.target)
    results = scanner.scan()
    
    # Display summary table
    table = Table(title=f"Scan Results for {args.target}")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Suspicious", style="red")
    
    for item in results[:20]: # Show first 20 for brevity in CLI
        suspicious_mark = "[bold red]YES[/bold red]" if item["suspicious"] else ""
        table.add_row(os.path.basename(item["path"]), item["extension_detected"] or "Unknown", suspicious_mark)
        
    console.print(table)
    if len(results) > 20:
        console.print(f"... and {len(results) - 20} more files.")

    # Save report
    report = {
        "timestamp": str(datetime.now()),
        "scan_target": args.target,
        "files_found": len(results),
        "suspicious_files": [f for f in results if f["suspicious"]],
        "all_files": results
    }
    
    with open("scan_report.json", "w") as f:
        json.dump(report, f, indent=4)
    log.info("[bold green]Report saved to scan_report.json[/bold green]")

def cmd_recover(args):
    """Handles the recover command."""
    scanner = Scanner(args.target)
    results = scanner.scan()
    
    recovery = RecoveryEngine("output/recovered")
    # Default to common formats if not specified
    extensions = args.type.split(",") if args.type else None
    
    count = recovery.recover_files(results, extensions=extensions)
    log.info(f"Recovered {count} files to output/recovered")

def cmd_artifacts(args):
    """Handles the artifacts command."""
    log.info("Collecting system artifacts...")
    
    sys_info = get_system_info()
    console.print(Panel(str(sys_info), title="System Information"))
    
    recent = RecentFilesScanner().scan_recent(days=3)
    
    # Browser history
    history = BrowserHistoryExtractor().get_chrome_history()
    
    report = {
        "system_info": sys_info,
        "recent_files": recent,
        "browser_history": history
    }
    
    with open("artifacts_report.json", "w") as f:
        json.dump(report, f, indent=4)
    log.info("[bold green]Artifacts report saved to artifacts_report.json[/bold green]")

def cmd_timeline(args):
    """Handles the timeline command."""
    scanner = Scanner(args.target)
    results = scanner.scan()
    
    timeline_gen = TimelineGenerator(results)
    timeline_gen.build()
    timeline_gen.export_json("timeline.json")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="NirikshaX - Digital Forensic Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Scan Command
    scan_parser = subparsers.add_parser("scan", help="Scan a directory")
    scan_parser.add_argument("target", help="Directory to scan")

    # Recover Command
    recover_parser = subparsers.add_parser("recover", help="Recover files")
    recover_parser.add_argument("target", help="Source directory")
    recover_parser.add_argument("--type", help="Comma-separated file extensions to recover (e.g. jpg,pdf)")

    # Artifacts Command
    subparsers.add_parser("artifacts", help="Collect system artifacts")

    # Timeline Command
    timeline_parser = subparsers.add_parser("timeline", help="Generate timeline")
    timeline_parser.add_argument("target", help="Directory to analyze")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "recover":
        cmd_recover(args)
    elif args.command == "artifacts":
        cmd_artifacts(args)
    elif args.command == "timeline":
        cmd_timeline(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
