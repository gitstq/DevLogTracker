"""
File system watcher for tracking development activities
"""
import os
import time
import json
from datetime import datetime
from pathlib import Path
from fnmatch import fnmatch
from typing import List, Dict, Any, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

class DevLogHandler(FileSystemEventHandler):
    def __init__(self, tracker, ignore_patterns: List[str]):
        self.tracker = tracker
        self.ignore_patterns = ignore_patterns
    
    def _should_ignore(self, path: str) -> bool:
        basename = os.path.basename(path)
        for pattern in self.ignore_patterns:
            if fnmatch(basename, pattern) or fnmatch(path, pattern):
                return True
        # Always ignore the log file itself to prevent feedback loops
        if hasattr(self.tracker, 'log_file') and os.path.abspath(path) == os.path.abspath(self.tracker.log_file):
            return True
        return False
    
    def on_modified(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.tracker.record_event('modified', event.src_path)
    
    def on_created(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.tracker.record_event('created', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.tracker.record_event('deleted', event.src_path)

class ActivityTracker:
    def __init__(self, log_file: str = "devlog.json", ignore_patterns: List[str] = None):
        self.log_file = log_file
        self.ignore_patterns = ignore_patterns or []
        self.events: List[Dict[str, Any]] = []
        self._load_existing()
    
    def _load_existing(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.events = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.events = []
    
    def record_event(self, event_type: str, file_path: str):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "file": os.path.abspath(file_path),
            "extension": Path(file_path).suffix.lower(),
            "size": self._get_file_size(file_path) if event_type != 'deleted' else 0
        }
        self.events.append(event)
        self._save()
    
    def _get_file_size(self, path: str) -> int:
        try:
            return os.path.getsize(path)
        except OSError:
            return 0
    
    def _save(self):
        import fcntl
        temp_file = self.log_file + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(self.events, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
            fcntl.flock(f, fcntl.LOCK_UN)
        os.replace(temp_file, self.log_file)
    
    def get_stats(self) -> Dict[str, Any]:
        if not self.events:
            return {}
        
        stats = {
            "total_events": len(self.events),
            "total_modified": len([e for e in self.events if e["type"] == "modified"]),
            "total_created": len([e for e in self.events if e["type"] == "created"]),
            "total_deleted": len([e for e in self.events if e["type"] == "deleted"]),
            "extensions": {},
            "timeline": {},
            "hot_files": []
        }
        
        file_counts: Dict[str, int] = {}
        for event in self.events:
            ext = event["extension"] or "no_extension"
            stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
            
            date = event["timestamp"][:10]
            stats["timeline"][date] = stats["timeline"].get(date, 0) + 1
            
            file_path = event["file"]
            file_counts[file_path] = file_counts.get(file_path, 0) + 1
        
        stats["hot_files"] = sorted(
            [{"file": k, "edits": v} for k, v in file_counts.items()],
            key=lambda x: x["edits"],
            reverse=True
        )[:10]
        
        return stats

class Watcher:
    def __init__(self, paths: List[str], tracker: ActivityTracker, ignore_patterns: List[str] = None):
        self.paths = paths
        self.tracker = tracker
        self.ignore_patterns = ignore_patterns or []
        self.observer = Observer()
        self.handler = DevLogHandler(tracker, self.ignore_patterns)
    
    def start(self):
        for path in self.paths:
            if os.path.exists(path):
                self.observer.schedule(self.handler, path, recursive=True)
        self.observer.start()
    
    def stop(self):
        self.observer.stop()
        self.observer.join()
    
    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
