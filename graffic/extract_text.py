from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  

def simple_circuit(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config='--psm 3')

    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*k', text)

    VDD = float(v_matches[0]) if v_matches else 0.0
    VGG = float(v_matches[1]) if len(v_matches) > 1 else 0.0
    RD = float(k_matches[0]) if k_matches else 0.0

    print(f"VDD: {VDD} V, VGG: {VGG} V, RD: {RD} k")
    return VDD, VGG, RD

def circuit(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config='--psm 3')

    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*k', text)

    VDD = float(v_matches[0]) if v_matches else 0.0
    RD = float(k_matches[0]) if k_matches else 0.0
    RS = float(k_matches[1]) if len(k_matches) > 1 else 0.0

    print(f"VDD: {VDD} V, RD: {RD} k, RS: {RS} k")
    return VDD, RD, RS

def complex_circuit(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config='--psm 3')

    v_matches = re.findall(r'(\d+\.?\d*)\s*V', text)
    k_matches = re.findall(r'(\d+\.?\d*)\s*[kK]', text)

    VDD = float(v_matches[0]) if v_matches else 0.0
    RD = float(k_matches[0]) if k_matches else 0.0
    RG1 = float(k_matches[1]) if len(k_matches) > 1 else 0.0
    RG2 = float(k_matches[2]) if len(k_matches) > 2 else 0.0
    RS = float(k_matches[3]) if len(k_matches) > 3 else 0.0

    print(f"VDD: {VDD} V, RD: {RD} k, RG1: {RG1} k, RG2: {RG2} k, RS: {RS} k")
    return VDD, RD, RG1, RG2, RS
