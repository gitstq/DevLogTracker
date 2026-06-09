"""
Unit tests for ActivityTracker
"""
import os
import tempfile
import unittest
from devlog_tracker.watcher import ActivityTracker

class TestActivityTracker(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "devlog.json")
        self.tracker = ActivityTracker(log_file=self.log_file)
    
    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)
    
    def test_record_event(self):
        self.tracker.record_event("modified", "/test/file.py")
        self.assertEqual(len(self.tracker.events), 1)
        self.assertEqual(self.tracker.events[0]['type'], 'modified')
    
    def test_get_stats(self):
        self.tracker.record_event("modified", "/test/file.py")
        self.tracker.record_event("created", "/test/file2.py")
        stats = self.tracker.get_stats()
        self.assertEqual(stats['total_events'], 2)

if __name__ == '__main__':
    unittest.main()
