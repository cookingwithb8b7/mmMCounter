# mmMCounter Testing Guide

This guide covers both automated unit tests and manual testing procedures for mmMCounter.

## Running Automated Tests

### Prerequisites
Install pytest (if not already installed):
```bash
pip install pytest pytest-cov
```

### Run All Tests
```bash
# From project root
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=src --cov-report=html
```

### Run Specific Test Files
```bash
pytest tests/test_timer.py -v
pytest tests/test_validators.py -v
pytest tests/test_config_manager.py -v
```

### Expected Results
All tests should pass. If any fail, review the error messages for details.

---

## Manual Testing Checklist

### 1. First Launch
- [ ] Application launches without errors
- [ ] Default profile is created automatically
- [ ] Main window is visible and always-on-top
- [ ] Window has proper title bar and controls

### 2. Timer Creation
- [ ] Click "Add Timer" button
- [ ] New timer appears in the list
- [ ] Default label is "New Timer"
- [ ] Default duration is 04:00 (4 minutes)
- [ ] Time displays as "04:00"

### 3. Timer Configuration
- [ ] Click "Config" button on a timer
- [ ] Configuration dialog opens centered on screen
- [ ] Can edit timer label
- [ ] Can set duration via minutes/seconds inputs
- [ ] Can capture hotkey using "Press keys..." button
- [ ] Can clear hotkey with "X" button
- [ ] Can configure visual alerts (checkboxes)
- [ ] Can configure audio alerts (file browser, volume slider)
- [ ] Changes save when clicking "OK"
- [ ] Changes cancel when clicking "Cancel"

### 4. Hotkey Capture (Critical!)
- [ ] Click "Press keys..." button
- [ ] Button text changes to "Listening... (Esc to cancel)"
- [ ] Press Ctrl+Shift+1
  - [ ] Displays as "ctrl+shift+1" (NOT "ctrl+shift+!")
- [ ] Press F13 (if you have a gaming mouse)
  - [ ] Displays as "f13"
- [ ] Press Page Up
  - [ ] Displays as "page_up"
- [ ] Press Insert
  - [ ] Displays as "insert"
- [ ] Press Escape to cancel
  - [ ] Previous hotkey value restored
- [ ] Click "X" to clear hotkey
  - [ ] Displays as "None"

### 5. Timer Operations
- [ ] Click "Start" button
  - [ ] Timer starts counting down
  - [ ] Button text changes to "Pause"
  - [ ] Time updates every second
- [ ] Click "Pause" button
  - [ ] Timer pauses
  - [ ] Button text changes to "Resume"
  - [ ] Time stops updating
- [ ] Click "Resume" button
  - [ ] Timer resumes from paused time
  - [ ] Button text changes to "Pause"
- [ ] Click "Reset" button
  - [ ] Timer resets to initial duration
  - [ ] Timer stops (state becomes STOPPED)
  - [ ] Button text changes to "Start"
- [ ] Let timer run to completion
  - [ ] Timer reaches 00:00
  - [ ] Time display turns red (alert color)
  - [ ] Button text changes to "Restart"

### 6. Global Hotkeys
- [ ] Configure a timer with hotkey "ctrl+shift+f13"
- [ ] Minimize mmMCounter or focus another app (e.g., Minecraft)
- [ ] Press the configured hotkey
  - [ ] Timer starts/pauses/resumes (depending on state)
  - [ ] Works even when app is not focused
- [ ] Try multiple timers with different hotkeys
  - [ ] Each hotkey controls only its assigned timer
  - [ ] No conflicts between hotkeys

### 7. Visual Alerts
Configure timer with flash options enabled:
- [ ] Flash numbers enabled
  - [ ] Time display flashes red when timer completes
  - [ ] Flashing alternates between red and normal color
- [ ] Flash background enabled
  - [ ] Timer row background flashes when timer completes
- [ ] Flash taskbar enabled
  - [ ] Windows taskbar icon flashes orange when timer completes

### 8. Audio Alerts
- [ ] Configure timer with audio enabled
- [ ] Browse and select sound file (or use default)
- [ ] Set volume to 80%
- [ ] Let timer complete
  - [ ] Sound plays at configured volume
  - [ ] Sound is audible and clear
- [ ] Set volume to 0%
  - [ ] Sound is silent
- [ ] Disable audio alert
  - [ ] No sound plays on completion

### 9. Multiple Timers
- [ ] Add 3 timers with different durations (1 min, 2 min, 3 min)
- [ ] Assign different hotkeys to each
- [ ] Start all three timers
  - [ ] All timers count down simultaneously
  - [ ] Each timer updates independently
- [ ] Let all timers complete
  - [ ] Each timer triggers its own alerts
  - [ ] Visual/audio alerts work correctly for each

### 10. Timer Deletion
- [ ] Create a timer
- [ ] Click "X" (delete) button
- [ ] Confirm deletion
  - [ ] Timer is removed from list
  - [ ] No errors occur

### 11. Profile Management
- [ ] Menu > Profiles > Manage Profiles
- [ ] Profile Manager dialog opens
- [ ] Create new profile:
  - [ ] Click "New" button
  - [ ] Enter profile name "PvP"
  - [ ] Profile appears in list
- [ ] Load profile:
  - [ ] Select "PvP" profile
  - [ ] Click "Load"
  - [ ] Current timers are saved to previous profile
  - [ ] New profile loads (empty timer list)
- [ ] Duplicate profile:
  - [ ] Select "default" profile
  - [ ] Click "Duplicate"
  - [ ] Enter name "Speedrun"
  - [ ] New profile created with same timers
