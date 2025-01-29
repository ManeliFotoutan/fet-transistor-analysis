from PIL import Image
import pytesseract
import re

def simple_circuit(image_path):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path if necessary

    image_path = 'try1.jpg'
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, config='--psm 3')  # Try different PSM values

    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*k', text)

    VDD = v_matches[0] if len(v_matches) > 0 else None  # First voltage
    VGG = v_matches[1] if len(v_matches) > 1 else None  # Second voltage
    RD = k_matches[0] if len(k_matches) > 0 else None  # First resistance

    print(f"VDD: {VDD} V")
    print(f"VGG: {VGG} V")
    print(f"RD: {RD} k")

    # Check for None and provide default values
    VDD = float(VDD) if VDD is not None else 0.0
    VGG = float(VGG) if VGG is not None else 0.0
    RD = float(RD) if RD is not None else 0.0

    return VDD, VGG, RD


def circuit(image_path):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path if necessary

    image_path = 'try1.jpg'
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, config='--psm 3')  # Try different PSM values

    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*k', text)

    VDD = v_matches[0] if len(v_matches) > 0 else None  # First voltage
    RD = k_matches[0] if len(k_matches) > 0 else None  # First resistance
    RS = k_matches[1] if len(k_matches) > 1 else None  # Second resistance

    print(f"VDD: {VDD} V")
    print(f"RD: {RD} k")
    print(f"RS: {RS} k")

    # Check for None and provide default values
    VDD = float(VDD) if VDD is not None else 0.0
    RD = float(RD) if RD is not None else 0.0
    RS = float(RS) if RS is not None else 0.0

    return VDD, RD, RS


def complex_circuit(image_path):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path if necessary

    image_path = 'try2.jpg'
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, config='--psm 3')  # Try different PSM values

    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*[kK]', text)  # Case-insensitive for 'k'

    VDD = v_matches[0] if len(v_matches) > 0 else None  # First voltage
    RD = k_matches[0] if len(k_matches) > 0 else None
    RG1 = k_matches[1] if len(k_matches) > 1 else None  
    RG2 = k_matches[2] if len(k_matches) > 2 else None  
    RS = k_matches[3] if len(k_matches) > 3 else None  

    print(f"VDD: {VDD} V")
    print(f"RD: {RD} k")
    print(f"RG1: {RG1} k")
    print(f"RG2: {RG2} k")
    print(f"RS: {RS} k")

    # Check for None and provide default values
    VDD = float(VDD) if VDD is not None else 0.0
    RD = float(RD) if RD is not None else 0.0
    RG1 = float(RG1) if RG1 is not None else 0.0
    RG2 = float(RG2) if RG2 is not None else 0.0
    RS = float(RS) if RS is not None else 0.0

    return VDD, RD, RG1, RG2, RS

