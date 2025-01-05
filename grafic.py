import tkinter as tk
from tkinter import messagebox

def launch_gui(on_submit_callback):
    def submit():
        try:
            state = int(state_var.get())
            params = entry_params.get("1.0", tk.END).strip().split(',')
            params = [float(p) for p in params]
            on_submit_callback(state, params)
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
    
    root = tk.Tk()
    root.title("DC FET Problem Solver")
    
    tk.Label(root, text="Select State (1-7):").grid(row=0, column=0, padx=10, pady=5)
    state_var = tk.StringVar(value="1")
    tk.Entry(root, textvariable=state_var).grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(root, text="Enter Parameters (comma-separated):").grid(row=1, column=0, padx=10, pady=5)
    entry_params = tk.Text(root, height=4, width=30)
    entry_params.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(root, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=10)
    
    root.mainloop()
