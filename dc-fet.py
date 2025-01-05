import numpy as np
from scipy.optimize import fsolve
import dc_fet_gui
from sympy import symbols, Eq, solve


#input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

#calculate ID and VGS
def calculate_ID_state_1(IDSS, VGS, VP0):
    ID = IDSS * (1 - VGS / VP0)**2
    return ID

def calculate_ID_state_2(K,VT):
    ID = K * (1 - VT)**2
    return ID

def calculate_IDandVGS_state_3(IDSS, RSS, VP0):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS + ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / VP0)**2  
        return [eq1, eq2]

    initial_guess = [1, -1]

    solution = fsolve(equations, initial_guess)
    
    ID1 = solution[0]

    initial_guess2 = [-1, 1]  
    solution2 = fsolve(equations, initial_guess2)

    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS = -ID * RSS  
    return ID, VGS

def calculate_IDandVGS_state_4(K, RSS, VT):
    def equations(vars):
        VGS = vars[0]
        ID = -VGS / RSS   
        eq2 = ID - K * (VGS - VT)**2
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
    VGS = -ID * RSS  
    
    return ID, VGS

def calculate_IDandVGS_state_5(Vth, RSS, IDSS, VP0):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS -Vth + ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / VP0)**2  
        return [eq1, eq2]

    initial_guess = [1, -1]  
    solution = fsolve(equations, initial_guess)
    
    ID1 = solution[0]

    initial_guess2 = [-1, 1]  
    solution2 = fsolve(equations, initial_guess2)

    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS = Vth - ID * RSS  
    return ID, VGS


def calculate_IDandVGS_state_6(Vth, RSS, K, VT):
    def equations(vars):
        ID, VGS = vars
        eq1 = ID - K * (VGS - VT)**2
        eq2 = VGS + (-Vth + ID * RSS)
        return [eq1, eq2]

    initial_guess = [1,-1]
    solution1 = fsolve(equations, initial_guess)
    ID1 = solution1[0]

    initial_guess2 = [-1, 1]
    solution2 = fsolve(equations, initial_guess2)
    ID2 = solution2[0]

    ID = min(ID1, ID2)
    VGS = Vth - ID * RSS    
    
    return ID, VGS

def calculate_IDandVDS_state_7(VDD, RD, K, VT):
    def equations(vars):
        ID, VDS = vars
        eq1 = ID - K * (VDS - VT)**2
        eq2 = VDS - (VDD - ID * RD)
        return [eq1, eq2]

    initial_guess1 = [1, VDD - 1]
    solution1 = fsolve(equations, initial_guess1)
    ID1, VDS1 = solution1

    initial_guess2 = [0.1, VDD - 0.1]
    solution2 = fsolve(equations, initial_guess2)
    ID2, VDS2 = solution2

    if ID1 < ID2:
        ID, VDS = ID1, VDS1
    else:
        ID, VDS = ID2, VDS2

    return ID, VDS

