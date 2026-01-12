"""Profile manager dialog for managing timer profiles."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import Optional, Callable
from src.ui.themes import Theme
from src.config.config_manager import ConfigManager
from src.utils.validators import validate_profile_name, sanitize_filename


class ProfileManagerDialog:
    """
    Modal dialog for managing profiles.

    Features:
    - List all profiles
    - Create new profile
    - Rename profile
    - Delete profile
    - Duplicate profile
    - Export/import profiles
    - Switch active profile
    """

    def __init__(
        self,
        parent: tk.Tk,
        config_manager: ConfigManager,
        current_profile: str,
        theme: Theme,
        on_profile_switch: Optional[Callable[[str], None]] = None
    ):
        """
        Initialize profile manager dialog.

        Args:
            parent: Parent window
            config_manager: Configuration manager instance
            current_profile: Currently active profile name
            theme: Current theme
            on_profile_switch: Callback when profile is switched (receives profile_name)
        """
        self.parent = parent
        self.config_manager = config_manager
        self.current_profile = current_profile
        self.theme = theme
        self.on_profile_switch = on_profile_switch
        self.selected_profile: Optional[str] = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Profile Manager")
        self.dialog.configure(bg=theme.bg_color)
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)

        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Build UI
        self._build_ui()

        # Load profiles
        self._refresh_profile_list()

        # Center on parent
        self._center_on_parent()

    def _build_ui(self):
        """Build the profile manager UI."""
        # Main container
        main_frame = tk.Frame(self.dialog, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header
        header_label = tk.Label(
            main_frame,
            text="Manage Profiles",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 12, "bold")
        )
        header_label.pack(anchor=tk.W, pady=(0, 10))

        # Profile list frame
        list_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.profile_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 10),
            height=10
        )
        self.profile_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.profile_listbox.yview)

        # Bind selection event
        self.profile_listbox.bind('<<ListboxSelect>>', self._on_profile_select)
        self.profile_listbox.bind('<Double-Button-1>', self._on_load_profile)

        # Action buttons frame
        action_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        action_frame.pack(fill=tk.X, pady=10)

        # Left side buttons (profile actions)
        left_buttons = tk.Frame(action_frame, bg=self.theme.bg_color)
        left_buttons.pack(side=tk.LEFT)

        new_btn = tk.Button(
            left_buttons,
            text="New",
            command=self._on_new_profile,
            width=10
        )
        self.theme.apply_to_widget(new_btn, "button")
        new_btn.pack(side=tk.LEFT, padx=2)

        self.load_btn = tk.Button(
            left_buttons,
            text="Load",
            command=self._on_load_profile,
            width=10,
            state="disabled"
        )
        self.theme.apply_to_widget(self.load_btn, "button")
        self.load_btn.pack(side=tk.LEFT, padx=2)

        self.rename_btn = tk.Button(
            left_buttons,
            text="Rename",
            command=self._on_rename_profile,
            width=10,
            state="disabled"
        )
        self.theme.apply_to_widget(self.rename_btn, "button")
        self.rename_btn.pack(side=tk.LEFT, padx=2)

        self.duplicate_btn = tk.Button(
            left_buttons,
            text="Duplicate",
            command=self._on_duplicate_profile,
            width=10,
            state="disabled"
        )
        self.theme.apply_to_widget(self.duplicate_btn, "button")
        self.duplicate_btn.pack(side=tk.LEFT, padx=2)

        # Second row of action buttons
        action_frame2 = tk.Frame(main_frame, bg=self.theme.bg_color)
        action_frame2.pack(fill=tk.X, pady=(0, 10))

        left_buttons2 = tk.Frame(action_frame2, bg=self.theme.bg_color)
        left_buttons2.pack(side=tk.LEFT)

        self.delete_btn = tk.Button(
            left_buttons2,
            text="Delete",
            command=self._on_delete_profile,
            width=10,
            state="disabled"
        )
        self.theme.apply_to_widget(self.delete_btn, "button")
        self.delete_btn.pack(side=tk.LEFT, padx=2)

        self.export_btn = tk.Button(
            left_buttons2,
            text="Export",
            command=self._on_export_profile,
            width=10,
            state="disabled"
        )
        self.theme.apply_to_widget(self.export_btn, "button")
        self.export_btn.pack(side=tk.LEFT, padx=2)

        import_btn = tk.Button(
            left_buttons2,
            text="Import",
            command=self._on_import_profile,
            width=10
        )
        self.theme.apply_to_widget(import_btn, "button")
        import_btn.pack(side=tk.LEFT, padx=2)

        # Close button
        close_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        close_frame.pack(fill=tk.X)

        close_btn = tk.Button(
            close_frame,
            text="Close",
            command=self.dialog.destroy,
            width=10
        )
        self.theme.apply_to_widget(close_btn, "button")
        close_btn.pack(side=tk.RIGHT)

    def _refresh_profile_list(self):
        """Refresh the profile listbox."""
        self.profile_listbox.delete(0, tk.END)

        profiles = self.config_manager.list_profiles()

        for profile in profiles:
            display_text = profile
            if profile == self.current_profile:
                display_text += " (active)"

            self.profile_listbox.insert(tk.END, display_text)

    def _on_profile_select(self, event):
        """Handle profile selection."""
        selection = self.profile_listbox.curselection()
        if selection:
            idx = selection[0]
            profile_text = self.profile_listbox.get(idx)
            # Remove " (active)" suffix if present
            self.selected_profile = profile_text.replace(" (active)", "")

            # Enable buttons
            self.load_btn.config(state="normal")
            self.rename_btn.config(state="normal")
            self.duplicate_btn.config(state="normal")
            self.export_btn.config(state="normal")

            # Enable delete only if not default profile
            if self.selected_profile != "default":
                self.delete_btn.config(state="normal")
            else:
                self.delete_btn.config(state="disabled")
        else:
            self.selected_profile = None
            self.load_btn.config(state="disabled")
            self.rename_btn.config(state="disabled")
            self.duplicate_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
            self.export_btn.config(state="disabled")

    def _on_new_profile(self):
        """Create a new profile."""
        name = simpledialog.askstring(
            "New Profile",
            "Enter profile name:",
            parent=self.dialog
        )

        if not name:
            return

        # Validate name
        is_valid, error_msg = validate_profile_name(name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg, parent=self.dialog)
            return

        # Check if profile already exists
        if self.config_manager.load_profile(name) is not None:
            messagebox.showerror(
                "Profile Exists",
                f"Profile '{name}' already exists",
                parent=self.dialog
            )
            return

        # Create new profile from current active profile as template
        current_config = self.config_manager.load_profile(self.current_profile)
        if current_config:
            # Clear timers for new profile
            current_config["timers"] = []
            current_config["profile_name"] = name

            if self.config_manager.save_profile(name, current_config):
                messagebox.showinfo(
                    "Success",
                    f"Profile '{name}' created",
                    parent=self.dialog
                )
                self._refresh_profile_list()
            else:
                messagebox.showerror(
                    "Error",
                    f"Failed to create profile '{name}'",
                    parent=self.dialog
                )

    def _on_load_profile(self, event=None):
        """Load selected profile."""
        if not self.selected_profile:
            return

        if self.selected_profile == self.current_profile:
            messagebox.showinfo(
                "Already Active",
                f"Profile '{self.selected_profile}' is already active",
                parent=self.dialog
            )
            return

        # Call profile switch callback
        if self.on_profile_switch:
            self.on_profile_switch(self.selected_profile)
            self.current_profile = self.selected_profile
            self._refresh_profile_list()

            messagebox.showinfo(
                "Profile Loaded",
                f"Switched to profile '{self.selected_profile}'",
                parent=self.dialog
            )

    def _on_rename_profile(self):
        """Rename selected profile."""
        if not self.selected_profile:
            return

        # Cannot rename default profile
        if self.selected_profile == "default":
            messagebox.showwarning(
                "Cannot Rename",
                "The default profile cannot be renamed",
                parent=self.dialog
            )
            return

        new_name = simpledialog.askstring(
            "Rename Profile",
            f"Enter new name for '{self.selected_profile}':",
            parent=self.dialog,
            initialvalue=self.selected_profile
        )

        if not new_name or new_name == self.selected_profile:
            return

        # Validate name
        is_valid, error_msg = validate_profile_name(new_name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg, parent=self.dialog)
            return

        # Check if new name already exists
        if self.config_manager.load_profile(new_name) is not None:
            messagebox.showerror(
                "Profile Exists",
                f"Profile '{new_name}' already exists",
                parent=self.dialog
            )
            return

        # Load old profile, save as new name, delete old
        old_config = self.config_manager.load_profile(self.selected_profile)
        if old_config:
            old_config["profile_name"] = new_name

            if self.config_manager.save_profile(new_name, old_config):
                self.config_manager.delete_profile(self.selected_profile)

                # Update current profile if renamed
                if self.selected_profile == self.current_profile:
                    self.current_profile = new_name
                    if self.on_profile_switch:
                        self.on_profile_switch(new_name)

                messagebox.showinfo(
                    "Success",
                    f"Profile renamed to '{new_name}'",
                    parent=self.dialog
                )
                self._refresh_profile_list()
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to rename profile",
                    parent=self.dialog
                )

    def _on_duplicate_profile(self):
        """Duplicate selected profile."""
        if not self.selected_profile:
            return

        new_name = simpledialog.askstring(
            "Duplicate Profile",
            f"Enter name for copy of '{self.selected_profile}':",
            parent=self.dialog,
            initialvalue=f"{self.selected_profile}_copy"
        )

        if not new_name:
            return

        # Validate name
        is_valid, error_msg = validate_profile_name(new_name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg, parent=self.dialog)
            return

        # Check if new name already exists
        if self.config_manager.load_profile(new_name) is not None:
            messagebox.showerror(
                "Profile Exists",
                f"Profile '{new_name}' already exists",
                parent=self.dialog
            )
            return

        # Load and duplicate
        config = self.config_manager.load_profile(self.selected_profile)
        if config:
            config["profile_name"] = new_name

            if self.config_manager.save_profile(new_name, config):
                messagebox.showinfo(
                    "Success",
                    f"Profile duplicated as '{new_name}'",
                    parent=self.dialog
                )
                self._refresh_profile_list()
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to duplicate profile",
                    parent=self.dialog
                )

    def _on_delete_profile(self):
        """Delete selected profile."""
        if not self.selected_profile:
            return

        # Cannot delete default profile
        if self.selected_profile == "default":
            messagebox.showwarning(
                "Cannot Delete",
                "The default profile cannot be deleted",
                parent=self.dialog
            )
            return

        # Cannot delete active profile
        if self.selected_profile == self.current_profile:
            messagebox.showwarning(
                "Cannot Delete",
                "Cannot delete the active profile. Switch to another profile first.",
                parent=self.dialog
            )
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete profile '{self.selected_profile}'?\nThis cannot be undone.",
            parent=self.dialog
        )

        if confirm:
            if self.config_manager.delete_profile(self.selected_profile):
                messagebox.showinfo(
                    "Success",
                    f"Profile '{self.selected_profile}' deleted",
                    parent=self.dialog
                )
                self.selected_profile = None
                self._refresh_profile_list()
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to delete profile",
                    parent=self.dialog
                )

    def _on_export_profile(self):
        """Export selected profile to file."""
        if not self.selected_profile:
            return

        filename = filedialog.asksaveasfilename(
            parent=self.dialog,
            title="Export Profile",
            defaultextension=".json",
            initialfile=f"{self.selected_profile}.json",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        if filename:
            if self.config_manager.export_profile(self.selected_profile, filename):
                messagebox.showinfo(
                    "Success",
                    f"Profile exported to:\n{filename}",
                    parent=self.dialog
                )
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to export profile",
                    parent=self.dialog
                )

    def _on_import_profile(self):
        """Import profile from file."""
        filename = filedialog.askopenfilename(
            parent=self.dialog,
            title="Import Profile",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        if not filename:
            return

        # Ask for profile name
        import os
        default_name = os.path.splitext(os.path.basename(filename))[0]
        default_name = sanitize_filename(default_name)

        new_name = simpledialog.askstring(
            "Import Profile",
            "Enter name for imported profile:",
            parent=self.dialog,
            initialvalue=default_name
        )

        if not new_name:
            return

        # Validate name
        is_valid, error_msg = validate_profile_name(new_name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg, parent=self.dialog)
            return

        # Check if profile already exists
        if self.config_manager.load_profile(new_name) is not None:
            overwrite = messagebox.askyesno(
                "Profile Exists",
                f"Profile '{new_name}' already exists.\nOverwrite?",
                parent=self.dialog
            )
            if not overwrite:
                return

        # Import
        if self.config_manager.import_profile(filename, new_name):
            messagebox.showinfo(
                "Success",
                f"Profile imported as '{new_name}'",
                parent=self.dialog
            )
            self._refresh_profile_list()
        else:
            messagebox.showerror(
                "Error",
                "Failed to import profile. File may be corrupted or invalid.",
                parent=self.dialog
            )

    def _center_on_parent(self):
        """Center dialog on parent window with screen bounds checking."""
        self.dialog.update_idletasks()

        # Get parent position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        # Get dialog size
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        # Get screen dimensions
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()

        # Clamp to screen bounds
        x = max(0, min(x, screen_width - dialog_width))
        y = max(0, min(y, screen_height - dialog_height))

        self.dialog.geometry(f"+{x}+{y}")

    def show(self):
        """Show the dialog and wait for it to close."""
        self.dialog.wait_window()
