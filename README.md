# mmMCounter (Money-Making-Meta Counter)

A lightweight, accessible timer application for tracking Minecraft item cooldowns with advanced hotkey support and customizable alerts.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## Features

### ⏱️ Multiple Timers
- Create unlimited timers with custom labels and durations
- Individual configuration for each timer
- Start, pause, resume, and reset controls
- Real-time countdown display (MM:SS format)
- Visual state indicators (running, paused, completed)

### ⌨️ Global Hotkeys
- Control timers even when Minecraft is focused (no admin rights required)
- Advanced key support:
  - **F13-F24** keys (perfect for gaming mice with extra buttons)
  - **Navigation keys**: Page Up, Page Down, Home, End, Insert, Delete
  - **Arrow keys**: Up, Down, Left, Right
  - **Numpad keys** and operators
  - **Standard keys** with modifiers (Ctrl, Shift, Alt)
- Smart hotkey capture with physical key detection
- No conflicts with Minecraft controls

### 🔔 Customizable Alerts
**Visual Alerts:**
- Flash timer numbers in alert color
- Flash timer row background
- Flash Windows taskbar icon

**Audio Alerts:**
- Custom sound file support (WAV/MP3)
- Volume control (0-100%)
- Default two-tone beep included

### 💾 Profile Management
- Save multiple timer configurations for different scenarios
- Quick profile switching
- Profile import/export (JSON format)
- Duplicate profiles for easy customization
- Auto-save on exit

### 🎨 Themes & Accessibility
- **Dark mode** (default): Easy on the eyes during long sessions
- **Light mode**: For brighter environments
- **High contrast mode**: Yellow text on black for maximum visibility
- **Tooltips**: Hover hints on all buttons
- **OpenDyslexic** font support (installation guide included)
- **Always-on-top** window option

### 🖥️ User Interface
- Clean, intuitive layout
- Per-timer configuration dialogs
- Smart dialog positioning (never off-screen)
- Window position persistence
- Minimal resource usage (<5% CPU with 10+ timers)

## Installation

### From Source

**Prerequisites:**
- Python 3.11 or higher
- Windows OS (currently)

**Steps:**
```bash
# Clone the repository
git clone git@github.com:cookingwithb8b7/mmMCounter.git
cd mmMCounter

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### From Executable (Coming Soon)

Download the latest release from the [Releases](https://github.com/cookingwithb8b7/mmMCounter/releases) page and run `mmMCounter.exe`.

## Quick Start

1. **Launch mmMCounter**
   - Run `python src/main.py` (or double-click `mmMCounter.exe`)
   - Window appears always-on-top by default

2. **Create Your First Timer**
   - Click "Add Timer"
   - Click "Config" to customize

3. **Configure Timer**
   - Set a label (e.g., "Pearl", "Chorus", "Gapple")
   - Set duration (minutes and seconds)
   - Click "Press keys..." to assign a hotkey
   - Configure visual/audio alerts
   - Click "OK"

4. **Use Hotkeys**
   - Focus Minecraft
   - Press your configured hotkey to start/pause the timer
   - Timer works in the background

5. **Save Your Setup**
   - File > Save Profile
   - Your timers are auto-saved on exit

## Usage Examples

### Speedrunning Setup
```
Timer 1: "Pearl" (4:00) - Hotkey: F13
Timer 2: "Bed" (5:00) - Hotkey: F14
Timer 3: "Eye" (0:45) - Hotkey: F15
```

### PvP Setup
```
Timer 1: "Totem" (0:01) - Hotkey: Ctrl+Shift+1
Timer 2: "Gapple" (0:30) - Hotkey: Ctrl+Shift+2
Timer 3: "Chorus" (1:00) - Hotkey: Ctrl+Shift+3
```

### Using Gaming Mouse Buttons
- Map your mouse side buttons to F13-F24 in your mouse software
- Assign these F-keys as hotkeys in mmMCounter
- Press mouse buttons to control timers while playing

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Add Timer | File > Add Timer |
| Save Profile | File > Save Profile |
| Profile Manager | File > Profiles > Manage |
| Settings | File > Settings |
| Close | Alt+F4 or window X |

## Profile Management

### Creating Profiles
1. File > Profiles > Manage Profiles
2. Click "New"
3. Enter profile name (e.g., "PvP", "Speedrun")
4. Profile is created with current global settings

### Switching Profiles
1. File > Profiles > Manage Profiles
2. Select profile
3. Click "Load"
4. Current profile is auto-saved before switch

### Exporting Profiles
1. Open Profile Manager
2. Select profile
3. Click "Export"
4. Choose save location
5. Share the JSON file with friends

### Importing Profiles
1. Open Profile Manager
2. Click "Import"
3. Select JSON file
4. Enter new profile name
5. Profile is ready to use

## Settings

### Theme Options
- **Dark**: Default dark theme
- **Light**: Light background with dark text
- **High Contrast**: Black background with yellow text

*Note: Theme changes require application restart for full effect*

### Always On Top
Toggle whether mmMCounter stays above other windows.

### Default Alert Configuration
Set default visual and audio alert preferences for new timers.

## Accessibility

### For Dyslexic Users
- OpenDyslexic font support
- Installation guide in `assets/fonts/README.md`
- Clear, consistent layout

### For Visually Impaired Users
- High contrast theme
- Large timer display (16pt bold)
- Customizable alert colors
- Tooltips on all interactive elements

### For Motor Impairment
- Large clickable buttons
- Keyboard navigation support
- Hotkey alternatives to clicking

## Building from Source

### Creating an Executable

```bash
# Install PyInstaller
pip install pyinstaller==6.3.0

