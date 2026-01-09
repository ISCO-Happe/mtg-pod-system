import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any

class DataStorage:
    """Handles data storage and backup operations"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.backup_dir = os.path.join(data_dir, "backups")
        self.players_file = os.path.join(data_dir, "players.json")
        self.config_file = os.path.join(data_dir, "config.json")
        self.history_file = os.path.join(data_dir, "history.json")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all necessary directories exist"""
        for directory in [self.data_dir, self.backup_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def save_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Save data to JSON file"""
        try:
            data['last_saved'] = datetime.now().isoformat()
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False
    
    def load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}
    
    def save_players(self, players: List[str]) -> bool:
        """Save player list"""
        data = {
            "players": players,
            "count": len(players)
        }
        return self.save_json(self.players_file, data)
    
    def load_players(self) -> List[str]:
        """Load player list"""
        data = self.load_json(self.players_file)
        return data.get("players", [])
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration"""
        return self.save_json(self.config_file, config)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        default_config = {
            "default_pod_size": 4,
            "max_pod_size": 8,
            "min_pod_size": 3,
            "auto_save": True,
            "keep_history": True,
            "max_history_items": 50
        }
        data = self.load_json(self.config_file)
        return {**default_config, **data}
    
    def save_history(self, history: List[Dict[str, Any]]) -> bool:
        """Save pod assignment history"""
        data = {
            "history": history,
            "count": len(history)
        }
        return self.save_json(self.history_file, data)
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load pod assignment history"""
        data = self.load_json(self.history_file)
        return data.get("history", [])
    
    def create_backup(self) -> bool:
        """Create backup of all data files"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_folder = os.path.join(self.backup_dir, f"backup_{timestamp}")
            os.makedirs(backup_folder)
            
            # Backup all data files
            for filename in [self.players_file, self.config_file, self.history_file]:
                if os.path.exists(filename):
                    basename = os.path.basename(filename)
                    shutil.copy2(filename, os.path.join(backup_folder, basename))
            
            print(f"Backup created: {backup_folder}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from a backup"""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                print(f"Backup not found: {backup_name}")
                return False
            
            # Restore files from backup
            for filename in ["players.json", "config.json", "history.json"]:
                backup_file = os.path.join(backup_path, filename)
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, os.path.join(self.data_dir, filename))
            
            print(f"Backup restored: {backup_name}")
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """List available backups"""
        if not os.path.exists(self.backup_dir):
            return []
        
        backups = []
        for item in os.listdir(self.backup_dir):
            if item.startswith("backup_") and os.path.isdir(os.path.join(self.backup_dir, item)):
                backups.append(item)
        
        return sorted(backups, reverse=True)  # Most recent first
    
    def export_data(self, export_path: str) -> bool:
        """Export all data to a single file"""
        try:
            export_data = {
                "players": self.load_players(),
                "config": self.load_config(),
                "history": self.load_history(),
                "export_timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"Data exported to: {export_path}")
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_data(self, import_path: str, merge: bool = False) -> bool:
        """Import data from a file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            if merge:
                # Merge with existing data
                current_players = self.load_players()
                import_players = import_data.get("players", [])
                
                # Combine players without duplicates
                all_players = list(set(current_players + import_players))
                self.save_players(all_players)
                
                # Merge configs (import takes precedence)
                import_config = import_data.get("config", {})
                current_config = self.load_config()
                merged_config = {**current_config, **import_config}
                self.save_config(merged_config)
                
            else:
                # Replace existing data
                self.save_players(import_data.get("players", []))
                self.save_config(import_data.get("config", {}))
                self.save_history(import_data.get("history", []))
            
            print(f"Data imported from: {import_path}")
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False