import argparse
import sys
import json
import os
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.layout import Layout
from rich.live import Live

from core.scanner import Scanner
from core.recovery import RecoveryEngine
from core.timeline import TimelineGenerator
from artifacts.system_info import get_system_info
from artifacts.recent_files import RecentFilesScanner
from artifacts.browser_history import BrowserHistoryExtractor
from utils.logger import log, console

def print_banner():
    banner_text = """
    [bold cyan]    
    ███╗   ██╗██╗██████╗ ██╗██╗  ██╗███████╗██╗  ██╗ █████╗ ██╗  ██╗
    ████╗  ██║██║██╔══██╗██║██║ ██╔╝██╔════╝██║  ██║██╔══██╗╚██╗██╔╝
    ██╔██╗ ██║██║██████╔╝██║█████╔╝ ███████╗███████║███████║ ╚███╔╝ 
    ██║╚██╗██║██║██╔══██╗██║██╔═██╗ ╚════██║██╔══██║██╔══██║ ██╔██╗ 
    ██║ ╚████║██║██║  ██║██║██║  ██╗███████║██║  ██║██║  ██║██╔╝ ██╗
    ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    [/bold cyan]
    [bold white]    DIGITAL FORENSIC RECOVERY & INVESTIGATION UTILITY[/bold white]
    [dim]    v1.0.0 | Coded for Professional Use[/dim]
    """
    console.print(banner_text)
    console.print("[bold red]    [!] AUTHORIZED USE ONLY. DO NOT USE FOR ILLEGAL ACTIVITIES.[/bold red]\n")

def cmd_scan(args):
    """Handles the scan command with professional UI."""
    log.info(f"Target: [bold white]{args.target}[/bold white]")
    log.info("Initializing scanning engine...")
    
    scanner = Scanner(args.target)
    
    # Live scan progress
    with Progress(
        SpinnerColumn(style="bold cyan"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=None, style="dim white"),
        TextColumn("[bold green]{task.fields[last_file]}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Scanning filesystem...", total=None, last_file="")
        
        def update_progress(file_info):
            progress.update(task, last_file=os.path.basename(file_info["path"])[:30])
        
        # Run scan
        results = scanner.scan(progress_callback=update_progress)
        progress.update(task, description="[bold green]Scan Complete[/bold green]", last_file=f"{len(results)} files found")

    console.print() 
    
    # Display summary table
    table = Table(title="SCAN RESULTS", title_style="bold cyan", border_style="dim white", show_lines=False)
    table.add_column("Filename", style="bold white")
    table.add_column("Type", style="cyan")
    table.add_column("Path", style="dim white")
    table.add_column("Status", style="bold red")
    
    suspicious_count = 0
    for item in results:
        if item["suspicious"]:
            suspicious_count += 1
            table.add_row(
                os.path.basename(item["path"]), 
                item["extension_detected"] or "Unknown", 
                item["path"][-50:], # Truncate path for display
                "[!] SUSPICIOUS"
            )
            
    # If no suspicious files, show last 10 normal files
    if suspicious_count == 0:
        for item in results[-10:]:
             table.add_row(
                os.path.basename(item["path"]), 
                item["extension_detected"] or "Unknown", 
                item["path"][-50:], 
                "[✓] OK"
            )

    console.print(table)
    
    if suspicious_count > 0:
        log.warning(f"Detected {suspicious_count} suspicious artifacts!")
    else:
        log.success("No suspicious artifacts detected in sample view.")

    # Save report
    report_file = "scan_report.json"
    report = {
        "timestamp": str(datetime.now()),
        "scan_target": args.target,
        "files_found": len(results),
        "suspicious_files": [f for f in results if f["suspicious"]],
        "all_files": results
    }
    
    with open(report_file, "w") as f:
        json.dump(report, f, indent=4)
    log.success(f"Full report saved to [bold white]{report_file}[/bold white]")

def cmd_recover(args):
    """Handles the recover command."""
    log.info(f"Target: [bold white]{args.target}[/bold white]")
    log.info("Scanning for recoverable files...")
    
    scanner = Scanner(args.target)
    results = scanner.scan()
    
    recovery = RecoveryEngine("output/recovered")
    extensions = args.type.split(",") if args.type else None
    
    log.info(f"Recovery Filter: {extensions if extensions else 'ALL'}")
    
    count = recovery.recover_files(results, extensions=extensions)
    
    if count > 0:
        log.success(f"Successfully recovered {count} files to [bold white]output/recovered[/bold white]")
    else:
        log.warning("No matching files found to recover.")

def cmd_artifacts(args):
    """Handles the artifacts command."""
    log.info("Engaging Artifact Collection Module...")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        console=console
    ) as progress:
        task1 = progress.add_task("[cyan]Collecting System Info...", total=None)
        sys_info = get_system_info()
        progress.update(task1, completed=True, description="[green]System Info Collected[/green]")
        
        task2 = progress.add_task("[cyan]Scanning Recent Files...", total=None)
        recent = RecentFilesScanner().scan_recent(days=3)
        progress.update(task2, completed=True, description="[green]Recent Files Scanned[/green]")
        
        task3 = progress.add_task("[cyan]Extracting Browser History...", total=None)
        history = BrowserHistoryExtractor().get_chrome_history()
        progress.update(task3, completed=True, description="[green]Browser History Extracted[/green]")

    # Display System Info
    console.print()
    sys_table = Table(title="SYSTEM INTELLIGENCE", border_style="dim white", show_header=False)
    for key, val in sys_info.items():
        sys_table.add_row(f"[bold cyan]{key.upper()}[/bold cyan]", str(val))
    console.print(sys_table)

    report = {
        "system_info": sys_info,
        "recent_files": recent,
        "browser_history": history
    }
    
    with open("artifacts_report.json", "w") as f:
        json.dump(report, f, indent=4)
    log.success("Artifacts report saved to [bold white]artifacts_report.json[/bold white]")

def cmd_timeline(args):
    """Handles the timeline command."""
    log.info(f"Building timeline for: {args.target}")
    
    scanner = Scanner(args.target)
    results = scanner.scan()
    
    timeline_gen = TimelineGenerator(results)
    timeline_gen.build()
    timeline_gen.export_json("timeline.json")
    
    log.success("Timeline generated and saved to [bold white]timeline.json[/bold white]")

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
        console.print("[bold yellow][!] No command specified. Use --help for usage.[/bold yellow]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Operation cancelled by user.[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red][!] An unexpected error occurred: {e}[/bold red]")
