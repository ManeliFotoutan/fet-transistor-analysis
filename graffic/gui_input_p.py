import tkinter as tk
from tkinter import messagebox , simpledialog , filedialog
from functools import partial
import gui_dc_fet_pnp
import extract_text
from PIL import Image, ImageTk

# Define global styles
BG_COLOR = "#1E1E2F"
FG_COLOR = "#FFFFFF"
BUTTON_COLOR = "#007ACC"
BUTTON_HOVER_COLOR = "#005A9E"
ENTRY_BG_COLOR = "#2D2D44"
ENTRY_FG_COLOR = "#FFFFFF"

def on_enter(e):
    """Handle button hover."""
    e.widget.config(bg=BUTTON_HOVER_COLOR)

def on_leave(e):
    """Handle button leave."""
    e.widget.config(bg=BUTTON_COLOR)
    
def get_float_inputs(prompts):
    # Create a modal form window
    form_window = tk.Toplevel()
    form_window.title("Input of Circuit")
    form_window.geometry("600x700")
    form_window.grab_set()  # Make the window modal
    form_window.configure(bg=BG_COLOR)

    inputs = {}  # Store the input fields and their associated prompts
    entries = {}  # Store the Entry widgets for validation

    def submit():
        try:
            # Validate and collect inputs
            for prompt, entry in entries.items():
                value = entry.get().strip()
                if value == "":
                    raise ValueError(f"Field '{prompt}' cannot be empty.")
                inputs[prompt] = float(value)
            form_window.destroy()  # Close the form on success
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def cancel():
        # Cancel input
        inputs.clear()  # Ensure no values are returned
        form_window.destroy()

    # Create labels and entry fields for each prompt
    for i, prompt in enumerate(prompts):
        tk.Label(
            form_window,
            text=prompt,
            bg=BG_COLOR,
            fg=FG_COLOR,
            font=("Arial", 12),
            anchor="w",
        ).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(
            form_window,
            font=("Arial", 12),
            width=20,
            bg=ENTRY_BG_COLOR,
            fg=ENTRY_FG_COLOR,
            relief="flat"
        )
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[prompt] = entry

    # Submit and Cancel buttons
    button_frame = tk.Frame(form_window)
    button_frame.grid(row=len(prompts)+1 , column=0, columnspan=2, pady=10)

    tk.Button(
        button_frame, text="Submit", command=submit, bg="#007ACC", fg="white", width=10
    ).pack(side="left")

    tk.Button(
        button_frame, text="Cancel", command=cancel, bg="#007ACC", fg="white", width=10
    ).pack(side="right")

    # Wait for the form to close
    form_window.wait_window()

    # Raise an error if the user cancels
    if not inputs:
        raise ValueError("Input cancelled or invalid.")

    return inputs


def show_output(result, details):
    # Create a new window
    root_output = tk.Tk()
    root_output.title("FET Analysis")
    root_output.configure(bg=BG_COLOR)

    # Display result label
    result_label = tk.Label(root_output, text=result, font=("Arial", 14, "bold"), bg=BG_COLOR, fg="white")
    result_label.pack(pady=20)

    # Display details label
    details_label = tk.Label(root_output, text=details, font=("Arial", 12), bg=BG_COLOR, fg="#005A9E")
    details_label.pack(pady=10)

    # Start the main loop for the output window
    root_output.mainloop()

    
