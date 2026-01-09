# mtg-pod-utility
# MTG Pod Randomizer

A cross-platform system for randomly assigning Magic: The Gathering players to pods. Works on desktop, mobile terminals, and web browsers with full offline capability.

## Features

### 🎯 Core Functionality
- **Random Pod Assignment**: Intelligent algorithm for balanced pod distribution
- **Flexible Pod Sizes**: Support for 3-8 players per pod
- **Player Management**: Add, remove, search, and organize players
- **History Tracking**: Keep records of past pod assignments
- **Data Persistence**: Automatic saving and backup capabilities

### 📱 Cross-Platform Support
- **Desktop Terminal**: Rich, colorful interface for desktop use
- **Mobile Terminal**: Compatible with Termux (Android) and iSH (iOS)
- **Web Interface**: Progressive Web App with offline support
- **Data Sync**: Share data between all interfaces

### 🛠 Advanced Features
- **Import/Export**: Transfer data between devices
- **Backup/Restore**: Protect your player data
- **Bulk Operations**: Add multiple players at once
- **Statistics**: Track pod assignment patterns
- **Customizable Settings**: Configure pod sizes and preferences

## Quick Start

### Desktop Setup

1. **Download/Clone** the project to your desktop
2. **Install dependencies**:
   ```bash
   pip install rich
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

### Mobile Setup

#### Android (Termux)
1. **Install Termux** from F-Droid or Play Store
2. **Install Python**:
   ```bash
   pkg update && pkg upgrade
   pkg install python
   ```
3. **Copy project files** to Termux storage
4. **Install rich library**:
   ```bash
   pip install rich
   ```
5. **Run the application**:
   ```bash
   python main.py
   ```

#### iOS (iSH Shell)
1. **Install iSH Shell** from App Store
2. **Install Python**:
   ```bash
   apk update && apk upgrade
   apk add python3 py3-pip
   ```
3. **Copy project files** to iSH storage
4. **Install rich library**:
   ```bash
   pip3 install rich
   ```
5. **Run the application**:
   ```bash
   python3 main.py
   ```

### Web Interface

1. **Start the web server**:
   ```bash
   python main.py
   ```
2. **Select option 2** for Web Interface
3. **Open browser** to http://localhost:8000
4. **Install as PWA**: Use browser's "Add to Home Screen" feature

## Project Structure

```
mtg_pod_system/
├── main.py                     # Main entry point
├── core/                       # Core functionality
│   ├── player_manager.py       # Player management
│   ├── pod_randomizer.py       # Randomization algorithm
│   └── data_storage.py         # Data persistence
├── interfaces/                 # User interfaces
│   └── terminal_app.py         # Terminal interface
├── mobile_web/                 # Progressive Web App
│   ├── index.html             # Web app entry point
│   ├── css/style.css          # Styling
│   ├── js/app.js              # Web app logic
│   ├── manifest.json          # PWA manifest
│   └── sw.js                  # Service worker
├── utils/                      # Utility modules
│   └── sync_utils.py          # Data synchronization
└── data/                       # Data storage
    ├── players.json           # Player database
    ├── config.json            # User settings
    └── history.json           # Assignment history
```

## Usage Guide

### Terminal Interface

1. **Main Menu Options**:
   - `1` - Manage Players: Add/remove players
   - `2` - Create Random Pods: Generate pod assignments
   - `3` - View History: See past assignments
   - `4` - Settings: Configure pod sizes
   - `5` - Data Management: Backup/restore data
   - `6` - Statistics: View system stats
   - `7` - Quick Randomize: Fast pod creation
   - `q` - Quit: Exit application

2. **Player Management**:
   - Add single or multiple players
   - Remove players by name
   - Search for specific players
   - Clear all players

3. **Pod Creation**:
   - Choose target pod size (3-8 players)
   - System automatically balances distribution
   - Handle odd numbers intelligently
   - View detailed pod assignments

### Web Interface

1. **Player Management**:
   - Add players individually or in bulk
   - Remove players with one click
   - Real-time player count display

2. **Pod Configuration**:
   - Set target pod size
   - Configure maximum pod size
   - Settings persist between sessions

3. **Randomization**:
   - One-click pod creation
   - Visual pod display with color coding
   - Statistics and summary information

4. **Data Management**:
   - Export data to JSON files
   - Import data from other devices
   - Clear all data option

### Mobile Terminal Use

1. **Touch Optimization**:
   - Large text for better readability
   - Simple keyboard navigation
   - Clear menu options

2. **Offline Capability**:
   - Works without internet connection
   - All data stored locally
   - Full feature set available offline

## Data Synchronization

### Between Interfaces

1. **Automatic Sync**:
   - All interfaces use the same data files
   - Changes reflected across all interfaces
   - No manual sync required for local use

2. **Export/Import**:
   - Export data from any interface
   - Import to another device/interface
   - Merge or replace existing data

3. **Cross-Platform Sharing**:
   - JSON format works everywhere
   - Email, cloud storage, or direct file transfer
   - Preserves all data and settings

## Advanced Features

### Backup Strategies

1. **Automatic Backups**:
   - Created automatically when using data management
   - Timestamped backup folders
   - Restore from any backup point

2. **Manual Exports**:
   - Export complete system state
   - Include players, history, and settings
   - Perfect for migrating to new devices

### Pod Algorithm

The system uses a balanced distribution algorithm:

1. **Random Shuffle**: All players are randomly shuffled
2. **Optimal Distribution**: Calculates best pod configuration
3. **Remainder Handling**: Distributes extra players fairly
4. **Size Constraints**: Respects min/max pod size limits

### Settings Configuration

- **Default Pod Size**: Preferred pod size (default: 4)
- **Maximum Pod Size**: Largest allowed pod (default: 8)
- **History Tracking**: Enable/disable history saving
- **Auto-save**: Automatically save changes

## Troubleshooting

### Common Issues

1. **Python Not Found**:
   - Install Python 3.7 or higher
   - Ensure Python is in system PATH

2. **Rich Library Error**:
   - Install with: `pip install rich`
   - For mobile: `pip install rich` in terminal app

3. **Port Already in Use**:
   - Web interface auto-finds available ports 8000-8999
   - Manually specify port if needed

4. **File Permission Issues**:
   - Ensure write permissions in project directory
   - On mobile, check storage permissions

### Mobile-Specific Issues

1. **Termux Performance**:
   - Update Termux packages regularly
   - Use `pkg upgrade` for latest fixes

2. **iSH Limitations**:
   - iSH has slower performance
   - Consider using alternative terminal apps

3. **Storage Access**:
   - Android: Grant Termux storage permissions
   - iOS: Use Files app for file management

## Development

### Adding New Features

1. **Core Logic**: Add to appropriate core module
2. **Terminal Interface**: Update `terminal_app.py`
3. **Web Interface**: Modify `app.js` and `style.css`
4. **Data Storage**: Update `data_storage.py` for new data types

### Testing

1. **Unit Tests**: Test individual modules
2. **Integration Tests**: Test interface interactions
3. **Cross-Platform**: Test on all target platforms

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review the documentation
3. Create an issue in the repository

---

**MTG Pod Randomizer** - Making pod assignments simple and fair for every game night!

-- Zarrotox
