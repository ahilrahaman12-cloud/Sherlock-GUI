import threading
import subprocess
import customtkinter as ctk

# Configure Dark Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Remove title bar and make window fixed size
        self.overrideredirect(True)
        width, height = 450, 220
        
        # Center splash relative to screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Container frame
        self.frame = ctk.CTkFrame(self, corner_radius=15, border_width=2, border_color="#1F6AA5")
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Flashing Text Label
        self.splash_label = ctk.CTkLabel(
            self.frame, 
            text="Sherlock-GUI by Ahil", 
            font=("Consolas", 32, "bold"),
            text_color="#000000"
        )
        self.splash_label.pack(expand=True)
        
        # Flash Animation State
        self.flash_colors = ["#000000", "#000000"]
        self.flash_step = 0
        self.animate_flash()

    def animate_flash(self):
        if self.flash_step < 10:
            # Alternate colors to simulate flashing effect
            color = self.flash_colors[self.flash_step % len(self.flash_colors)]
            self.splash_label.configure(text_color=color)
            self.flash_step += 1
            self.after(250, self.animate_flash)
        else:
            self.destroy()
            self.parent.deiconify()  # Reveal main window when splash completes


class OSINTApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sherlock-GUI - by Ahil")
        self.geometry("750x700")
        self.resizable(True, True)
        
        # Initially hide main window while splash screen runs
        self.withdraw()
        
        # Launch Splash Screen
        self.splash = SplashScreen(self)
        
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        self.header_label = ctk.CTkLabel(
            self, 
            text="Sherlok-GUI", 
            font=("Consolas", 22, "bold")
        )
        self.header_label.pack(pady=(20, 10))

        # Inputs Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=20, pady=10)

        # Form Input Fields
        self.entries = {}
        fields = [
            ("Username", "username", "e.g. octocat"),
            
        ]

        for idx, (label_text, key, placeholder) in enumerate(fields):
            lbl = ctk.CTkLabel(self.input_frame, text=label_text, font=("Arial", 12, "bold"))
            lbl.grid(row=idx, column=0, padx=15, pady=8, sticky="w")
            
            entry = ctk.CTkEntry(self.input_frame, placeholder_text=placeholder, width=420)
            entry.grid(row=idx, column=1, padx=15, pady=8, sticky="ew")
            self.entries[key] = entry

        self.input_frame.grid_columnconfigure(1, weight=1)

        # Run Button
        self.run_btn = ctk.CTkButton(
            self, 
            text="Start Investigation", 
            font=("Arial", 14, "bold"),
            fg_color="#1F6AA5",
            hover_color="#144870",
            command=self.start_investigation_thread
        )
        self.run_btn.pack(pady=10)

        # Output Text Console
        self.console_label = ctk.CTkLabel(self, text="Console Output:", font=("Arial", 12, "bold"))
        self.console_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.output_box = ctk.CTkTextbox(
            self, 
            font=("Consolas", 12), 
            wrap="word",
            activate_scrollbars=True
        )
        self.output_box.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def log(self, text: str):
        """Append output text safely to console."""
        self.output_box.insert(ctk.END, text + "\n")
        self.output_box.see(ctk.END)

    def start_investigation_thread(self):
        """Runs OSINT checks in a background thread to keep GUI smooth."""
        self.output_box.delete("1.0", ctk.END)
        self.run_btn.configure(state="disabled", text="Running...")
        threading.Thread(target=self.run_osint_checks, daemon=True).start()

    def run_osint_checks(self):
        username = self.entries["username"].get().strip()
      

        # 1. Sherlock
        if username:
            self.log(f"=== 1. Sherlock Search for '{username}' ===")
            cmd = ["sherlock", username, "--site", "github", "--site", "twitter"]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.log(result.stdout)
            except subprocess.CalledProcessError as e:
                self.log(f"Error running Sherlock: {e}\n")
            except FileNotFoundError:
                self.log("Error: Sherlock executable not found in system PATH.\n")
        else:
            self.log("=== 1. Sherlock ===\nSkipped: No username provided.\n")

       


if __name__ == "__main__":
    app = OSINTApp()
    app.mainloop()