- [ ] Rename profile:
  - [ ] Select "Speedrun" profile
  - [ ] Click "Rename"
  - [ ] Enter new name "Speedrun_Practice"
  - [ ] Profile name updated in list
- [ ] Export profile:
  - [ ] Select any profile
  - [ ] Click "Export"
  - [ ] Choose save location
  - [ ] JSON file created successfully
- [ ] Import profile:
  - [ ] Click "Import"
  - [ ] Select exported JSON file
  - [ ] Enter profile name
  - [ ] Profile imported successfully
- [ ] Delete profile:
  - [ ] Select non-default, non-active profile
  - [ ] Click "Delete"
  - [ ] Confirm deletion
  - [ ] Profile removed from list
  - [ ] Cannot delete "default" profile
  - [ ] Cannot delete currently active profile

### 12. Settings
- [ ] Menu > Settings
- [ ] Settings dialog opens
- [ ] Change theme:
  - [ ] Select "light" theme
  - [ ] Click "OK"
  - [ ] Notification about restart appears
  - [ ] Restart app
  - [ ] Light theme applied
- [ ] Test "high_contrast" theme:
  - [ ] Select "high_contrast"
  - [ ] Black background, yellow buttons visible
- [ ] Change "Always on top":
  - [ ] Uncheck "Always on top"
  - [ ] Click "OK"
  - [ ] Window can now be covered by other windows
- [ ] Configure default alerts:
  - [ ] Enable/disable visual alert options
  - [ ] Configure default audio settings
  - [ ] Changes apply to new timers

### 13. Tooltips
- [ ] Hover over "Start" button
  - [ ] Tooltip appears after ~500ms
  - [ ] Shows "Start/pause the timer (hotkey if configured)"
- [ ] Hover over "Reset" button
  - [ ] Shows "Reset timer to initial duration"
- [ ] Hover over "Config" button
  - [ ] Shows configuration description
- [ ] Hover over "X" button
  - [ ] Shows "Delete this timer"
- [ ] Move mouse away
  - [ ] Tooltip disappears

### 14. Dialog Positioning
- [ ] Move main window to top edge of screen
- [ ] Click "Config" on a timer
  - [ ] Dialog opens fully on-screen
  - [ ] Title bar is accessible and draggable
- [ ] Move main window to bottom-right corner
- [ ] Click "Config" on a timer
  - [ ] Dialog opens fully on-screen
  - [ ] No parts clipped off screen

### 15. Persistence
- [ ] Create several timers
- [ ] Configure each with labels, durations, hotkeys
- [ ] Close mmMCounter
- [ ] Relaunch mmMCounter
  - [ ] All timers restored
  - [ ] Labels, durations, hotkeys preserved
  - [ ] Last active profile loaded
  - [ ] Window position restored (approximately)

### 16. Edge Cases
- [ ] Try to create hotkey with only modifiers (ctrl+shift)
  - [ ] Error message: "must include at least one regular key"
- [ ] Try to assign same hotkey to two timers
  - [ ] Error message: "hotkey already in use"
- [ ] Try to save profile with empty name
  - [ ] Error message: "cannot be empty"
- [ ] Try to save profile with name "CON"
  - [ ] Error message: "reserved name"
- [ ] Set timer duration to 0 seconds
  - [ ] Error message: "must be greater than 0"
- [ ] Set audio volume to 101
  - [ ] Error message: "between 0 and 100"

### 17. Performance
- [ ] Create 10+ timers
- [ ] Start all timers simultaneously
  - [ ] UI remains responsive
  - [ ] Timers update smoothly (no lag)
  - [ ] CPU usage is reasonable (<5%)
- [ ] Let all timers complete
  - [ ] All alerts trigger correctly
  - [ ] No crashes or freezing

---

## Testing Results Template

Copy this template and fill in your test results:

```
Date: ___________
Tester: ___________
Python Version: ___________
OS: ___________

Automated Tests:
- test_timer.py: [ PASS / FAIL ]
- test_validators.py: [ PASS / FAIL ]
- test_config_manager.py: [ PASS / FAIL ]

Manual Tests:
- First Launch: [ PASS / FAIL ]
- Timer Creation: [ PASS / FAIL ]
- Timer Configuration: [ PASS / FAIL ]
- Hotkey Capture: [ PASS / FAIL ]
- Timer Operations: [ PASS / FAIL ]
- Global Hotkeys: [ PASS / FAIL ]
- Visual Alerts: [ PASS / FAIL ]
- Audio Alerts: [ PASS / FAIL ]
- Multiple Timers: [ PASS / FAIL ]
- Timer Deletion: [ PASS / FAIL ]
- Profile Management: [ PASS / FAIL ]
- Settings: [ PASS / FAIL ]
- Tooltips: [ PASS / FAIL ]
- Dialog Positioning: [ PASS / FAIL ]
- Persistence: [ PASS / FAIL ]
- Edge Cases: [ PASS / FAIL ]
- Performance: [ PASS / FAIL ]

Issues Found:
1.
2.
3.

Notes:


```

---

## Known Limitations

1. **Theme Changes**: Require app restart for full effect
2. **Hotkey Conflicts**: mmMCounter cannot detect system-level hotkey conflicts
3. **Audio Formats**: Only WAV and MP3 files supported
4. **Window Position**: May not restore correctly on multi-monitor setups
5. **F13-F24 Keys**: Require hardware that supports these keys (gaming mice/keyboards)

---

## Reporting Issues

If you find bugs during testing:

1. Note the exact steps to reproduce
2. Include Python version and OS
3. Check console output for error messages
4. Create GitHub issue with details
