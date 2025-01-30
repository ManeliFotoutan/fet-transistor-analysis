import tkinter as tk
from tkinter import messagebox
import gui_input_p
import gui_input_n
from tkinter import ttk

# Define global styles
BG_COLOR = "#fbebe5" 
FG_COLOR = "#fbebe5" 
BUTTON_COLOR = "#635048" 
BUTTON_HOVER_COLOR = "#635048" 
brown = "#635048"


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
            gui_input_n.select_state()
        elif selection == "p-channel":
            gui_input_p.select_state()
        else:
            messagebox.showerror("Error", "Invalid selection.")
        manual_window.destroy()

    manual_window = tk.Toplevel()
    manual_window.title("Manual Input")
    manual_window.geometry("500x300")
    manual_window.configure(bg=BG_COLOR)

    tk.Label(
        manual_window,
        text="Please select one of the following states :",
        bg=BG_COLOR, 
        fg=BUTTON_HOVER_COLOR,
        font=("Arial bold", 14)
    ).pack(pady=20)

    n_button = tk.Button(
        manual_window,
        text="n-channel",
        command=lambda: handle_selection("n-channel"),
        bg=BUTTON_COLOR,
        fg=FG_COLOR,
        font=("Arial", 14),
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
        font=("Arial", 14),
        relief="flat",
        width=15,
        height=2
    )
    p_button.pack(pady=10)
    p_button.bind("<Enter>", on_enter)
    p_button.bind("<Leave>", on_leave)
def show_guide():
    """Opens a Guide Window with scrollable text."""
    guide_window = tk.Toplevel()
    guide_window.title("User Guide")
    guide_window.geometry("500x400")
    guide_window.configure(bg=BG_COLOR)

    # Title Label
    ttk.Label(
        guide_window,
        text="📘 DC_FET Circuit Analyzer - Guide",
        font=("Arial Bold", 14),
        background=BG_COLOR,
        foreground=brown
    ).pack(pady=10)

    # Frame for Scrollable Text
    frame = ttk.Frame(guide_window)
    frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Text Widget
    text_box = tk.Text(frame, wrap="word", height=10, font=("Arial", 12), bg=BG_COLOR, fg=brown)
    text_box.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, command=text_box.yview)
    scrollbar.pack(side="right", fill="y")
    text_box.config(yscrollcommand=scrollbar.set)

    # Guide Instructions
    guide_text = """
    1 Click 'Input Circuit' to analyze a DC_FET circuit.
    2 Then you have 2 options , n_channel and p-channel
    3 p-channel includes 7 states  including JFET , Enhancement MOSFET and Depletion MOSFET
    4 n-channel includes 8 states  including JFET , Enhancement MOSFET and Depletion MOSFET
    5 Select an image of the circuit OR enter values manually.
    6 if you choose uploading image , choose the correct circuit type (1-6).
    7 The tool will compute the results (saturated , not saturated or cutoff) and display the analysis.
    8 Use this guide if you need help!
    
    
    Electronics Circuits Project 
    @ Foroutan - Kazemzade
    """
    text_box.insert("1.0", guide_text)
    text_box.config(state="disabled")  # Prevent user edits

    # Close Button
    ttk.Button(
        guide_window,
        text="Close",
        command=guide_window.destroy,
        style="TButton"
    ).pack(pady=10)
    
def main_gui():
    """Main GUI application."""
    root = tk.Tk()
    root.title("DC_FET Circuit Analyzer")
    root.geometry("500x300")
    root.configure(bg=BG_COLOR)

    tk.Label(
        root,
        text="Input your DC_FET circuit :",
        bg=BG_COLOR,
        fg="#a020f0",
        font=("Arial bold", 14)
    ).pack(pady=20)

    manual_button = tk.Button(
        root,
        text="Input Circuit",
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
        command=show_guide,
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
