import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class PlayerManager:
    """Manages player operations for MTG pod system"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.players_file = os.path.join(data_dir, "players.json")
        self.players: List[str] = []
        self._ensure_data_dir()
        self.load_players()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def add_player(self, name: str) -> bool:
        """Add a player to the list"""
        name = name.strip()
        if not name:
            return False
        
        if name.lower() in [p.lower() for p in self.players]:
            return False  # Duplicate
        
        self.players.append(name)
        return True
    
    def remove_player(self, name: str) -> bool:
        """Remove a player from the list"""
        name = name.strip()
        if name in self.players:
            self.players.remove(name)
            return True
        return False
    
    def get_players(self) -> List[str]:
        """Get all players"""
        return self.players.copy()
    
    def get_player_count(self) -> int:
        """Get total number of players"""
        return len(self.players)
    
    def clear_players(self):
        """Clear all players"""
        self.players.clear()
    
    def save_players(self) -> bool:
        """Save players to file"""
        try:
            data = {
                "players": self.players,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.players_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_players(self) -> bool:
        """Load players from file"""
        try:
            if os.path.exists(self.players_file):
                with open(self.players_file, 'r') as f:
                    data = json.load(f)
                    self.players = data.get("players", [])
            return True
        except Exception:
            self.players = []
            return False
    
    def import_players_from_list(self, player_list: List[str]) -> int:
        """Import players from a list, returns number added"""
        added = 0
        for name in player_list:
            name = name.strip()
            if name and name.lower() not in [p.lower() for p in self.players]:
                self.players.append(name)
                added += 1
        return added
    
    def search_players(self, query: str) -> List[str]:
        """Search players by name"""
        query = query.lower()
        return [p for p in self.players if query in p.lower()]