import tkinter as tk
from tkinter import messagebox
import gui_input_p
import input_n

# Define global styles
BG_COLOR = "#1E1E2F"
FG_COLOR = "#FFFFFF"
BUTTON_COLOR = "#007ACC"
BUTTON_HOVER_COLOR = "#005A9E"

def on_enter(e):
    """Handle button hover."""
    e.widget.config(bg=BUTTON_HOVER_COLOR)

def on_leave(e):
    """Handle button leave."""
    e.widget.config(bg=BUTTON_COLOR)

def handle_manual_input():
    """Handles the manual input selection."""
    def handle_selection(selection):
        if selection == "n-channel":
            input_n.select_state()
        elif selection == "p-channel":
            gui_input_p.select_state()
        else:
            messagebox.showerror("Error", "Invalid selection.")
        manual_window.destroy()

    manual_window = tk.Toplevel()
    manual_window.title("Manual Input")
    manual_window.geometry("400x200")
    manual_window.configure(bg=BG_COLOR)

    tk.Label(
        manual_window,
        text="Please select one of the following states:",
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=("Arial", 12)
    ).pack(pady=20)

    n_button = tk.Button(
        manual_window,
        text="n-channel",
        command=lambda: handle_selection("n-channel"),
        bg=BUTTON_COLOR,
        fg=FG_COLOR,
        font=("Arial", 12),
        relief="flat",
        width=15,
        height=2
    )
    n_button.pack(pady=10)
    n_button.bind("<Enter>", on_enter)
    n_button.bind("<Leave>", on_leave)

    p_button = tk.Button(
        manual_window,
        text="p-channel",
        command=lambda: handle_selection("p-channel"),
        bg=BUTTON_COLOR,
        fg=FG_COLOR,
        font=("Arial", 12),
        relief="flat",
        width=15,
        height=2
    )
    p_button.pack(pady=10)
    p_button.bind("<Enter>", on_enter)
    p_button.bind("<Leave>", on_leave)

def main_gui():
    """Main GUI application."""
    root = tk.Tk()
    root.title("DC_FET Circuit Analyzer")
    root.geometry("500x300")
    root.configure(bg=BG_COLOR)

    tk.Label(
        root,
        text="Input your DC_FET circuit",
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=("Arial Bold", 16)
    ).pack(pady=20)

    manual_button = tk.Button(
        root,
        text="Manual Input",
        command=handle_manual_input,
        bg=BUTTON_COLOR,
        fg=FG_COLOR,
        font=("Arial", 14),
        relief="flat",
        width=20,
        height=2
    )
    manual_button.pack(pady=10)
    manual_button.bind("<Enter>", on_enter)
    manual_button.bind("<Leave>", on_leave)

    guide_button = tk.Button(
        root,
        text="Guide",
        bg=BUTTON_COLOR,
        fg=FG_COLOR,
        font=("Arial", 14),
        relief="flat",
        width=20,
        height=2
    )
    guide_button.pack(pady=10)
    guide_button.bind("<Enter>", on_enter)
    guide_button.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