def select_state():
    """Handles the GUI for selecting one of the 9 states."""
    def handle_selection(state):
        if state == 0:
            image_path = filedialog.askopenfilename(title="Select Image File")
            if not image_path:
                messagebox.showerror("Error", "No image selected!")
                return
            
            img = Image.open(image_path)
            img_display = ImageTk.PhotoImage(img)

            img_window = tk.Toplevel()
            img_window.title("Circuit Image")
            img_label = tk.Label(img_window, image=img_display)
            img_label.image = img_display 
            img_label.pack()
            
            circuit_type_input = get_float_inputs(["Enter Circuit Type (1-6):"])
            circuit_type = int(next(iter(circuit_type_input.values()), None))

            if circuit_type not in range(1, 7):
                circuit_type = None

            if not circuit_type or circuit_type not in range(1, 7):
                messagebox.showerror("Error", "Invalid Circuit Type!")
                return

            circuit_extractors = [extract_text.simple_circuit, extract_text.circuit, extract_text.complex_circuit]
            extract_func = circuit_extractors[min(circuit_type-1, 2)]
            circuit_values = extract_func(image_path)

            if circuit_values[0] is None:
                messagebox.showerror("Error", "Failed to extract circuit values.")
                return
            
            param_prompts = {
                1: ["Enter IDSS (Gate-Source Leakage Current):", "Enter VPO (Pinch-off Voltage):"],
                2: ["Enter K (transconductance parameter):", "Enter VT (voltage transformer):"],
                3: ["Enter IDSS (Gate-Source Leakage Current):", "Enter VPO (Pinch-off Voltage):"],
                4: ["Enter K (transconductance parameter):", "Enter VT (voltage transformer):"],
                5: ["Enter IDSS (Gate-Source Leakage Current):", "Enter VPO (Pinch-off Voltage):"],
                6: ["Enter K (transconductance parameter):", "Enter VT (voltage transformer):"]
            }
            
            inputs = get_float_inputs(param_prompts[circuit_type])
            
            function_map = {
                1: gui_dc_fet_pnp.state_1_p_channel,
                2: gui_dc_fet_pnp.state_2_p_channel,
                3: gui_dc_fet_pnp.state_3_p_channel,
                4: gui_dc_fet_pnp.state_4_p_channel,
                5: gui_dc_fet_pnp.state_5_p_channel,
                6: gui_dc_fet_pnp.state_6_p_channel
            }
            
            result, details = function_map[circuit_type](*circuit_values, *inputs.values())
            show_output(result, details)

        else:
            if state == 1:
                prompts = [
                "Enter VGG (Gate Voltage) : ",
                "Enter VDD (Supply Voltage) : ",
                "Enter RD (Drain Resistance) : ",
                "Enter IDSS (Gate-Source Leakage Current) : ",
                "Enter VPO (Pinch-off Voltage) : "
                ]
                inputs = get_float_inputs(prompts)
                VGG = inputs["Enter VGG (Gate Voltage) : "]
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                IDSS = inputs["Enter IDSS (Gate-Source Leakage Current) : "]
                VPO = inputs["Enter VPO (Pinch-off Voltage) : "]
                result , details = gui_dc_fet_pnp.state_1_p_channel(VDD, VGG, RD, IDSS, VPO)
                show_output(result, details)
                
            elif state == 2:
                prompts = ["Enter VGG (Gate Voltage) : ",
                "Enter VDD (Supply Voltage) : ",
                "Enter RD (Drain Resistance) : ",
                "Enter K (transconductance parameter) : " ,
                "Enter VT (voltage transformer) : "
                ]
                inputs = get_float_inputs(prompts)
                VGG = inputs["Enter VGG (Gate Voltage) : "]
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                K = inputs["Enter K (transconductance parameter) : "]
                VT = inputs["Enter VT (voltage transformer) : "]
                result , details = gui_dc_fet_pnp.state_2_p_channel(VDD, VGG, RD, K, VT)
                show_output(result, details)

            elif state == 3:
                prompts = ["Enter RSS (Source-Source Resistance): ",
                "Enter VDD (Supply Voltage) : ",
                "Enter RD (Drain Resistance) : ",
                "Enter IDSS (Gate-Source Leakage Current) : ",
                "Enter VPO (Pinch-off Voltage) : "
                ]
                inputs = get_float_inputs(prompts)
                RSS = inputs["Enter RSS (Source-Source Resistance): "]
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                IDSS = inputs["Enter IDSS (Gate-Source Leakage Current) : "]
                VPO = inputs["Enter VPO (Pinch-off Voltage) : "]
                result , details = gui_dc_fet_pnp.state_3_p_channel(VDD, RD, RSS, IDSS, VPO)
                show_output(result, details)
                
            elif state == 4:
                prompts = ["Enter RSS (Source-Source Resistance): ",
                "Enter VDD (Supply Voltage) : ",
                "Enter RD (Drain Resistance) : ",
                "Enter K (transconductance parameter) : ",
                "Enter VT (voltage transformer) : "
                ]
                inputs = get_float_inputs(prompts)
                RSS = inputs["Enter RSS (Source-Source Resistance): "]
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                K = inputs["Enter K (transconductance parameter) : "]
                VT = inputs["Enter VT (voltage transformer) : "]
                result , details = gui_dc_fet_pnp.state_4_p_channel(VDD, RD , RSS, K, VT)
                show_output(result, details)
                
            elif state == 5:
                prompts = [
                    "Enter RSS (Source-Source Resistance) : ",
                    "Enter VDD (Supply Voltage) : ",
                    "Enter RD (Drain Resistance) : ",
                    "Enter RG1 (Gate Resistance) : ",
                    "Enter RG2 (Gate Resistance) : ",
                    "Enter IDSS (Gate-Source Leakage Current) : ",
                    "Enter VPO (Pinch-off Voltage) : "
                ]
                inputs = get_float_inputs(prompts)
                RSS = inputs["Enter RSS (Source-Source Resistance) : "]
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                RG1 = inputs["Enter RG1 (Gate Resistance) : "]
                RG2 = inputs["Enter RG2 (Gate Resistance) : "]
                IDSS = inputs["Enter IDSS (Gate-Source Leakage Current) : "]
                VPO = inputs["Enter VPO (Pinch-off Voltage) : "]
                result , details = gui_dc_fet_pnp.state_5_p_channel(VDD, RD, RG1, RG2, RSS, IDSS, VPO)
                show_output(result, details)

            elif state == 6:
                prompts = [
                    "Enter VDD (Supply Voltage) : ",
                    "Enter RD (Drain Resistance) : ",
                    "Enter RSS (Source-Source Resistance) : ",
                    "Enter RG1 (Gate Resistance) : ",
                    "Enter RG2 (Gate Resistance) : ",
                    "Enter K (transconductance parameter) : ",
                    "Enter VT (voltage transformer) : "
                ]
                inputs = get_float_inputs(prompts)
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                RSS = inputs["Enter RSS (Source-Source Resistance) : "]
                RG1 = inputs["Enter RG1 (Gate Resistance) : "]
                RG2 = inputs["Enter RG2 (Gate Resistance) : "]
                K = inputs["Enter K (transconductance parameter) : "]
                VT = inputs["Enter VT (voltage transformer) : "]
                result , details = gui_dc_fet_pnp.state_6_p_channel(VDD, RD, RG1, RG2, RSS, K, VT)
                show_output(result, details)

            elif state == 7:
                prompts = [
                    "Enter VDD (Supply Voltage) : ",
                    "Enter RD (Drain Resistance) : ",
                    "Enter RG (Gate Resistance) : ",
                    "Enter K (transconductance parameter) : ",
                    "Enter VT (voltage transformer) : "
                ]
                inputs = get_float_inputs(prompts)
                VDD = inputs["Enter VDD (Supply Voltage) : "]
                RD = inputs["Enter RD (Drain Resistance) : "]
                RG = inputs["Enter RG (Gate Resistance) : "]
                K = inputs["Enter K (transconductance parameter) : "]
                VT = inputs["Enter VT (voltage transformer) : "]
                result , details = gui_dc_fet_pnp.state_7_p_channel(VDD, RD, RG, K, VT)
                show_output(result, details)
                
            else:
                messagebox.showerror("Error", "Invalid state selection.")
                messagebox.showinfo("Selection", f"You selected: State {state}.")
            root.destroy()

    # Set up the main window
    root = tk.Tk()
    root.title("FET Analysis")
    root.configure(bg=BG_COLOR)


    tk.Label(root, text="Please select one of the following states:", font=("Arial", 14) ,bg= BG_COLOR ,fg = "white").pack(pady=10)

    tk.Button(
    root,
    text="0: Use picture for extracting values",
    command=lambda: handle_selection(0),
    bg=BUTTON_COLOR,
    fg=FG_COLOR,
    font=("Arial", 12),
    relief="flat",
    width=30,
    height=2
    ).pack(pady=10)
    state_texts = {
        1: "State 1 ():",
        2: "State 2: Description for State 2",
        3: "State 3: Description for State 3",
        4: "State 4: Description for State 4",
        5: "State 5: Description for State 5",
        6: "State 6: Description for State 6",
        7: "State 7: Description for State 7",
    }
    # Create buttons for each state (1 to 7)
    for i in range(1, 8):  # States 1 to 7
        tk.Button(
            root,
            text=f"{i}: {state_texts[i]}",
            command=lambda state=i: handle_selection(state),
            bg=BUTTON_COLOR,
            fg=FG_COLOR,
            font=("Arial", 12),
            relief="flat",
            width=30,
            height=2
        ).pack(pady=5)

    root.mainloop()