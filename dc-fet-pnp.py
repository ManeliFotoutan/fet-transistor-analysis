import numpy as np
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve

#input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

#calculate ID and VGS
def calculate_ID_state_1_p_channel(IDSS, VGS, VP0):
    ID = IDSS * (1 - VGS / abs(VP0))**2
    return ID

def calculate_ID_state_2_p_channel(K, VT):
    ID = K * (1 - abs(VT))**2
    return ID


def calculate_IDandVGS_state_3_p_channel(IDSS, RSS, VP0):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS - ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / abs(VP0))**2  
        return [eq1, eq2]

    initial_guess = [1, -1]  # Adjust the initial guess as needed for the p-channel case
    solution = fsolve(equations, initial_guess)
    
    ID1 = solution[0]

    initial_guess2 = [-1, 1]  
    solution2 = fsolve(equations, initial_guess2)

    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS = ID * RSS  # Adjust VGS calculation for p-channel
    return ID, VGS

def calculate_IDandVGS_state_4_p_channel(K, RSS, VT):
    def equations(vars):
        VGS = vars[0]
        ID = VGS / RSS   
        eq2 = ID - K * (VGS - abs(VT))**2
        return [eq2]

    initial_guess = [1]
    solution1 = fsolve(equations, initial_guess)
    VGS1 = solution1[0]
    ID1 = -VGS1 / RSS  

    initial_guess2 = [-1]  
    solution2 = fsolve(equations, initial_guess2)
    VGS2 = solution2[0]
    ID2 = -VGS2 / RSS  

    ID = min(ID1, ID2)
    VGS = ID * RSS  
    
    return ID, VGS

def calculate_IDandVGS_state_5_p_channel(Vth, RSS, IDSS, VP0):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS +Vth - ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / abs(VP0))**2  
        return [eq1, eq2]

    initial_guess = [1, -1]  # Adjust the initial guess as needed for the p-channel case
    solution = fsolve(equations, initial_guess)
    
    ID1 = solution[0]

    initial_guess2 = [-1, 1]  
    solution2 = fsolve(equations, initial_guess2)

    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS = -Vth + ID * RSS  
    return ID, VGS

def calculate_IDandVGS_state_6_p_channel(Vth, RSS, K, VT):
    def equations(vars):
        ID = vars[0]
        VGS = vars[1]
        eq1 = ID - K * (VGS - abs(VT))**2
        eq2 = VGS + (Vth - ID * RSS)
        return [eq1, eq2]

    initial_guess = [1, 1]
    solution1 = fsolve(equations, initial_guess)
    ID1 = solution1[0]

    initial_guess2 = [-1, 1]
    solution2 = fsolve(equations, initial_guess2)
    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS = -Vth + ID * RSS
    
    return ID, VGS

def calculate_IDandVDS_state_7_p_channel(VDD, RD, K, VT):
    def equations(vars):
        ID, VDS = vars
        eq1 = ID - K * (VDS - abs(VT))**2 
        eq2 = VDS + (VDD - ID * RD)  
        return [eq1, eq2]
   
    initial_guess = [1,-1]
    solution1 = fsolve(equations, initial_guess)
    ID1 = solution1[0]

    initial_guess2 = [-1, 1]
    solution2 = fsolve(equations, initial_guess2)
    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS =- VDD + ID * RD 
    
    return ID, VGS

#calculate VDS
def calculate_VDS_state_p_channel_1and2_p_channel(VDD, ID, RD):
    VDS = -VDD + (ID * RD)  
    return VDS

def calculate_VDS_state_p_channel(VDD, ID, RD , RSS):
    VDS = -VDD + ID * (RSS+RD) 
    return VDS

#Vth
def calculate_Vth_p_channel(VDD,RG1,RG2):
    return VDD*(RG2/(RG1+RG2))

#States
def state_1_p_channel(VGG, VDD, RD, IDSS, VP0):
    VGS = VGG  
    ID = calculate_ID_state_1_p_channel(IDSS, VGS, VP0)
    VDS = calculate_VDS_state_p_channel_1and2_p_channel(VDD, ID, RD)
    if VDS <= VGS - abs(VP0):
        print("Saturated")
        print(f"State 1 with VGS ={VGS }, ID={ID}, VDS={VDS}")
    else:
        print(f"State 1 with VGS ={VGS }, ID={ID}, VDS={VDS}")

        print("Not Saturated")