# Build executable
pyinstaller --name=mmMCounter \
            --onefile \
            --windowed \
            --icon=assets/icon.ico \
            --add-data="assets;assets" \
            src/main.py

# Executable will be in dist/mmMCounter.exe
```

## Testing

### Running Unit Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_timer.py -v
```

### Manual Testing
See `tests/TESTING_GUIDE.md` for comprehensive manual testing checklist.

## Troubleshooting

### Hotkeys Not Working
- Ensure pynput is installed: `pip install pynput==1.7.6`
- Check for hotkey conflicts with other applications
- Run with Python 3.11 (not 3.13): `py -3.11 src/main.py`
- Verify hotkey is registered (check timer config)

### Sound Not Playing
- Install pygame: `pip install pygame==2.5.2`
- Check audio file format (WAV or MP3 only)
- Verify volume is not set to 0
- Test with default sound: `assets/sounds/default_alert.wav`

### Timer Display Issues
- Check theme settings (try switching themes)
- Verify window is not minimized
- Restart application if UI becomes unresponsive

### Profile Not Saving
- Check write permissions in config directory
- Look for error messages in console
- Try exporting profile manually

## Development

### Project Structure
```
mmMCounter/
├── src/
│   ├── core/           # Core timer logic and managers
│   ├── ui/             # UI components and dialogs
│   ├── config/         # Configuration and defaults
│   └── utils/          # Utilities and validators
├── tests/              # Unit tests and testing guide
├── assets/
│   ├── sounds/         # Default alert sound
│   └── fonts/          # Font installation guide
├── scripts/            # Utility scripts
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Follow existing code style
5. Submit a pull request

### Running Tests Before Commit
```bash
pytest tests/ -v
```

## Known Limitations

1. **Windows Only**: Currently supports Windows only (Linux/macOS planned)
2. **Theme Changes**: Require application restart for full effect
3. **F13-F24 Keys**: Require hardware that supports these keys
4. **Hotkey Conflicts**: Cannot detect system-level hotkey conflicts
5. **Audio Formats**: Only WAV and MP3 supported

## Roadmap

- [ ] Linux support
- [ ] macOS support
- [ ] Hotkey conflict detection
- [ ] Custom alert animations
- [ ] Timer groups and categories
- [ ] Statistics and usage tracking
- [ ] Cloud profile sync
- [ ] Multi-language support

## Credits

**Developer:** cookingwithb8b7
**AI Assistant:** Claude Sonnet 4.5 (Anthropic)
**License:** MIT License

### Libraries Used
- [pynput](https://github.com/moses-palmer/pynput) - Global hotkey support
- [pygame](https://www.pygame.org/) - Audio playback
- [PyInstaller](https://pyinstaller.org/) - Executable bundling

### Special Thanks
- Minecraft speedrunning community for inspiration
- Beta testers and early users

## License

MIT License - See [LICENSE](LICENSE) for full details.

## Support

- **Issues**: [GitHub Issues](https://github.com/cookingwithb8b7/mmMCounter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cookingwithb8b7/mmMCounter/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Note:** This is a community tool for Minecraft players. Not affiliated with Mojang or Microsoft.

**Made with ❤️ for the Minecraft community**
