import tkinter as tk
from tkinter import messagebox , simpledialog , filedialog
from functools import partial
import gui_dc_fet_p_channel
import extract_text
from PIL import Image, ImageTk
import pyttsx3
import re

BG_COLOR = "#FFE4C4" 
FG_COLOR = "#640f09"
BUTTON_COLOR = "#640f09" 
BUTTON_HOVER_COLOR = "#640f09" 
DARK_BROWN = "#500C07"
BROWN = "#640f09"
ENTRY_BG_COLOR = "#640f09"
ENTRY_FG_COLOR = "#FFE4C4" 
CREAM = "#FFE4C4"

def on_enter(e):
    """Handle button hover."""
    e.widget.config(bg=BUTTON_HOVER_COLOR)

def on_leave(e):
    """Handle button leave."""
    e.widget.config(bg=BUTTON_COLOR)

def show_error_window(error_message):
    """Create Window4 to display error messages without freezing."""
    error_window = tk.Toplevel()
    error_window.title("Input Error")
    error_window.geometry("400x200")
    error_window.grab_set()
    error_window.configure(bg=BG_COLOR)

    tk.Label(error_window, text="Invalid Input!", fg= FG_COLOR, font=("Arial", 14, "bold"), bg=BG_COLOR).pack(pady=10)
    tk.Label(error_window, text=error_message, fg=FG_COLOR, font=("Arial", 12), bg=BG_COLOR, wraplength=350).pack(pady=10)
    tk.Button(error_window, text="OK", command=error_window.destroy, bg=BUTTON_COLOR, fg=CREAM, width=10).pack(pady=10)

def get_float_inputs(prompts):
    # Create a modal form window
    form_window = tk.Toplevel()
    form_window.title("Input of Circuit")
    form_window.geometry("600x700")
    form_window.grab_set()  # Make the window modal
    form_window.configure(bg=BG_COLOR)

    inputs = {}  # Store the input fields and their associated prompts
    entries = {}  # Store the Entry widgets for validation
    
    def is_valid_float(value):
        """Check if the input is a valid float number."""
        try:
            float(value)
            return True
        except ValueError:
            return False
    def submit():
        try:
            # Validate and collect inputs
            for prompt, entry in entries.items():
                value = entry.get().strip()
                if value == "":
                    raise ValueError(f"Field '{prompt}' cannot be empty.")
                elif not is_valid_float(value): 
                    raise ValueError(f"Field '{prompt}' must be a number.")
                
                inputs[prompt] = float(value)
            form_window.destroy()  # Close the form on success
        except ValueError as e:
            show_error_window(str(e))

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
            fg=DARK_BROWN,
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
        button_frame, text="Submit", command=submit, bg=BUTTON_COLOR, fg=CREAM, width=10
    ).pack(side="left")

    tk.Button(
        button_frame, text="Cancel", command=cancel, bg=BUTTON_COLOR, fg=CREAM, width=10
    ).pack(side="right")

    # Wait for the form to close
    form_window.wait_window()

    # Raise an error if the user cancels
    if not inputs:
        raise ValueError("Input cancelled or invalid.")

    return inputs

def truncate_numbers_in_text(text):
    def truncate_match(match):
        num = match.group()
        return num[:num.find('.') + 3]  # Keep only two digits after the decimal point

    return re.sub(r"\d+\.\d+", truncate_match, text)


