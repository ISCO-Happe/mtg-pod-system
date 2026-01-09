import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any

class SyncManager:
    """Handles synchronization between terminal and web interfaces"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.web_data_file = os.path.join(data_dir, "web_sync.json")
        self.terminal_data_file = os.path.join(data_dir, "terminal_sync.json")
        self.sync_log_file = os.path.join(data_dir, "sync_log.json")
        
    def sync_terminal_to_web(self, players: List[str], config: Dict[str, Any], history: List[Dict]) -> bool:
        """Sync terminal data to web format"""
        try:
            web_data = {
                "players": players,
                "config": config,
                "history": history,
                "last_sync": datetime.now().isoformat(),
                "sync_source": "terminal",
                "version": "1.0"
            }
            
            with open(self.web_data_file, 'w') as f:
                json.dump(web_data, f, indent=2)
            
            self._log_sync("terminal_to_web", len(players), len(history))
            return True
        except Exception as e:
            print(f"Error syncing terminal to web: {e}")
            return False
    
    def sync_web_to_terminal(self, storage_manager) -> bool:
        """Sync web data to terminal format"""
        try:
            if not os.path.exists(self.web_data_file):
                return False
            
            with open(self.web_data_file, 'r') as f:
                web_data = json.load(f)
            
            # Save players to terminal format
            if 'players' in web_data:
                storage_manager.save_players(web_data['players'])
            
            # Save config
            if 'config' in web_data:
                storage_manager.save_config(web_data['config'])
            
            # Save history
            if 'history' in web_data:
                storage_manager.save_history(web_data['history'])
            
            self._log_sync("web_to_terminal", len(web_data.get('players', [])), len(web_data.get('history', [])))
            return True
        except Exception as e:
            print(f"Error syncing web to terminal: {e}")
            return False
    
    def get_web_data(self) -> Optional[Dict[str, Any]]:
        """Get web-formatted data"""
        try:
            if os.path.exists(self.web_data_file):
                with open(self.web_data_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error reading web data: {e}")
            return None
    
    def create_sync_file(self, file_path: str, data_type: str) -> bool:
        """Create a sync file for easy sharing"""
        try:
            if data_type == "web":
                source_file = self.web_data_file
            else:
                source_file = self.terminal_data_file
            
            if not os.path.exists(source_file):
                return False
            
            shutil.copy2(source_file, file_path)
            return True
        except Exception as e:
            print(f"Error creating sync file: {e}")
            return False
    
    def import_sync_file(self, file_path: str, data_type: str, merge: bool = False) -> bool:
        """Import data from sync file"""
        try:
            with open(file_path, 'r') as f:
                sync_data = json.load(f)
            
            if data_type == "web":
                if merge and os.path.exists(self.web_data_file):
                    with open(self.web_data_file, 'r') as f:
                        existing_data = json.load(f)
                    
                    # Merge data
                    if 'players' in sync_data and 'players' in existing_data:
                        all_players = list(set(existing_data['players'] + sync_data['players']))
                        sync_data['players'] = all_players
                
                with open(self.web_data_file, 'w') as f:
                    json.dump(sync_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error importing sync file: {e}")
            return False
    
    def _log_sync(self, sync_type: str, player_count: int, history_count: int):
        """Log synchronization events"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "sync_type": sync_type,
                "player_count": player_count,
                "history_count": history_count
            }
            
            logs = []
            if os.path.exists(self.sync_log_file):
                with open(self.sync_log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            # Keep only last 50 log entries
            if len(logs) > 50:
                logs = logs[-50:]
            
            with open(self.sync_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"Error logging sync: {e}")
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get synchronization status"""
        status = {
            "web_sync_exists": os.path.exists(self.web_data_file),
            "terminal_sync_exists": os.path.exists(self.terminal_sync_file),
            "last_sync": None,
            "sync_count": 0
        }
        
        try:
            if os.path.exists(self.sync_log_file):
                with open(self.sync_log_file, 'r') as f:
                    logs = json.load(f)
                    if logs:
                        status["last_sync"] = logs[-1]["timestamp"]
                        status["sync_count"] = len(logs)
        except Exception:
            pass
        
        return status