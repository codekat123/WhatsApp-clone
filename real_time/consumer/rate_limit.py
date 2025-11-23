import time
from collections import defaultdict
from django.conf import settings

class RateLimiter:
    def __init__(self, limit=10, window=60):
        self.limit = limit  # messages
        self.window = window  # seconds
        self.user_timestamps = defaultdict(list)
    
    def check_rate_limit(self, user_id):
        now = time.time()
        timestamps = self.user_timestamps[user_id]
        
        
        timestamps = [ts for ts in timestamps if now - ts < self.window]
        self.user_timestamps[user_id] = timestamps
        
        if len(timestamps) >= self.limit:
            return False
        
        self.user_timestamps[user_id].append(now)
        return True