def calculate_IDandVDS_state_8(VDD,RD,IDSS,VP):
    def equations(vars):
        ID, VDS = vars
        eq1 = ID - (IDSS(1-VDS//VP)**2)
        eq2 = VDS - (VDD - ID * RD)
        return [eq1, eq2]

    initial_guess1 = [1, VDD - 1]
    solution1 = fsolve(equations, initial_guess1)
    ID1, VDS1 = solution1

    initial_guess2 = [0.1, VDD - 0.1]
    solution2 = fsolve(equations, initial_guess2)
    ID2, VDS2 = solution2

    if ID1 < ID2:
        ID, VDS = ID1, VDS1
    else:
        ID, VDS = ID2, VDS2

    return ID, VDS

def calculate_not_saturated_parameters_state1(VGG, VDD, RD, IDSS, VP0):

    VDS, VGS, ID = symbols('VDS VGS ID')
    
    eq1 = Eq(VGS, -VGG)
    eq2 = Eq(VDS, VDD - ID * RD)
    eq3 = Eq(ID, IDSS * (2 * (VGS / VP0 - 1) * (VDS / VP0) - (VDS / VP0)**2))
    
    ID_solutions = solve(eq3.subs(VGS, -VGG).subs(VDS, VDD - ID * RD), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = -VGG
    VDS_selected = VDD - ID_selected * RD
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state2(VGG, VDD, RD, K, VT):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, K * (2 * (VDS - VT) -VDS**2))
    
    ID_solutions = solve(eq.subs(VGS, -VGG).subs(VDS, VDD - ID * RD), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = -VGG
    VDS_selected = VDD - ID_selected * RD
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state3(RSS, VDD, RD, IDSS, VP0):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, IDSS * (2 * (VGS / VP0 - 1) * (VDS / VP0) - (VDS / VP0)**2))
    
    ID_solutions = solve(eq.subs(VGS, ID*RSS).subs(VDS, VDD-ID(RD+RSS)), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected =  -ID*RSS
    VDS_selected = VDD - ID *(RD + RSS )
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state4(RSS, VDD, RD, K, VT):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, K * (2 * (VDS - VT) -VDS**2))
    
    ID_solutions = solve(eq.subs(VGS, ID*RSS).subs(VDS, VDD-ID*(RD+RSS)), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = -ID*RSS
    VDS_selected = VDD - ID*(RD + RSS )
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state5(VDD, RD, RSS, Vth, IDSS, VP0):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, IDSS * (2 * (VGS / VP0 - 1) * (VDS / VP0) - (VDS / VP0)**2))
    
    ID_solutions = solve(eq.subs(VGS, Vth - ID * RSS).subs(VDS, VDD - ID * (RD + RSS)), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = Vth - ID_selected * RSS
    VDS_selected = VDD - ID_selected * (RD + RSS)
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state6(VDD, RD, RSS, Vth, K, VT):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, K * (2 * (VDS - VT) - VDS**2))
    
    ID_solutions = solve(eq.subs(VGS, Vth - ID * RSS).subs(VDS, VDD - ID * (RD + RSS)), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = Vth - ID_selected * RSS
    VDS_selected = VDD - ID_selected * (RD + RSS)
    
    return VDS_selected, VGS_selected, ID_selected


#calculate VDS
def calculate_VDS_state_1and2(VDD, ID, RD):
    VDS = VDD - (ID * RD)  
    return VDS

def calculate_VDS_Other_states(VDD, ID, RD , RSS):
    VDS = VDD - ID * (RSS+RD) 
    return VDS

#Vth
def calculate_Vth(VDD,RG1,RG2):
    return VDD*(RG2/(RG1+RG2))

#States
def state_1(VGG, VDD, RD, IDSS, VP0):
    VGS = -VGG  
    ID = calculate_ID_state_1(IDSS, VGS, VP0)
    VDS = calculate_VDS_state_1and2(VDD, ID, RD)
    if VDS> VGS - VP0 and ID !=0:
        print(f"State 1 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else:
        VDS,VGS,ID = calculate_not_saturated_parameters_state1(VGG, VDD, RD, IDSS, VP0)
        if VDS > 0 and VDS < VGS - VP0 :
            print(f"State 1 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Ohmic")
        else:
            print("Cutoff")

def state_2(VGG, VDD, RD, K, VT):
    VGS = -VGG  
    ID = calculate_ID_state_2(K, VT)
    VDS = calculate_VDS_state_1and2(VDD, ID, RD)
    if VDS> VGS - VT and ID !=0:
        print(f"State 2 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else:
        VDS,VGS,ID = calculate_not_saturated_parameters_state2(VGG, VDD, RD, K, VT)
        if VDS > 0 and VDS < VGS - VT :
            print(f"State 2 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Ohmic")
        else :
            # print(f"State 2 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Cutoff")

def state_3(RSS, VDD, RD, IDSS, VP0):
    ID , VGS  = calculate_IDandVGS_state_3(IDSS, RSS, VP0)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS > VGS - VP0 and ID !=0:
        print(f"State 3 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else:
        VDS,VGS,ID = calculate_not_saturated_parameters_state3(RSS, VDD, RD, IDSS, VP0)
        if VDS > 0 and VDS < VGS - VP0 :
            print(f"State 3 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Ohmic")
        else:
            # print(f"State 3 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Cutoff")


def state_4(RSS, VDD, RD, K, VT):
    ID , VGS  = calculate_IDandVGS_state_4(K, RSS, VT)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS> VGS - VT and ID !=0:
        print(f"State 4 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else:
        ID = calculate_not_saturated_parameters_state4(RSS, VDD, RD, K, VT)
        if VDS > 0 and VDS < VGS - VT :
            print(f"State 4 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Ohmic")
        else :
            # print(f"State 4 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Cutoff")

def state_5(VDD, RD, RSS,RG1,RG2,IDSS, VP0):
    Vth=calculate_Vth(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_5(Vth,RSS,IDSS,VP0)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS> VGS - VP0 and ID !=0:
        print(f"State 5 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else:
        ID = calculate_not_saturated_parameters_state5(VDD, RD, RSS,Vth,IDSS, VP0)
        if VDS > 0 and VDS < VGS - VP0 :
            print(f"State 5 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Ohmic")          
        else:
            print(f"State 5 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Cutoff")

def state_6(VDD, RD, RSS,RG1,RG2, K, VT):
    Vth=calculate_Vth(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_6(Vth,RSS,K,VT)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS> VGS - VT and ID !=0:
        print(f"State 6 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else:
        ID = calculate_not_saturated_parameters_state6(VDD, RD, RSS,Vth, K, VT)
        if VDS > 0 and VDS < VGS - VT :
            print(f"State 6 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Ohmic")
        else :
            # print(f"State 6 with VGS ={VGS }, ID={ID}, VDS={VDS}")
            print("Cutoff")

def state_7(VDD, RD, RG ,K, VT):
    ID , VDS  = calculate_IDandVDS_state_7(VDD,RD,K,VT)
    VGS = VDS
    if VDS> VGS - VT:
        print(f"State 7 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else :
        print("try again !")      


def state_8(VDD, RD, RG,IDSS, VP):
    ID , VDS  = calculate_IDandVDS_state_8(VDD,RD,IDSS,VP)
    VGS = VDS
    if VDS> VGS - VP:
        print(f"State 7 with VGS ={VGS }, ID={ID}, VDS={VDS}")
        print("Saturated")
    else :
        print("try again !") 
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
    print("8: State 8")

    selection = int(input("Your choice: "))
    
    if selection == 1:
        VGG = get_float_input("Enter VGG: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP0 = get_float_input("Enter VP0: ")
        state_1(VGG, VDD, RD, IDSS, VP0)

    if selection == 2:
        VGG = get_float_input("Enter VGG: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_2(VGG, VDD, RD, K, VT)

    elif selection == 3:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP0 = get_float_input("Enter VP0: ")
        state_3(RSS, VDD, RD, IDSS, VP0)

    elif selection == 4:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_4(RSS, VDD, RD, K, VT)

    elif selection == 5:
        RSS = get_float_input("Enter RSS: ")
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG1 = get_float_input("Enter RG1: ")
        RG2 = get_float_input("Enter RG2: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP0 = get_float_input("Enter VP0: ")
        state_5(VDD, RD, RSS,RG1,RG2,IDSS, VP0)

    elif selection == 6:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RSS = get_float_input("Enter RSS: ")
        RG1 = get_float_input("Enter RG1: ")
        RG2 = get_float_input("Enter RG2: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_6(VDD, RD, RSS,RG1,RG2, K, VT)

    elif selection == 7:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG = get_float_input("Enter RG: ")
        K = get_float_input("Enter K: ")
        VT = get_float_input("Enter VT: ")
        state_7(VDD, RD, RG,K, VT)

    elif selection == 8:
        VDD = get_float_input("Enter VDD: ")
        RD = get_float_input("Enter RD: ")
        RG = get_float_input("Enter RG: ")
        IDSS = get_float_input("Enter IDSS: ")
        VP = get_float_input("Enter VP: ")
        state_8(VDD, RD, RG,IDSS, VP)

    else:
        print("Invalid choice!")
        
def solve_dc_fet_problem(state, params):
    if state == 1:
        VGG, VDD, RD, IDSS, VP0 = params
        state_1(VGG, VDD, RD, IDSS, VP0)
    elif state == 2:
        VGG, VDD, RD, K, VT = params
        state_2(VGG, VDD, RD, K, VT)
    elif state == 3:
        RSS, VDD, RD, IDSS, VP0 = params
        state_3(RSS, VDD, RD, IDSS, VP0)
    elif state == 4:
        RSS, VDD, RD, K, VT = params
        state_4(RSS, VDD, RD, K, VT)
    elif state == 5:
        RSS, VDD, RD, RG1, RG2, IDSS, VP0 = params
        state_5(VDD, RD, RSS, RG1, RG2, IDSS, VP0)
    elif state == 6:
        VDD, RD, RSS, RG1, RG2, K, VT = params
        state_6(VDD, RD, RSS, RG1, RG2, K, VT)
    elif state == 7:
        VDD, RD, RG, K, VT = params
        state_7(VDD, RD, RG, K, VT)
    elif state == 8:
        VDD, RD, RG,IDSS, VP = params
        state_8(VDD, RD, RG,IDSS, VP)
    else:
        print("Invalid state selected!")

# select_state()

if __name__ == "__main__":
    dc_fet_gui.launch_gui(solve_dc_fet_problem)
