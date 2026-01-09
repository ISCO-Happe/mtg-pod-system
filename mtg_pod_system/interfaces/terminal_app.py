import sys
import os
from typing import List, Optional

# Add the project root to the path so we can import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.player_manager import PlayerManager
from core.pod_randomizer import PodRandomizer, Pod
from core.data_storage import DataStorage
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich import print as rprint

class TerminalInterface:
    """Interactive terminal interface for MTG Pod System"""
    
    def __init__(self):
        self.console = Console()
        self.player_manager = PlayerManager()
        self.pod_randomizer = PodRandomizer()
        self.data_storage = DataStorage()
        self.config = self.data_storage.load_config()
        
    def run(self):
        """Main application loop"""
        self.console.clear()
        self.show_welcome()
        
        while True:
            self.show_main_menu()
            choice = self.get_menu_choice("Select an option", ["1", "2", "3", "4", "5", "6", "7", "q"])
            
            if choice == "1":
                self.manage_players()
            elif choice == "2":
                self.create_pods()
            elif choice == "3":
                self.view_history()
            elif choice == "4":
                self.settings_menu()
            elif choice == "5":
                self.data_menu()
            elif choice == "6":
                self.show_statistics()
            elif choice == "7":
                self.quick_randomize()
            elif choice.lower() == "q":
                self.console.print("Goodbye!", style="bold green")
                break
    
    def show_welcome(self):
        """Display welcome message"""
        title = Text("MTG Pod Randomizer", style="bold bright_magenta")
        subtitle = Text("Player Pod Management System", style="italic cyan")
        
        welcome_panel = Panel(
            Align.center(Text.from_markup(f"{title}\n\n{subtitle}")),
            border_style="bright_magenta",
            padding=(1, 2)
        )
        
        rprint(Align.center(welcome_panel))
        self.console.print()
    
    def show_main_menu(self):
        """Display main menu options"""
        menu_text = Text()
        menu_text.append("Main Menu\n\n", style="bold white")
        
        menu_options = [
            ("1.", "Manage Players", "green"),
            ("2.", "Create Random Pods", "yellow"),
            ("3.", "View History", "cyan"),
            ("4.", "Settings", "blue"),
            ("5.", "Data Management", "magenta"),
            ("6.", "Statistics", "red"),
            ("7.", "Quick Randomize", "bright_green"),
            ("q.", "Quit", "red")
        ]
        
        for num, desc, color in menu_options:
            menu_text.append(f"{num} ", style=color)
            menu_text.append(f"{desc}\n", style="white")
        
        panel = Panel(menu_text, title="Menu", border_style="bright_cyan")
        rprint(panel)
    
    def get_menu_choice(self, prompt: str, valid_choices: List[str]) -> str:
        """Get and validate menu choice"""
        while True:
            choice = Prompt.ask(prompt, default="q").strip()
            if choice in valid_choices:
                return choice
            self.console.print("Invalid choice. Please try again.", style="red")
    
    def manage_players(self):
        """Player management submenu"""
        while True:
            self.console.clear()
            self.console.print("Player Management", style="bold blue")
            self.console.print(f"Current Players: {self.player_manager.get_player_count()}\n")
            
            # Show current players
            if self.player_manager.get_players():
                self.display_players_table()
                self.console.print()
            
            choices = ["1", "2", "3", "4", "5", "b"]
            choice = self.get_menu_choice(
                "1) Add Player  2) Add Multiple  3) Remove Player  4) Search  5) Clear All  b) Back",
                choices
            )
            
            if choice == "1":
                self.add_single_player()
            elif choice == "2":
                self.add_multiple_players()
            elif choice == "3":
                self.remove_player()
            elif choice == "4":
                self.search_players()
            elif choice == "5":
                self.clear_all_players()
            elif choice == "b":
                break
    
    def add_single_player(self):
        """Add a single player"""
        name = Prompt.ask("Enter player name").strip()
        if name and self.player_manager.add_player(name):
            self.player_manager.save_players()
            self.console.print(f"Added: {name}", style="green")
        else:
            self.console.print("Failed to add player (empty or duplicate name)", style="red")
        Prompt.ask("Press Enter to continue")
    
    def add_multiple_players(self):
        """Add multiple players"""
        self.console.print("Enter player names (one per line). Enter blank line when done.")
        names = []
        while True:
            name = Prompt.ask("Player name").strip()
            if not name:
                break
            names.append(name)
        
        if names:
            added = 0
            for name in names:
                if self.player_manager.add_player(name):
                    added += 1
            
            if added > 0:
                self.player_manager.save_players()
                self.console.print(f"Added {added} player(s)", style="green")
            else:
                self.console.print("No new players added", style="yellow")
        
        Prompt.ask("Press Enter to continue")
    
    def remove_player(self):
        """Remove a player"""
        players = self.player_manager.get_players()
        if not players:
            self.console.print("No players to remove", style="yellow")
            Prompt.ask("Press Enter to continue")
            return
        
        name = Prompt.ask("Enter player name to remove").strip()
        if self.player_manager.remove_player(name):
            self.player_manager.save_players()
            self.console.print(f"Removed: {name}", style="green")
        else:
            self.console.print(f"Player not found: {name}", style="red")
        Prompt.ask("Press Enter to continue")
    
    def search_players(self):
        """Search for players"""
        query = Prompt.ask("Enter search term").strip()
        if not query:
            return
        
        results = self.player_manager.search_players(query)
        if results:
            self.console.print(f"Found {len(results)} player(s):", style="green")
            for i, player in enumerate(results, 1):
                self.console.print(f"  {i}. {player}")
        else:
            self.console.print("No players found", style="yellow")
        Prompt.ask("Press Enter to continue")
    
    def clear_all_players(self):
        """Clear all players"""
        if Confirm.ask("Are you sure you want to clear all players?"):
            self.player_manager.clear_players()
            self.player_manager.save_players()
            self.console.print("All players cleared", style="green")
        else:
            self.console.print("Cancelled", style="yellow")
        Prompt.ask("Press Enter to continue")
    
    def display_players_table(self):
        """Display players in a table"""
        players = self.player_manager.get_players()
        if not players:
            return
        
        table = Table(title="Current Players")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Name", style="white")
        
        for i, player in enumerate(players, 1):
            table.add_row(str(i), player)
        
        rprint(table)
    
    def create_pods(self):
        """Create random pods"""
        players = self.player_manager.get_players()
        if len(players) < 3:
            self.console.print("Need at least 3 players to create pods", style="red")
            Prompt.ask("Press Enter to continue")
            return
        
        # Get pod size preference
        pod_size = Prompt.ask(
            f"Target pod size (3-{self.config['max_pod_size']})",
            default=str(self.config['default_pod_size'])
        )
        
        try:
            pod_size = int(pod_size)
            pod_size = max(3, min(pod_size, self.config['max_pod_size']))
        except ValueError:
            pod_size = self.config['default_pod_size']
        
        # Create pods
        pods = self.pod_randomizer.create_pods(players, pod_size, self.config['max_pod_size'])
        
        # Display results
        self.display_pods(pods)
        
        # Save to history
        if self.config['keep_history']:
            self.save_to_history(pods)
        
        Prompt.ask("Press Enter to continue")
    
    def display_pods(self, pods: List[Pod]):
        """Display pods in a formatted way"""
        self.console.print("Pod Assignment:", style="bold yellow")
        
        for pod in pods:
            # Create colored panel for each pod
            players_text = Text()
            for i, player in enumerate(pod.players):
                players_text.append(f"{i+1}. {player}", style="white")
                if i < len(pod.players) - 1:
                    players_text.append("\n")
            
            panel = Panel(
                Align.center(players_text),
                title=f"Pod {pod.id} ({pod.size} players)",
                border_style="bright_green"
            )
            rprint(panel)
        
        # Show statistics
        stats = self.pod_randomizer.get_statistics(pods)
        stats_text = f"Total: {stats['total_players']} players | {stats['total_pods']} pods | Avg: {stats['avg_pod_size']:.1f} per pod"
        self.console.print(Align.center(Text(stats_text, style="italic cyan")))
    
    def quick_randomize(self):
        """Quick randomize with current settings"""
        players = self.player_manager.get_players()
        if len(players) < 3:
            self.console.print("Need at least 3 players to create pods", style="red")
            Prompt.ask("Press Enter to continue")
            return
        
        pods = self.pod_randomizer.create_pods(
            players, 
            self.config['default_pod_size'], 
            self.config['max_pod_size']
        )
        
        self.display_pods(pods)
        
        if self.config['keep_history']:
            self.save_to_history(pods)
        
        Prompt.ask("Press Enter to continue")
    
    def save_to_history(self, pods: List[Pod]):
        """Save pod assignment to history"""
        from datetime import datetime
        
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "pods": [
                {
                    "id": pod.id,
                    "players": pod.players,
                    "size": pod.size
                }
                for pod in pods
            ]
        }
        
        history = self.data_storage.load_history()
        history.append(history_entry)
        
        # Keep only recent history items
        max_items = self.config['max_history_items']
        if len(history) > max_items:
            history = history[-max_items:]
        
        self.data_storage.save_history(history)
    
    def view_history(self):
        """View pod assignment history"""
        history = self.data_storage.load_history()
        
        if not history:
            self.console.print("No history available", style="yellow")
            Prompt.ask("Press Enter to continue")
            return
        
        self.console.print("Pod Assignment History:", style="bold blue")
        
        for i, entry in enumerate(reversed(history[-10:]), 1):  # Show last 10
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            pod_count = len(entry['pods'])
            player_count = sum(pod['size'] for pod in entry['pods'])
            
            self.console.print(f"{i}. {timestamp} - {pod_count} pods, {player_count} players", style="cyan")
        
        Prompt.ask("Press Enter to continue")
    
    def settings_menu(self):
        """Settings configuration"""
        while True:
            self.console.clear()
            self.console.print("Settings", style="bold blue")
            
            choices = ["1", "2", "3", "b"]
            choice = self.get_menu_choice(
                f"1) Default Pod Size: {self.config['default_pod_size']}  "
                f"2) Max Pod Size: {self.config['max_pod_size']}  "
                f"3) Keep History: {self.config['keep_history']}  b) Back",
                choices
            )
            
            if choice == "1":
                size = Prompt.ask(f"Default pod size (3-8)", default=str(self.config['default_pod_size']))
                try:
                    size = int(size)
                    size = max(3, min(size, 8))
                    self.config['default_pod_size'] = size
                    self.data_storage.save_config(self.config)
                    self.console.print(f"Default pod size set to {size}", style="green")
                except ValueError:
                    self.console.print("Invalid number", style="red")
                Prompt.ask("Press Enter to continue")
            elif choice == "2":
                size = Prompt.ask(f"Max pod size (4-8)", default=str(self.config['max_pod_size']))
                try:
                    size = int(size)
                    size = max(4, min(size, 8))
                    self.config['max_pod_size'] = size
                    self.data_storage.save_config(self.config)
                    self.console.print(f"Max pod size set to {size}", style="green")
                except ValueError:
                    self.console.print("Invalid number", style="red")
                Prompt.ask("Press Enter to continue")
            elif choice == "3":
                self.config['keep_history'] = not self.config['keep_history']
                self.data_storage.save_config(self.config)
                status = "enabled" if self.config['keep_history'] else "disabled"
                self.console.print(f"History keeping {status}", style="green")
                Prompt.ask("Press Enter to continue")
            elif choice == "b":
                break
    
    def data_menu(self):
        """Data management menu"""
        while True:
            self.console.clear()
            self.console.print("Data Management", style="bold blue")
            
            choices = ["1", "2", "3", "4", "b"]
            choice = self.get_menu_choice(
                "1) Create Backup  2) Restore Backup  3) Export Data  4) Import Data  b) Back",
                choices
            )
            
            if choice == "1":
                if self.data_storage.create_backup():
                    self.console.print("Backup created successfully", style="green")
                else:
                    self.console.print("Backup failed", style="red")
                Prompt.ask("Press Enter to continue")
            elif choice == "2":
                backups = self.data_storage.list_backups()
                if not backups:
                    self.console.print("No backups available", style="yellow")
                else:
                    self.console.print("Available backups:")
                    for i, backup in enumerate(backups, 1):
                        self.console.print(f"  {i}. {backup}")
                    
                    try:
                        choice_idx = int(Prompt.ask("Select backup number")) - 1
                        if 0 <= choice_idx < len(backups):
                            if self.data_storage.restore_backup(backups[choice_idx]):
                                self.console.print("Backup restored successfully", style="green")
                                # Reload data
                                self.player_manager.load_players()
                                self.config = self.data_storage.load_config()
                            else:
                                self.console.print("Restore failed", style="red")
                        else:
                            self.console.print("Invalid selection", style="red")
                    except ValueError:
                        self.console.print("Invalid number", style="red")
                Prompt.ask("Press Enter to continue")
            elif choice == "3":
                filename = Prompt.ask("Export filename", default="mtg_export.json")
                if self.data_storage.export_data(filename):
                    self.console.print(f"Data exported to {filename}", style="green")
                else:
                    self.console.print("Export failed", style="red")
                Prompt.ask("Press Enter to continue")
            elif choice == "4":
                filename = Prompt.ask("Import filename")
                merge = Confirm.ask("Merge with existing data? (default: replace)")
                if self.data_storage.import_data(filename, merge):
                    self.console.print("Data imported successfully", style="green")
                    # Reload data
                    self.player_manager.load_players()
                    self.config = self.data_storage.load_config()
                else:
                    self.console.print("Import failed", style="red")
                Prompt.ask("Press Enter to continue")
            elif choice == "b":
                break
    
    def show_statistics(self):
        """Show system statistics"""
        players = self.player_manager.get_players()
        history = self.data_storage.load_history()
        
        stats_text = Text()
        stats_text.append("System Statistics\n\n", style="bold white")
        stats_text.append(f"Current Players: {len(players)}\n", style="cyan")
        stats_text.append(f"History Entries: {len(history)}\n", style="cyan")
        stats_text.append(f"Default Pod Size: {self.config['default_pod_size']}\n", style="cyan")
        stats_text.append(f"Max Pod Size: {self.config['max_pod_size']}\n", style="cyan")
        
        if history:
            # Calculate some statistics from history
            total_assignments = len(history)
            avg_players_per_assignment = sum(
                len(entry['pods']) for entry in history
            ) / total_assignments if total_assignments > 0 else 0
            
            stats_text.append(f"\nHistory Stats:\n", style="bold yellow")
            stats_text.append(f"Total Assignments: {total_assignments}\n", style="green")
            stats_text.append(f"Avg Pods per Assignment: {avg_players_per_assignment:.1f}\n", style="green")
        
        panel = Panel(stats_text, title="Statistics", border_style="bright_blue")
        rprint(panel)
        Prompt.ask("Press Enter to continue")

def main():
    """Main entry point"""
    try:
        app = TerminalInterface()
        app.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()