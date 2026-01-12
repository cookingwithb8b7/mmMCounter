"""Main application window for mmMCounter."""

import tkinter as tk
from tkinter import messagebox
from typing import Dict
from src.core.timer import Timer
from src.core.timer_manager import TimerManager
from src.ui.timer_row import TimerRow
from src.ui.themes import Theme
from src.config.config_manager import ConfigManager
from src.config.defaults import DEFAULT_TIMER
import uuid


class MainWindow(tk.Tk):
    """
    Main application window.

    Features:
    - Always-on-top behavior
    - Scrollable timer rows
    - Add/remove timers dynamically
    - Menu bar for settings and profiles
    """

    def __init__(self, config_manager: ConfigManager, timer_manager: TimerManager):
        """
        Initialize main window.

        Args:
            config_manager: Configuration manager instance
            timer_manager: Timer manager instance
        """
        super().__init__()

        self.config_manager = config_manager
        self.timer_manager = timer_manager
        self.timer_rows: Dict[str, TimerRow] = {}  # timer_id -> TimerRow

        # Load app state
        self.app_state = config_manager.load_app_state()
        self.current_profile_name = self.app_state.get("last_active_profile", "default")

        # Load theme from profile
        profile = config_manager.load_profile(self.current_profile_name)
        theme_name = "dark"
        if profile:
            theme_name = profile.get("global_settings", {}).get("theme", "dark")

        self.theme = Theme(theme_name)

        # Window setup
        self.title("mmMCounter")
        self.configure(bg=self.theme.bg_color)

        # Always on top
        self.attributes('-topmost', True)

        # Window size (start compact)
        self.geometry("480x300")
        self.resizable(True, True)

        # Create UI
        self._create_menu()
        self._create_toolbar()
        self._create_scrollable_frame()

        # Set up timer callbacks
        self.timer_manager.set_on_timer_tick(self._on_timer_tick)
        self.timer_manager.set_on_timer_complete(self._on_timer_complete)

        # Load timers from profile
        self._load_profile(self.current_profile_name)

        # Start timer update loop
        self.timer_manager.start()

        # Update UI every 100ms
        self._schedule_ui_update()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Profile", command=self._save_current_profile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)

        # Profiles menu (placeholder for Phase 4)
        profiles_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Profiles", menu=profiles_menu)
        profiles_menu.add_command(label="Manage Profiles...", command=self._show_profile_manager)

        # Settings menu (placeholder for Phase 4)
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences...", command=self._show_settings)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

    def _create_toolbar(self):
        """Create toolbar with Add Timer button."""
        toolbar = tk.Frame(self, bg=self.theme.bg_color)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        add_button = tk.Button(
            toolbar,
            text="+ Add Timer",
            command=self._add_timer
        )
        self.theme.apply_to_widget(add_button, "button")
        add_button.pack(side=tk.LEFT, padx=2)

    def _create_scrollable_frame(self):
        """Create scrollable frame for timer rows."""
        # Container frame
        container = tk.Frame(self, bg=self.theme.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Canvas for scrolling
        self.canvas = tk.Canvas(container, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.theme.bg_color)

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _add_timer(self):
        """Add a new timer."""
        # Create new timer with default values
        new_timer = Timer(
            label=f"Timer {len(self.timer_manager) + 1}",
            duration=DEFAULT_TIMER["duration_seconds"],
            timer_id=str(uuid.uuid4())
        )

        # Add to manager
        self.timer_manager.add_timer(new_timer)

        # Create timer row widget
        self._create_timer_row(new_timer)

    def _create_timer_row(self, timer: Timer):
        """
        Create a timer row widget for a timer.

        Args:
            timer: Timer instance
        """
        row = TimerRow(
            self.scrollable_frame,
            timer,
            self.theme,
            on_config_click=self._on_timer_config,
            on_delete_click=self._on_timer_delete
        )
        row.pack(fill=tk.X, padx=2, pady=2)

        self.timer_rows[timer.id] = row

    def _on_timer_config(self, timer_id: str):
        """
        Handle timer config button click.

        Args:
            timer_id: ID of timer to configure
        """
        # Placeholder for Phase 4
        messagebox.showinfo("Config", f"Timer configuration dialog\n(Phase 4)")

    def _on_timer_delete(self, timer_id: str):
        """
        Handle timer delete button click.

        Args:
            timer_id: ID of timer to delete
        """
        # Remove from UI
        if timer_id in self.timer_rows:
            self.timer_rows[timer_id].destroy()
            del self.timer_rows[timer_id]

        # Remove from manager
        self.timer_manager.remove_timer(timer_id)

    def _on_timer_tick(self, timer: Timer):
        """
        Handle timer tick event.

        Args:
            timer: Timer that ticked
        """
        # UI update is handled by scheduled update
        pass

    def _on_timer_complete(self, timer: Timer):
        """
        Handle timer completion event.

        Args:
            timer: Timer that completed
        """
        # Placeholder for Phase 3 (alerts)
        print(f"Timer completed: {timer.label}")

    def _schedule_ui_update(self):
        """Schedule periodic UI updates."""
        # Update all timer row displays
        for timer_row in self.timer_rows.values():
            timer_row.update_display()

        # Schedule next update (100ms)
        self.after(100, self._schedule_ui_update)

    def _load_profile(self, profile_name: str):
        """
        Load a profile and populate timers.

        Args:
            profile_name: Name of profile to load
        """
        profile = self.config_manager.load_profile(profile_name)
        if not profile:
            print(f"Profile '{profile_name}' not found, creating default")
            self.config_manager.create_default_profile()
            profile = self.config_manager.load_profile("default")

        # Clear existing timers
        for timer_id in list(self.timer_rows.keys()):
            self._on_timer_delete(timer_id)

        # Load timers from profile
        timer_data_list = profile.get("timers", [])
        self.timer_manager.load_from_dict_list(timer_data_list)

        # Create UI rows for each timer
        for timer in self.timer_manager.get_all_timers():
            self._create_timer_row(timer)

    def _save_current_profile(self):
        """Save current timers to active profile."""
        profile = self.config_manager.load_profile(self.current_profile_name)
        if profile:
            # Update timers in profile
            profile["timers"] = self.timer_manager.to_dict_list()

            # Save profile
            if self.config_manager.save_profile(self.current_profile_name, profile):
                messagebox.showinfo("Success", f"Profile '{self.current_profile_name}' saved")
            else:
                messagebox.showerror("Error", "Failed to save profile")

    def _show_profile_manager(self):
        """Show profile manager dialog (Phase 4)."""
        messagebox.showinfo("Profiles", "Profile manager\n(Phase 4)")

    def _show_settings(self):
        """Show settings dialog (Phase 4)."""
        messagebox.showinfo("Settings", "Settings dialog\n(Phase 4)")

    def _show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About mmMCounter",
            "mmMCounter v0.1.0\nMoney-Making-Meta Counter\n\n"
            "A lightweight timer for Minecraft item cooldowns\n\n"
            "https://github.com/cookingwithb8b7/mmMCounter"
        )

    def _on_close(self):
        """Handle window close event."""
        # Save current profile
        self._save_current_profile()

        # Save app state
        self.app_state["last_active_profile"] = self.current_profile_name
        # Window position would be saved here
        self.config_manager.save_app_state(self.app_state)

        # Stop timer manager
        self.timer_manager.stop()

        # Close window
        self.destroy()