def speak_text(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Ensure proper shutdown after speech is finished

def show_output(result, details):
    root_output = tk.Tk()
    root_output.title("FET Analysis")
    root_output.configure(bg=BG_COLOR)

    rounded_details = truncate_numbers_in_text(details)
    
    # Display result label
    result_label = tk.Label(root_output, text=result, font=("Arial", 14, "bold"), bg=BG_COLOR, fg=DARK_BROWN)
    result_label.pack(pady=20)

    # Display details label
    details_label = tk.Label(root_output, text=details, font=("Arial", 12), bg=BG_COLOR, fg=DARK_BROWN, wraplength=400)
    details_label.pack(pady=10)

    # Speak after window appears (delay by 500ms)
    root_output.after(500, lambda: speak_text(f"Result: {result}. {rounded_details}."))

    # Start the main loop for the output window
    root_output.mainloop()
    
def select_state():
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

            circuit_type_input = get_float_inputs(["Enter Circuit Type 1-7 (the order is like previous page)"])
            circuit_type = int(next(iter(circuit_type_input.values()), None))

            if circuit_type not in range(1, 8):
                circuit_type = None

            if circuit_type not in range(1, 8):
                messagebox.showerror("Error", "Invalid Circuit Type!")
                return

            circuit_extractors = {
                1: extract_text.simple_circuit,
                2: extract_text.simple_circuit,
                3: extract_text.circuit,
                4: extract_text.circuit,
                5: extract_text.complex_circuit,
                6: extract_text.complex_circuit,
                7: extract_text.baiasing_circuit
            }
            extract_func = circuit_extractors[circuit_type]
            circuit_values = extract_func(image_path)

            if circuit_values[0] is None:
                messagebox.showerror("Error", "Failed to extract circuit values.")
                return
            
            param_prompts = {
                1: ["Enter IDSS (Gate-Source Leakage Current) in 'mA': ", "Enter VPO (Pinch-off Voltage) in 'V': "],
                2: ["Enter K (transconductance parameter) in 'mA/V²': ", "Enter VT (voltage transformer) in 'V': "],
                3: ["Enter IDSS (Gate-Source Leakage Current) in 'mA': ", "Enter VPO (Pinch-off Voltage) in 'V': "],
                4: ["Enter K (transconductance parameter) in 'mA/V²': ", "Enter VT (voltage transformer) in 'V': "],
                5: ["Enter IDSS (Gate-Source Leakage Current) in 'mA': ", "Enter VPO (Pinch-off Voltage) in 'V': "],
                6: ["Enter K (transconductance parameter) in 'mA/V²': ", "Enter VT (voltage transformer) in 'V': "],
                7: ["Enter IDSS (Gate-Source Leakage Current) in 'mA': ", "Enter VPO (Pinch-off Voltage) in 'V': "],
            }
            
            inputs = get_float_inputs(param_prompts[circuit_type])
            
            if circuit_type == 1:
                result, details = gui_dc_fet_p_channel.state_1_p_channel(
                    circuit_values[0],  # VDD
                    circuit_values[1],  # VGG
                    circuit_values[2],  # RD
                    inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "],  
                    inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                )
            elif circuit_type == 2:
                result, details = gui_dc_fet_p_channel.state_2_p_channel(
                    circuit_values[0],  # VDD
                    circuit_values[1],  # VGG
                    circuit_values[2],  # RD
                    inputs["Enter K (transconductance parameter) in 'mA/V²': "],  
                    inputs["Enter VT (voltage transformer) in 'V': "]
                )
            elif circuit_type == 3:
                result, details = gui_dc_fet_p_channel.state_3_p_channel(
                    circuit_values[0],  # VDD
                    circuit_values[1],  # RD
                    circuit_values[2],  # RSS
                    inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "],  
                    inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                )
            elif circuit_type == 4:
                result, details = gui_dc_fet_p_channel.state_4_p_channel(
                    circuit_values[0],  # VDD
                    circuit_values[1],  # RD
                    circuit_values[2],  # RSS
                    inputs["Enter K (transconductance parameter) in 'mA/V²': "],  
                    inputs["Enter VT (voltage transformer) in 'V': "]
                )
            elif circuit_type == 5:
                result, details = gui_dc_fet_p_channel.state_5_p_channel(
                circuit_values[0],  # VDD
                circuit_values[1],  # RD
                circuit_values[2],  # RG1
                circuit_values[3],  # RG2
                circuit_values[4],  # RSS
                inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "],  
                inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                )
            elif circuit_type == 6:
                result, details = gui_dc_fet_p_channel.state_6_p_channel(
                circuit_values[0],  # VDD
                circuit_values[1],  # RD
                circuit_values[2],  # RG1
                circuit_values[3],  # RG2
                circuit_values[4],  # RSS
                inputs["Enter K (transconductance parameter) in 'mA/V²': "],  
                inputs["Enter VT (voltage transformer) in 'V': "]
                )
            elif circuit_type == 7:
                result, details = gui_dc_fet_p_channel.state_7_p_channel(
                    circuit_values[0],  # VDD
                    circuit_values[1],  # RD
                    circuit_values[2],  # RG
                    inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "],  
                    inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                )
            else:
                messagebox.showerror("Error", "Invalid Circuit Type!")
                return
            
            show_output(result, details)

        else:
            if state == 1:
                prompts = [
                "Enter VGG (Gate Voltage) in 'V': ",
                "Enter VDD (Supply Voltage) in 'V': ",
                "Enter RD (Drain Resistance) in 'KΩ' : ",
                "Enter IDSS (Gate-Source Leakage Current) in 'mA': ",
                "Enter VPO (Pinch-off Voltage) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                VGG = inputs["Enter VGG (Gate Voltage) in 'V': "]
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                IDSS = inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "]
                VPO = inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_1_p_channel(VDD, VGG, RD, IDSS, VPO)
                show_output(result, details)
                
            elif state == 2:
                prompts = ["Enter VGG (Gate Voltage) in 'V': ",
                "Enter VDD (Supply Voltage) in 'V': ",
                "Enter RD (Drain Resistance) in 'KΩ': ",
                "Enter K (transconductance parameter) in 'mA/V²': ",
                "Enter VT (voltage transformer) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                VGG = inputs["Enter VGG (Gate Voltage) in 'V': "]
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                K = inputs["Enter K (transconductance parameter) in 'mA/V²': "]
                VT = inputs["Enter VT (voltage transformer) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_2_p_channel(VDD, VGG, RD, K, VT)
                show_output(result, details)

            elif state == 3:
                prompts = ["Enter RSS (Source-Source Resistance) in 'KΩ': ",
                "Enter VDD (Supply Voltage) in 'V': ",
                "Enter RD (Drain Resistance) in 'KΩ': ",
                "Enter IDSS (Gate-Source Leakage Current) in 'mA': ",
                "Enter VPO (Pinch-off Voltage) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                RSS = inputs["Enter RSS (Source-Source Resistance) in 'KΩ': "]
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                IDSS = inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "]
                VPO = inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_3_p_channel(VDD, RD, RSS, IDSS, VPO)
                show_output(result, details)
                
            elif state == 4:
                prompts = ["Enter RSS (Source-Source Resistance) in 'KΩ': ",
                "Enter VDD (Supply Voltage) in 'V': ",
                "Enter RD (Drain Resistance) in 'KΩ': ",
                "Enter K (transconductance parameter) in 'mA/V²': ",
                "Enter VT (voltage transformer) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                RSS = inputs["Enter RSS (Source-Source Resistance) in 'KΩ': "]
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                K = inputs["Enter K (transconductance parameter) in 'mA/V²': "]
                VT = inputs["Enter VT (voltage transformer) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_4_p_channel(VDD, RD , RSS, K, VT)
                show_output(result, details)
                
            elif state == 5:
                prompts = [
                    "Enter RSS (Source-Source Resistance) in 'KΩ': ",
                    "Enter VDD (Supply Voltage) in 'V': ",
                    "Enter RD (Drain Resistance) in 'KΩ': ",
                    "Enter RG1 (Gate Resistance) in 'KΩ': ",
                    "Enter RG2 (Gate Resistance) in 'KΩ': ",
                    "Enter IDSS (Gate-Source Leakage Current) in 'mA': ",
                    "Enter VPO (Pinch-off Voltage) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                RSS = inputs["Enter RSS (Source-Source Resistance) in 'KΩ': "]
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                RG1 = inputs["Enter RG1 (Gate Resistance) in 'KΩ': "]
                RG2 = inputs["Enter RG2 (Gate Resistance) in 'KΩ': "]
                IDSS = inputs["Enter IDSS (Gate-Source Leakage Current) in 'mA': "]
                VPO = inputs["Enter VPO (Pinch-off Voltage) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_5_p_channel(VDD, RD, RG1, RG2, RSS, IDSS, VPO)
                show_output(result, details)

            elif state == 6:
                prompts = [
                    "Enter VDD (Supply Voltage) in 'V': ",
                    "Enter RD (Drain Resistance) in 'KΩ': ",
                    "Enter RSS (Source-Source Resistance) in 'KΩ': ",
                    "Enter RG1 (Gate Resistance) in 'KΩ': ",
                    "Enter RG2 (Gate Resistance) in 'KΩ': ",
                    "Enter K (transconductance parameter) in 'mA/V²': ",
                    "Enter VT (voltage transformer) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                RSS = inputs["Enter RSS (Source-Source Resistance) in 'KΩ': "]
                RG1 = inputs["Enter RG1 (Gate Resistance) in 'KΩ': "]
                RG2 = inputs["Enter RG2 (Gate Resistance) in 'KΩ': "]
                K = inputs["Enter K (transconductance parameter) in 'mA/V²': "]
                VT = inputs["Enter VT (voltage transformer) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_6_p_channel(VDD, RD, RG1, RG2, RSS, K, VT)
                show_output(result, details)

            elif state == 7:
                prompts = [
                    "Enter VDD (Supply Voltage) in 'V': ",
                    "Enter RD (Drain Resistance) in 'KΩ': ",
                    "Enter RG (Gate Resistance) in 'KΩ': ",
                    "Enter K (transconductance parameter) in 'mA/V²': ",
                    "Enter VT (voltage transformer) in 'V': "
                ]
                inputs = get_float_inputs(prompts)
                VDD = inputs["Enter VDD (Supply Voltage) in 'V': "]
                RD = inputs["Enter RD (Drain Resistance) in 'KΩ': "]
                RG = inputs["Enter RG (Gate Resistance) in 'KΩ': "]
                K = inputs["Enter K (transconductance parameter) in 'mA/V²': "]
                VT = inputs["Enter VT (voltage transformer) in 'V': "]
                result , details = gui_dc_fet_p_channel.state_7_p_channel(VDD, RD, RG, K, VT)
                show_output(result, details)
                
            else:
                messagebox.showerror("Error", "Invalid state selection.")
                messagebox.showinfo("Selection", f"You selected: State {state}.")
            root.destroy()

    # Set up the main window
    root = tk.Tk()
    root.title("FET Analysis")
    root.configure(bg=BG_COLOR)
    root.geometry("800x600")

    tk.Label(root, text="Please select one of the following states:", font=("Arial bold", 14) ,bg= BG_COLOR ,fg = DARK_BROWN).pack(pady=10)

    tk.Button(
    root,
    text=" Upload Picture",
    command=lambda: handle_selection(0),
    bg=BUTTON_COLOR,
    fg=CREAM,
    font=("Arial", 12),
    relief="flat",
    width=40,
    height=2
    ).pack(pady=10)
    state_texts = {
        1: "VGG in JFET and Depletion MOSFET",
        2: "VGG in Enhancement MOSFET",
        3: "RSS in JFET and Depletion MOSFET",
        4: "RSS in Enhancement MOSFET",
        5: "RG1, RG2 in JFET and Depletion MOSFET",
        6: "RG1, RG2 in Enhancement MOSFET",
        7: "Biasing Circuit",
    }
    # Create buttons for each state (1 to 7)
    for i in range(1, 8):  # States 1 to 7
        tk.Button(
            root,
            text=f"{i}: {state_texts[i]}",
            command=lambda state=i: handle_selection(state),
            bg=BUTTON_COLOR,
            fg=CREAM,
            font=("Arial", 12),
            relief="flat",
            width=40,
            height=2
        ).pack(pady=5)

    root.mainloop()