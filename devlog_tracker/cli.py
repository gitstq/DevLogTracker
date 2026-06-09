"""
Command-line interface for DevLogTracker
"""
import os
import sys
import time
import json
from datetime import datetime
from typing import List

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich import box

from .config import Config
from .watcher import Watcher, ActivityTracker
from .analyzer import LogAnalyzer

console = Console()

@click.group()
@click.version_option(version="1.0.0", prog_name="devlog")
def main():
    """🚀 DevLogTracker - Intelligent Developer Log Tracker"""
    pass

@main.command()
@click.option('--path', '-p', multiple=True, default=['.'], help='Paths to watch')
@click.option('--output', '-o', default='devlog.json', help='Output log file')
@click.option('--config', '-c', default=None, help='Config file path')
def watch(path: tuple, output: str, config: str):
    """👁️  Start watching file changes in real-time"""
    cfg = Config(config)
    
    watch_paths = list(path) if path else cfg.get('watch_paths', ['.'])
    ignore_patterns = cfg.get('ignore_patterns', [])
    
    tracker = ActivityTracker(log_file=output, ignore_patterns=ignore_patterns)
    watcher = Watcher(watch_paths, tracker, ignore_patterns)
    
    console.print(Panel.fit(
        f"[bold green]👁️  DevLog Tracker Started[/bold green]\n"
        f"Watching: {', '.join(watch_paths)}\n"
        f"Log file: {output}\n"
        f"Press Ctrl+C to stop",
        title="DevLog Tracker",
        border_style="green"
    ))
    
    watcher.run()

