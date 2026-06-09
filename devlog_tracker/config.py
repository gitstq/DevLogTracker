"""
Configuration management for DevLogTracker
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List, Any

DEFAULT_CONFIG = {
    "watch_paths": ["."],
    "ignore_patterns": [
        "*.pyc", "__pycache__", ".git", "node_modules", ".venv", "venv",
        "*.log", "*.tmp", ".idea", ".vscode", "dist", "build",
        "*.min.js", "*.min.css", "coverage", ".pytest_cache"
    ],
    "log_file": "devlog.json",
    "auto_commit": False,
    "categories": {
        "code": [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c"],
        "config": [".json", ".yaml", ".yml", ".toml", ".ini", ".env"],
        "doc": [".md", ".rst", ".txt"],
        "test": ["test_*.py", "*_test.py", "*.spec.js", "*.test.ts"],
        "style": [".css", ".scss", ".less", ".html"]
    },
    "thresholds": {
        "large_file": 500,
        "hot_edit": 10
    }
}

class Config:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._find_config()
        self.data = self._load()
    
    def _find_config(self) -> str:
        cwd = Path.cwd()
        config_file = cwd / ".devlog.yml"
        if config_file.exists():
            return str(config_file)
        home = Path.home()
        global_config = home / ".config" / "devlog" / "config.yml"
        if global_config.exists():
            return str(global_config)
        return str(config_file)
    
    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return DEFAULT_CONFIG.copy()
        with open(self.config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f) or {}
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        return config
    
    def save(self):
        os.makedirs(os.path.dirname(self.config_path) or '.', exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        self.data[key] = value