def state_2_p_channel(VGG, VDD, RD, K, VT):
    VGS = VGG  
    ID = calculate_ID_state_2_p_channel(K, VT)
    VDS = calculate_VDS_state_p_channel_1and2_p_channel(VDD, ID, RD)
    if VDS < VGS - VT:
        print("Saturated")
        print(f"State 2 with VGS ={VGS }, ID={ID}, VDS={VDS}")
    else:
        print("Not Saturated")

def state_3_p_channel(RSS, VDD, RD, IDSS, VP0):
    ID, VGS = calculate_IDandVGS_state_3_p_channel(IDSS, RSS, VP0)
    VDS = calculate_VDS_state_p_channel(VDD, ID, RD, RSS)   
    if VDS <= VGS - abs(VP0):
        print("Saturated")
        print(f"State 3 with VGS ={VGS}, ID={ID}, VDS={VDS}")
    else:
        print("Not Saturated")
        print(f"State 3 with VGS ={VGS}, ID={ID}, VDS={VDS}")


def state_4_p_channel(RSS, VDD, RD, K, VT):
    ID , VSG  = calculate_IDandVGS_state_5_p_channel(K, RSS, VT)
    VSD = calculate_VDS_state_p_channel(VDD, ID, RD , RSS)
    if VSD > abs(VSG - VT):
        print("Saturated")
        print(f"State 4 (p-channel) with VSG ={VSG }, ID={ID}, VSD={VSD}")
    else:
        print("Not Saturated")

def state_5_p_channel(VDD, RD, RSS,RG1,RG2,IDSS, VP0):
    Vth=calculate_Vth_p_channel(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_5_p_channel(Vth,RSS,IDSS,VP0)
    VDS = calculate_VDS_state_p_channel(VDD, ID, RD , RSS)
    if VDS> VGS - VP0:
        print("Saturated")
        print(f"State 3 with VGS ={VGS }, ID={ID}, VDS={VDS}")
    else:
        print("Not Saturated")
        print(f"State 3 with Vth={Vth},VGS ={VGS }, ID={ID}, VDS={VDS}")

def state_6_p_channel(VDD, RD, RSS,RG1,RG2, K, VT):
    Vth=calculate_Vth_p_channel(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_6_p_channel(Vth,RSS,K,VT)
    VDS = calculate_VDS_state_p_channel(VDD, ID, RD , RSS)
    if VDS> VGS - VT:
        print("Saturated")
        print(f"State 4 with VGS ={VGS }, ID={ID}, VDS={VDS},Vth={Vth}")
    else:
        print("Not Saturated")

def state_7_p_channel(VDD, RD, RG, K, VT):
    ID, VDS = calculate_IDandVDS_state_7_p_channel(VDD, RD, K, VT)
    VGS = VDS

    if VDS >= VGS - abs(VT):
        print(f"State 7 with VGS = {VGS:.2f}, ID = {ID:.6f}, VDS = {VDS:.2f}")
        print("Saturated")
    else:
        print("Operating in the linear region or invalid. Try again!")


#input
def select_state():
    print("Please select one of the following states:")
    print("1: State 1")
    print("2: State 2")
    print("3: State 3")
    print("4: State 4")
    print("5: State 5")
    print("6: State 6")
    print("7: State 7")
    

    selection = int(input("Your choice: "))
    
    if selection == 1:
        VGG = get_float_input("Enter VGG: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP0 = get_float_input("Enter VP0: ")
        state_1_p_channel(VGG, VDD, RD, IDSS, VP0)

    if selection == 2:
        VGG = get_float_input("Enter VGG: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_2_p_channel(VGG, VDD, RD, K, VT)

    elif selection == 3:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP0 = get_float_input("Enter VP0: ")
        state_3_p_channel(RSS, VDD, RD, IDSS, VP0)

    elif selection == 4:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_4_p_channel(RSS, VDD, RD, K, VT)

    elif selection == 5:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG1 = get_float_input("Enter RG1: ")
        RG2 = get_float_input("Enter RG2: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP0 = get_float_input("Enter VP0: ")
        state_5_p_channel(VDD, RD, RSS,RG1,RG2,IDSS, VP0)

    elif selection == 6:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RSS = get_float_input("Enter RSS: ")
        RG1 = get_float_input("Enter RG1: ")
        RG2 = get_float_input("Enter RG2: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_6_p_channel(VDD, RD, RSS,RG1,RG2, K, VT)

    elif selection == 7:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG = get_float_input("Enter RG: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_7_p_channel(VDD, RD, RG,K, VT)
    else:
        print("Invalid choice!")

select_state()
