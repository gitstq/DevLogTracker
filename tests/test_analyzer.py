"""
Unit tests for LogAnalyzer
"""
import os
import json
import tempfile
import unittest
from datetime import datetime
from devlog_tracker.analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.json")
        events = [
            {
                "timestamp": datetime.now().isoformat(),
                "type": "modified",
                "file": "/test/main.py",
                "extension": ".py",
                "size": 100
            },
            {
                "timestamp": datetime.now().isoformat(),
                "type": "created",
                "file": "/test/utils.py",
                "extension": ".py",
                "size": 50
            }
        ]
        with open(self.log_file, 'w') as f:
            json.dump(events, f)
    
    def tearDown(self):
        os.remove(self.log_file)
        os.rmdir(self.temp_dir)
    
    def test_daily_summary(self):
        analyzer = LogAnalyzer(self.log_file)
        summary = analyzer.daily_summary()
        self.assertEqual(summary['total_events'], 2)
        self.assertEqual(summary['unique_files'], 2)
    
    def test_productivity_score(self):
        analyzer = LogAnalyzer(self.log_file)
        score = analyzer.productivity_score()
        self.assertIn('score', score)
        self.assertIn('level', score)

if __name__ == '__main__':
    unittest.main()