@main.command()
@click.option('--log-file', '-l', default='devlog.json', help='Log file path')
@click.option('--date', '-d', default=None, help='Date to summarize (YYYY-MM-DD)')
def summary(log_file: str, date: str):
    """📊  Show daily activity summary"""
    if not os.path.exists(log_file):
        console.print(f"[red]❌ Log file not found: {log_file}[/red]")
        return
    
    analyzer = LogAnalyzer(log_file)
    summary = analyzer.daily_summary(date)
    
    if "message" in summary:
        console.print(f"[yellow]⚠️  {summary['message']}[/yellow]")
        return
    
    table = Table(title=f"📅 Daily Summary - {summary['date']}", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Events", str(summary['total_events']))
    table.add_row("Unique Files", str(summary['unique_files']))
    table.add_row("Peak Hour", summary['peak_hour'])
    table.add_row("Activity Span", summary['activity_span'])
    
    console.print(table)
    
    if summary['top_extensions']:
        ext_table = Table(title="🔤 Top File Types", box=box.SIMPLE)
        ext_table.add_column("Extension", style="cyan")
        ext_table.add_column("Count", style="magenta")
        for ext, count in summary['top_extensions'].items():
            ext_table.add_row(ext or "unknown", str(count))
        console.print(ext_table)

@main.command()
@click.option('--log-file', '-l', default='devlog.json', help='Log file path')
def week(log_file: str):
    """📈  Show weekly report"""
    if not os.path.exists(log_file):
        console.print(f"[red]❌ Log file not found: {log_file}[/red]")
        return
    
    analyzer = LogAnalyzer(log_file)
    report = analyzer.weekly_report()
    
    table = Table(title=f"📈 Weekly Report - Week of {report['week_of']}", box=box.ROUNDED)
    table.add_column("Day", style="cyan")
    table.add_column("Events", style="magenta")
    table.add_column("Bar", style="green")
    
    max_count = max(report['daily_breakdown'].values()) if report['daily_breakdown'] else 1
    
    for day, count in report['daily_breakdown'].items():
        bar = "█" * int((count / max_count) * 20) if max_count > 0 else ""
        table.add_row(day, str(count), bar)
    
    table.add_row("", "", "")
    table.add_row("Total", str(report['total_events']), "")
    table.add_row("Average/Day", str(report['average_daily']), "")
    table.add_row("Most Active", report['most_active_day'], "")
    
    console.print(table)

@main.command()
@click.option('--log-file', '-l', default='devlog.json', help='Log file path')
def stats(log_file: str):
    """🏆  Show overall statistics and productivity score"""
    if not os.path.exists(log_file):
        console.print(f"[red]❌ Log file not found: {log_file}[/red]")
        return
    
    analyzer = LogAnalyzer(log_file)
    basic_stats = analyzer._load_events()
    
    tracker = ActivityTracker(log_file=log_file)
    tracker.events = basic_stats
    basic_stats = tracker.get_stats()
    productivity = analyzer.productivity_score()
    
    console.print(Panel.fit(
        f"[bold]{productivity['level']}[/bold]\n"
        f"Score: {productivity['score']}/100\n"
        f"Daily Average: {productivity['daily_average']} events\n"
        f"Unique Files: {productivity['unique_files']}",
        title="🏆 Productivity Score",
        border_style="blue"
    ))
    
    if basic_stats:
        table = Table(title="📊 Overall Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Total Events", str(basic_stats.get('total_events', 0)))
        table.add_row("Modified", str(basic_stats.get('total_modified', 0)))
        table.add_row("Created", str(basic_stats.get('total_created', 0)))
        table.add_row("Deleted", str(basic_stats.get('total_deleted', 0)))
        console.print(table)
        
        if basic_stats.get('hot_files'):
            hot_table = Table(title="🔥 Hot Files (Most Edited)", box=box.SIMPLE)
            hot_table.add_column("File", style="cyan", no_wrap=True)
            hot_table.add_column("Edits", style="magenta")
            for item in basic_stats['hot_files'][:5]:
                hot_table.add_row(item['file'], str(item['edits']))
            console.print(hot_table)
    
    if productivity['suggestions']:
        console.print("\n[bold yellow]💡 Suggestions:[/bold yellow]")
        for suggestion in productivity['suggestions']:
            console.print(f"  • {suggestion}")

@main.command()
@click.option('--log-file', '-l', default='devlog.json', help='Log file path')
@click.option('--output', '-o', default='devlog_report.html', help='Output HTML file')
def report(log_file: str, output: str):
    """📄  Generate HTML report"""
    if not os.path.exists(log_file):
        console.print(f"[red]❌ Log file not found: {log_file}[/red]")
        return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating report...", total=None)
        analyzer = LogAnalyzer(log_file)
        output_path = analyzer.export_report(output)
        progress.update(task, completed=True)
    
    console.print(f"[green]✅ Report generated: {os.path.abspath(output_path)}[/green]")

@main.command()
@click.option('--global', 'is_global', is_flag=True, help='Create global config')
def init(is_global: bool):
    """🔧  Initialize DevLogTracker configuration"""
    if is_global:
        config_path = os.path.expanduser("~/.config/devlog/config.yml")
    else:
        config_path = ".devlog.yml"
    
    if os.path.exists(config_path):
        console.print(f"[yellow]⚠️  Config already exists at {config_path}[/yellow]")
        return
    
    cfg = Config(config_path)
    cfg.save()
    
    console.print(f"[green]✅ Configuration created at {config_path}[/green]")
    console.print("[dim]Edit this file to customize watch paths and ignore patterns[/dim]")

@main.command()
@click.option('--log-file', '-l', default='devlog.json', help='Log file path')
@click.option('--days', '-d', default=30, help='Keep events from last N days')
def cleanup(log_file: str, days: int):
    """🧹  Clean up old log entries"""
    if not os.path.exists(log_file):
        console.print(f"[red]❌ Log file not found: {log_file}[/red]")
        return
    
    cutoff = datetime.now() - __import__('datetime').timedelta(days=days)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        events = json.load(f)
    
    filtered = [
        e for e in events 
        if datetime.fromisoformat(e['timestamp']) >= cutoff
    ]
    
    removed = len(events) - len(filtered)
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✅ Cleaned up {removed} old entries. Kept {len(filtered)} entries.[/green]")

if __name__ == '__main__':
    main()
