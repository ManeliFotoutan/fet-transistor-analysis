import numpy as np
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve
import extract_text


#calculate ID and VGS
def calculate_ID_state_1(IDSS, VGS, VPO):
    ID = IDSS * (1 - VGS / VPO)**2
    return ID

def calculate_ID_state_2(K,VT):
    ID = K * (1 - VT)**2
    return ID

def calculate_IDandVGS_state_3(IDSS, RSS, VPO):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS + ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / VPO)**2  
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

def calculate_IDandVGS_state_5(Vth, RSS, IDSS, VPO):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS -Vth + ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / VPO)**2  
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
        eq1 = ID - IDSS * (1 - VDS / VP) ** 2
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

def calculate_not_saturated_parameters_state1(VDD,VGG,RD, IDSS, VPO):

    VDS, VGS, ID = symbols('VDS VGS ID')
    
    eq1 = Eq(VGS, -VGG)
    eq2 = Eq(VDS, VDD - ID * RD)
    eq3 = Eq(ID, IDSS * (2 * (VGS / VPO - 1) * (VDS / VPO) - (VDS / VPO)**2))
    
    ID_solutions = solve(eq3.subs(VGS, -VGG).subs(VDS, VDD - ID * RD), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = -VGG
    VDS_selected = VDD - ID_selected * RD
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state2(VDD,VGG,RD, K, VT):
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

def calculate_not_saturated_parameters_state3(VDD,RD,RSS, IDSS, VPO):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, IDSS * (2 * (VGS / VPO - 1) * (VDS / VPO) - (VDS / VPO)**2))
    
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

def calculate_not_saturated_parameters_state5(VDD,RD,RSS,Vth, IDSS, VPO):
    VDS, VGS, ID = symbols('VDS VGS ID')

    eq = Eq(ID, IDSS * (2 * (VGS / VPO - 1) * (VDS / VPO) - (VDS / VPO)**2))
    
    ID_solutions = solve(eq.subs(VGS, Vth - ID * RSS).subs(VDS, VDD - ID * (RD + RSS)), ID)
    
    real_IDs = [sol.evalf() for sol in ID_solutions if sol.is_real and sol > 0]
    
    if not real_IDs:
        return None, None, None
    
    ID_selected = min(real_IDs)
    
    VGS_selected = Vth - ID_selected * RSS
    VDS_selected = VDD - ID_selected * (RD + RSS)
    
    return VDS_selected, VGS_selected, ID_selected

def calculate_not_saturated_parameters_state6(VDD,RD,RSS,Vth, K, VT):
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
def state_1_n_channel(VDD,VGG,RD, IDSS, VPO):
    VGS = -VGG  
    ID = calculate_ID_state_1(IDSS, VGS, VPO)
    VDS = calculate_VDS_state_1and2(VDD, ID, RD)
    if VDS> VGS - VPO and ID !=0:
        details = f"State 1 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V"
        result = "Saturated"
        print(details)
    else:
        VDS,VGS,ID = calculate_not_saturated_parameters_state1(VDD,VGG,RD, IDSS, VPO)
        if VDS > 0 and VDS < VGS - VPO :
            details = f"State 1 with VGS ={VGS } V, ID={ID} mA , VDS = {VDS} V "
            result = "Ohmic"
        else:
            result = "Cuttoff"
            details =""
        return result , details

def state_2_n_channel(VGG, VDD, RD, K, VT):
    VGS = -VGG  
    ID = calculate_ID_state_2(K, VT)
    VDS = calculate_VDS_state_1and2(VDD, ID, RD)
    if VDS> VGS - VT and ID !=0:
        details = f"State 2 with VGS ={VGS } V, ID={ID} mA, VDS={VDS} V "
        result = "Saturated"

    else:
        VDS,VGS,ID = calculate_not_saturated_parameters_state2(VGG, VDD, RD, K, VT)
        if VDS > 0 and VDS < VGS - VT :
            details = f"State 2 with VGS = {VGS } V , ID={ID} mA , VDS={VDS} V "
            result = "Ohmic"
        else :
            details = ""
            result = "Cuttoff"
    return result , details

def state_3_n_channel(VDD,RD,RSS, IDSS, VPO):
    ID , VGS  = calculate_IDandVGS_state_3(IDSS, RSS, VPO)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS > VGS - VPO and ID !=0:
        details = f"State 3 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
        result = "Saturated"
    else:
        VDS,VGS,ID = calculate_not_saturated_parameters_state3(VDD,RD,RSS, IDSS, VPO)
        if VDS > 0 and VDS < VGS - VPO :
            details = f"State 3 with VGS ={VGS } V, ID={ID} mA , VDS={VDS} V "
            result = "Ohmic"
        else:
            details = ""
            result = "Cuttoff"
    return result , details

def state_4_n_channel(RSS, VDD, RD, K, VT):
    ID , VGS  = calculate_IDandVGS_state_4(K, RSS, VT)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS> VGS - VT and ID !=0:
        details = f"State 4 with VGS ={VGS } V , ID={ID} mA , VDS = {VDS} V "
        result = "Saturated"
    else:
        ID = calculate_not_saturated_parameters_state4(RSS, VDD, RD, K, VT)
        if VDS > 0 and VDS < VGS - VT :
            details = f"State 4 with VGS ={VGS} V , ID={ID} mA , VDS={VDS} V "
            result = "Ohmic"
        else :
            details = f"State 4 with VGS ={VGS } V , ID={ID} mA, VDS={VDS} V "
            result = "Cuttoff"
    return result , details

def state_5_n_channel(VDD,RD,RG1,RG2,RSS,IDSS, VPO):
    Vth=calculate_Vth(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_5(Vth,RSS,IDSS,VPO)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS> VGS - VPO and ID !=0:
        details = f"State 5 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
        result = "Saturated"
    else:
        ID = calculate_not_saturated_parameters_state5(VDD, RD, RSS,Vth,IDSS, VPO)
        if VDS > 0 and VDS < VGS - VPO :
            details = f"State 5 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
            result = "Ohmic"          
        else:
            details = ""
            result = "Cuttoff"
    return result , details

def state_6_n_channel(VDD,RD,RG1,RG2,RSS, K, VT):
    Vth=calculate_Vth(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_6(Vth,RSS,K,VT)
    VDS = calculate_VDS_Other_states(VDD, ID, RD , RSS)
    if VDS> VGS - VT and ID !=0:
        details = f"State 6 with VGS ={VGS } V , ID={ID} mA, VDS={VDS} V "
        result = "Saturated"
    else:
        ID = calculate_not_saturated_parameters_state6(VDD,RD,RSS,Vth, K, VT)
        if VDS > 0 and VDS < VGS - VT :
            details = f"State 6 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
            result = "Ohmic"
        else :
            details = ""
            result = "Cuttoff"
            
    return result , details

def state_7_n_channel(VDD, RD, RG ,K, VT):
    ID , VDS  = calculate_IDandVDS_state_7(VDD,RD,K,VT)
    VGS = VDS
    if VDS> VGS - VT:
        details = f"State 7 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
        result = "Saturated"
    else :
        result = "Try Again" 
        details = ""
    return result , details


def state_8_n_channel(VDD, RD, RG,IDSS, VP):
    ID , VDS  = calculate_IDandVDS_state_8(VDD,RD,IDSS,VP)
    VGS = VDS
    if VDS> VGS - VP:
        details = f"State 7 with VGS ={VGS } V , ID={ID} mA,  VDS={VDS} V "
        result = "Saturated"
    else :
        result = "Try Again"
        details = ""
    return result , details
