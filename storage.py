"""
In-memory storage for watch data
"""

import logging
from typing import List, Dict, Optional
from threading import Lock
from utils.logger import setup_logger

logger = setup_logger()

class WatchStorage:
    def __init__(self):
        self.watches = {}  # user_id -> [watches]
        self.lock = Lock()
    
    def add_watch(self, user_id: int, chat_id: int, token: str, target_price: float) -> bool:
        """Add a new watch for a user"""
        with self.lock:
            if user_id not in self.watches:
                self.watches[user_id] = []
            
            # Check if user already has a watch for this token
            for watch in self.watches[user_id]:
                if watch['token'] == token:
                    logger.info(f"User {user_id} already has a watch for {token}")
                    return False
            
            # Add new watch
            watch = {
                'user_id': user_id,
                'chat_id': chat_id,
                'token': token,
                'target_price': target_price
            }
            
            self.watches[user_id].append(watch)
            logger.info(f"Added watch for user {user_id}: {token} at ${target_price}")
            return True
    
    def remove_watch(self, user_id: int, token: str) -> bool:
        """Remove a watch for a user"""
        with self.lock:
            if user_id not in self.watches:
                return False
            
            # Find and remove the watch
            for i, watch in enumerate(self.watches[user_id]):
                if watch['token'] == token:
                    del self.watches[user_id][i]
                    logger.info(f"Removed watch for user {user_id}: {token}")
                    
                    # Clean up empty user entries
                    if not self.watches[user_id]:
                        del self.watches[user_id]
                    
                    return True
            
            return False
    
    def get_user_watches(self, user_id: int) -> List[Dict]:
        """Get all watches for a user"""
        with self.lock:
            return self.watches.get(user_id, []).copy()
    
    def get_all_watches(self) -> List[Dict]:
        """Get all watches from all users"""
        with self.lock:
            all_watches = []
            for user_watches in self.watches.values():
                all_watches.extend(user_watches)
            return all_watches
    
    def get_watch_count(self) -> int:
        """Get total number of active watches"""
        with self.lock:
            return sum(len(watches) for watches in self.watches.values())
    
    def get_user_count(self) -> int:
        """Get number of users with active watches"""
        with self.lock:
            return len(self.watches)
    
    def clear_user_watches(self, user_id: int) -> int:
        """Clear all watches for a user"""
        with self.lock:
            if user_id in self.watches:
                count = len(self.watches[user_id])
                del self.watches[user_id]
                logger.info(f"Cleared {count} watches for user {user_id}")
                return count
            return 0
    
    def get_stats(self) -> Dict:
        """Get storage statistics"""
        with self.lock:
            return {
                'total_watches': self.get_watch_count(),
                'total_users': self.get_user_count(),
                'unique_tokens': len(set(
                    watch['token'] 
                    for watches in self.watches.values() 
                    for watch in watches
                ))
            }
