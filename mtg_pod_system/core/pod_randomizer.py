import random
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Pod:
    """Represents a single pod of players"""
    id: int
    players: List[str]
    size: int
    
    def __str__(self):
        return f"Pod {self.id} ({self.size} players): {', '.join(self.players)}"

class PodRandomizer:
    """Handles randomization of players into pods"""
    
    def __init__(self):
        self.history: List[List[Pod]] = []
    
    def create_pods(self, players: List[str], target_size: int = 4, max_size: int = 8) -> List[Pod]:
        """Create random pods from player list"""
        if not players:
            return []
        
        # Validate pod sizes
        target_size = max(3, min(target_size, max_size))
        
        # Shuffle players for randomness
        shuffled_players = players.copy()
        random.shuffle(shuffled_players)
        
        # Calculate optimal pod distribution
        total_players = len(shuffled_players)
        pods = self._calculate_pod_distribution(shuffled_players, target_size, max_size)
        
        # Save to history
        self.history.append(pods)
        return pods
    
    def _calculate_pod_distribution(self, players: List[str], target_size: int, max_size: int) -> List[Pod]:
        """Calculate optimal pod distribution for balanced gameplay"""
        total_players = len(players)
        pods = []
        player_index = 0
        
        # Calculate number of pods needed
        min_pods = (total_players + max_size - 1) // max_size
        max_pods = (total_players + target_size - 1) // target_size
        
        # Try to find optimal distribution
        for num_pods in range(min_pods, max_pods + 1):
            if num_pods == 0:
                continue
                
            # Calculate base size and remainder
            base_size = total_players // num_pods
            remainder = total_players % num_pods
            
            # Create pods with balanced distribution
            current_pods = []
            current_index = 0
            
            for i in range(num_pods):
                # Some pods get one extra player to handle remainder
                pod_size = base_size + (1 if i < remainder else 0)
                
                if pod_size == 0:
                    continue
                    
                # Ensure pod size is within valid range
                pod_size = max(3, min(pod_size, max_size))
                
                # Add players to this pod
                pod_players = players[current_index:current_index + pod_size]
                current_pods.append(Pod(
                    id=i + 1,
                    players=pod_players,
                    size=len(pod_players)
                ))
                current_index += pod_size
            
            # Check if this distribution uses all players
            if current_index >= total_players:
                pods = current_pods
                break
        
        # Fallback: simple distribution
        if not pods:
            pods = self._simple_distribution(players, target_size, max_size)
        
        return pods
    
    def _simple_distribution(self, players: List[str], target_size: int, max_size: int) -> List[Pod]:
        """Simple fallback distribution method"""
        pods = []
        pod_id = 1
        i = 0
        
        while i < len(players):
            # Determine pod size (prefer target size, adjust for remainder)
            remaining_players = len(players) - i
            pod_size = min(target_size, remaining_players)
            
            # If this is the last pod and too small, merge with previous
            if remaining_players < 3 and pods:
                # Add remaining players to last pod if it won't exceed max_size
                if len(pods[-1].players) + remaining_players <= max_size:
                    pods[-1].players.extend(players[i:])
                    pods[-1].size = len(pods[-1].players)
                    break
                # Otherwise, make a smaller pod (better than excluding players)
                elif remaining_players > 0:
                    pod_size = remaining_players
            
            # Create pod
            pod_players = players[i:i + pod_size]
            pods.append(Pod(
                id=pod_id,
                players=pod_players,
                size=len(pod_players)
            ))
            
            i += pod_size
            pod_id += 1
        
        return pods
    
    def get_statistics(self, pods: List[Pod]) -> Dict:
        """Get statistics about pod distribution"""
        if not pods:
            return {"total_pods": 0, "total_players": 0, "avg_pod_size": 0}
        
        total_players = sum(pod.size for pod in pods)
        pod_sizes = [pod.size for pod in pods]
        
        return {
            "total_pods": len(pods),
            "total_players": total_players,
            "avg_pod_size": total_players / len(pods),
            "min_pod_size": min(pod_sizes),
            "max_pod_size": max(pod_sizes),
            "pod_sizes": pod_sizes
        }
    
    def get_history(self) -> List[List[Pod]]:
        """Get history of pod assignments"""
        return self.history.copy()
    
    def clear_history(self):
        """Clear assignment history"""
        self.history.clear()