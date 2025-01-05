import extract_text
import dc_fet

#input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

#input
def select_state():
    print("Please select one of the following states:")
    print("0: Use picture for extracting values")
    print("1: State 1")
    print("2: State 2")
    print("3: State 3")
    print("4: State 4")
    print("5: State 5")
    print("6: State 6")
    print("7: State 7")
    print("8: State 8")

    selection = int(input("Your choice: "))
    
    # Updated part in select_state function to allow file input for image extraction
    if selection == 0:
        image_path = input("Enter the path of the image file: ")
        circuit_type = int(input("Select circuit type:\n1: Simple\n2: Complex\n3: Circuit\nYour choice: "))

        if circuit_type == 1:
            VDD, VGG, RD = extract_text.simple_circuit(image_path)
            if VDD is not None:
                IDSS = get_float_input("Enter IDSS: ")
                VPO = get_float_input("Enter VPO: ")
                dc_fet.state_1_p_channel(VDD, VGG, RD, IDSS, VPO)

        if circuit_type == 2:
            VDD, VGG, RD = extract_text.simple_circuit(image_path)
            if VDD is not None:
                K = get_float_input("Enter IDSS: ")
                VT = get_float_input("Enter VPO: ")
                dc_fet.state_1_p_channel(VDD, VGG, RD, K, VT)

        elif circuit_type == 3:
            VDD, RD, RS = extract_text.circuit(image_path)
            if VDD is not None:
                K = get_float_input("Enter K: ")
                VT = get_float_input("Enter VT: ")
                dc_fet.state_2_p_channel(VDD, RD, RS, K, VT)

        elif circuit_type == 4:
            VDD, RD, RS = extract_text.circuit(image_path)
            if VDD is not None:
                IDSS = get_float_input("Enter IDSS: ")
                VPO = get_float_input("Enter VPO: ")
                dc_fet.state_2_p_channel(VDD, RD, RS, IDSS, VPO)

        elif circuit_type == 5:
            VDD, RD, RG1, RG2, RS = extract_text.complex_circuit(image_path)
            if VDD is not None:
                IDSS = get_float_input("Enter IDSS: ")
                VPO = get_float_input("Enter VPO: ")
                dc_fet.state_5_p_channel(VDD, RD, RG1, RG2, RS, IDSS, VPO)

        elif circuit_type == 6:
            VDD, RD, RG1, RG2, RS = extract_text.complex_circuit(image_path)
            if VDD is not None:
                K = get_float_input("Enter K: ")
                VT = get_float_input("Enter VT: ")
                dc_fet.state_5_p_channel(VDD, RD, RG1, RG2, RS, K, VT)
        else:
            print("Invalid choice for circuit type!")



    elif selection == 1:
        VGG = get_float_input("Enter VGG: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        IDSS = get_float_input("Enter IDSS: ")
        VPO = get_float_input("Enter VPO: ")
        dc_fet.state_1(VDD, VGG, RD, IDSS, VPO)

    elif selection == 2:
        VGG = get_float_input("Enter VGG: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        dc_fet.state_2(VDD, VGG, RD, K, VT)

    elif selection == 3:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        IDSS = get_float_input("Enter IDSS: ")
        VPO = get_float_input("Enter VPO: ")
        dc_fet.state_3(VDD, RD, RSS, IDSS, VPO)

    elif selection == 4:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        dc_fet.state_4(RSS, VDD, RD, K, VT)

    elif selection == 5:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG1 = get_float_input("Enter RG1: ")
        RG2 = get_float_input("Enter RG2: ")
        IDSS = get_float_input("Enter IDSS: ")
        VPO = get_float_input("Enter VPO: ")
        dc_fet.state_5(VDD, RD, RG1, RG2, RSS, IDSS, VPO)

    elif selection == 6:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RSS = get_float_input("Enter RSS: ")
        RG1 = get_float_input("Enter RG1: ")
        RG2 = get_float_input("Enter RG2: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        dc_fet.state_6(VDD, RD, RG1, RG2, RSS, K, VT)

    elif selection == 7:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG = get_float_input("Enter RG: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        dc_fet.state_7(VDD, RD, RG, K, VT)

    elif selection == 8:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG = get_float_input("Enter RG: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP = get_float_input("Enter VP: ")
        dc_fet.state_8(VDD, RD, RG, IDSS, VP)

    else:
        print("Invalid choice!")
        
