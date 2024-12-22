from PIL import Image
import pytesseract
import re

def simple_circuit():
    # Path to tesseract executable (if it's not in your PATH)
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path if necessary

    # Load an image from file
    image_path = 'try1.jpg'
    img = Image.open(image_path)

    # Use tesseract to extract text and numbers
    text = pytesseract.image_to_string(img, config='--psm 3')  # Try different PSM values

    # Print the extracted text
    print("Extracted text:")
    print(text)

    # Find all numbers followed by 'V' or 'k' in the order they appear
    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*k', text)

    #Assign values based on their order
    VDD = v_matches[0] if len(v_matches) > 0 else None  # First voltage
    VGG = v_matches[1] if len(v_matches) > 1 else None  # Second voltage
    RD = k_matches[0] if len(k_matches) > 0 else None  # First resistance
    RS = k_matches[1] if len(k_matches) > 1 else None  # Second resistance

    # Print the variables
    print(f"VDD: {VDD} V")
    print(f"VGG: {VGG} V")
    print(f"RD: {RD} k")
    print(f"RS: {RS} k")

def complex_circuit():
    # Path to tesseract executable (if it's not in your PATH)
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path if necessary

    # Load an image from file
    image_path = 'try2.jpg'
    img = Image.open(image_path)

    # Use tesseract to extract text and numbers
    text = pytesseract.image_to_string(img, config='--psm 3')  # Try different PSM values

    # Print the extracted text
    print("Extracted text:")
    print(text)

    # Find all numbers followed by 'V' or 'k' (case-insensitive)
    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*[kK]', text)  # Case-insensitive for 'k'

    # Assign values based on their order
    VDD = v_matches[0] if len(v_matches) > 0 else None  # First voltage
    RD = k_matches[0] if len(k_matches) > 0 else None
    RG1 = k_matches[1] if len(k_matches) > 1 else None  
    RG2 = k_matches[2] if len(k_matches) > 2 else None  
    RS = k_matches[3] if len(k_matches) > 3 else None  

    # Print the variables
    print(f"VDD: {VDD} V")
    print(f"RD: {RD} k")
    print(f"RG1: {RG1} k")
    print(f"RG2: {RG2} k")
    print(f"RS: {RS} k")





complex_circuit()