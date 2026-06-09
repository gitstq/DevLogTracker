"""
Analytics and insights for development logs
"""
import json
import os
from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, List, Any

class LogAnalyzer:
    def __init__(self, log_file: str = "devlog.json"):
        self.log_file = log_file
        self.events = self._load_events()
    
    def _load_events(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.log_file):
            return []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def daily_summary(self, date: str = None) -> Dict[str, Any]:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        day_events = [e for e in self.events if e["timestamp"].startswith(date)]
        
        if not day_events:
            return {"date": date, "message": "No activity recorded"}
        
        extensions = Counter(e["extension"] or "unknown" for e in day_events)
        event_types = Counter(e["type"] for e in day_events)
        files = set(e["file"] for e in day_events)
        
        return {
            "date": date,
            "total_events": len(day_events),
            "unique_files": len(files),
            "event_types": dict(event_types),
            "top_extensions": dict(extensions.most_common(5)),
            "peak_hour": self._get_peak_hour(day_events),
            "activity_span": self._get_activity_span(day_events)
        }
    
    def _get_peak_hour(self, events: List[Dict[str, Any]]) -> str:
        hours = Counter(e["timestamp"][11:13] for e in events)
        return hours.most_common(1)[0][0] + ":00" if hours else "N/A"
    
    def _get_activity_span(self, events: List[Dict[str, Any]]) -> str:
        if not events:
            return "N/A"
        times = [datetime.fromisoformat(e["timestamp"]) for e in events]
        start = min(times)
        end = max(times)
        duration = end - start
        return f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m)"
    
    def weekly_report(self) -> Dict[str, Any]:
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_events = [
            e for e in self.events 
            if datetime.fromisoformat(e["timestamp"]) >= week_start
        ]
        
        daily_counts = {}
        for i in range(7):
            day = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            day_events = [e for e in week_events if e["timestamp"].startswith(day)]
            daily_counts[day] = len(day_events)
        
        return {
            "week_of": week_start.strftime("%Y-%m-%d"),
            "total_events": len(week_events),
            "daily_breakdown": daily_counts,
            "most_active_day": max(daily_counts, key=daily_counts.get) if daily_counts else "N/A",
            "average_daily": round(len(week_events) / 7, 1) if week_events else 0
        }
    
    def productivity_score(self) -> Dict[str, Any]:
        if not self.events:
            return {"score": 0, "level": "No Data", "daily_average": 0, "unique_files": 0, "suggestions": ["Start coding to generate insights!"]}
        
        last_7_days = [e for e in self.events 
                       if datetime.fromisoformat(e["timestamp"]) >= datetime.now() - timedelta(days=7)]
        
        if not last_7_days:
            return {"score": 0, "level": "Inactive", "daily_average": 0, "unique_files": 0, "suggestions": ["No recent activity detected."]}
        
        daily_avg = len(last_7_days) / 7
        unique_files = len(set(e["file"] for e in last_7_days))
        
        score = min(100, int(daily_avg * 5 + unique_files * 2))
        
        level = "🔥 Prolific" if score >= 80 else "⚡ Productive" if score >= 50 else "🌱 Steady" if score >= 20 else "💤 Quiet"
        
        suggestions = []
        if daily_avg < 10:
            suggestions.append("Consider setting daily coding goals to build momentum.")
        if unique_files < 5:
            suggestions.append("Try working across different modules to diversify your contributions.")
        if score >= 80:
            suggestions.append("Amazing productivity! Remember to take breaks to avoid burnout.")
        
        return {
            "score": score,
            "level": level,
            "daily_average": round(daily_avg, 1),
            "unique_files": unique_files,
            "suggestions": suggestions
        }
    
    def export_report(self, output_file: str = "devlog_report.html"):
        from jinja2 import Template
        
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DevLog Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin: 10px 20px 10px 0; }
        .metric-value { font-size: 2em; font-weight: bold; color: #667eea; }
        .metric-label { color: #666; font-size: 0.9em; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 2px; }
        .badge-primary { background: #e3f2fd; color: #1976d2; }
        .badge-success { background: #e8f5e9; color: #388e3c; }
        .suggestion { background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; margin: 8px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 DevLog Tracker Report</h1>
        <p>Generated on {{ now }}</p>
    </div>
    
    <div class="card">
        <h2>📈 Productivity Overview</h2>
        <div class="metric">
            <div class="metric-value">{{ productivity.score }}</div>
            <div class="metric-label">Productivity Score</div>
        </div>
        <div class="metric">
            <div class="metric-value">{{ productivity.level }}</div>
            <div class="metric-label">Level</div>
        </div>
        <div class="metric">
            <div class="metric-value">{{ productivity.daily_average }}</div>
            <div class="metric-label">Daily Avg Events</div>
        </div>
    </div>
    
    <div class="card">
        <h2>📅 Weekly Breakdown</h2>
        {% for day, count in weekly.daily_breakdown.items() %}
        <span class="badge badge-primary">{{ day }}: {{ count }} events</span>
        {% endfor %}
        <p><strong>Most Active Day:</strong> {{ weekly.most_active_day }}</p>
    </div>
    
    <div class="card">
        <h2>💡 Suggestions</h2>
        {% for suggestion in productivity.suggestions %}
        <div class="suggestion">{{ suggestion }}</div>
        {% endfor %}
    </div>
</body>
</html>
"""
        
        template = Template(template_str)
        html = template.render(
            now=datetime.now().strftime("%Y-%m-%d %H:%M"),
            productivity=self.productivity_score(),
            weekly=self.weekly_report()
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_file
