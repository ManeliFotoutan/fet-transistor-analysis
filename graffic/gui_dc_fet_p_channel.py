import numpy as np
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve
import tkinter as tk


#calculate ID and VGS
def calculate_ID_state_1_p_channel(IDSS, VGS, VPO):
    ID = IDSS * (1 - VGS / abs(VPO))**2
    return ID

def calculate_ID_state_2_p_channel(K, VT):
    ID = K * (1 - abs(VT))**2
    return ID


def calculate_IDandVGS_state_3_p_channel(IDSS, RSS, VPO):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS - ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / abs(VPO))**2  
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

def calculate_IDandVGS_state_5_p_channel(Vth, RSS, IDSS, VPO):
    def equations(vars):
        ID, VGS = vars
        eq1 = VGS +Vth - ID * RSS  
        eq2 = ID - IDSS * (1 - VGS / abs(VPO))**2  
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
def state_1_p_channel(VDD, VGG, RD, IDSS, VPO):
    VGS = VGG  
    ID = calculate_ID_state_1_p_channel(IDSS, VGS, VPO)
    VDS = calculate_VDS_state_p_channel_1and2_p_channel(VDD, ID, RD)
    if VDS <= VGS - abs(VPO):
        result = "Saturated"
        details = f"State 1 with VGS = {VGS} V , ID = {ID} mA, VDS = {VDS} V "
    else:
        result = "Not Saturated"
        details = f"State 1 with VGS = {VGS} V , ID = {ID} mA , VDS = {VDS} V "
    return result, details

def state_2_p_channel(VDD, VGG, RD, K, VT):
    VGS = VGG
    ID = calculate_ID_state_2_p_channel(K, VT)
    VDS = calculate_VDS_state_p_channel_1and2_p_channel(VDD, ID, RD)
    if VDS < VGS - VT:
        result = "Saturated"
        details = f"State 2 with VGS = {VGS} V , ID = {ID} mA , VDS = {VDS} V "
    else: 
        result = "Not Saturated"
        details = f"State 2 with VGS = {VGS} V , ID = {ID} mA , VDS = {VDS} V "
    return result, details

def state_3_p_channel(VDD, RD, RSS, IDSS, VPO):
    ID, VGS = calculate_IDandVGS_state_3_p_channel(IDSS, RSS, VPO)
    VDS = calculate_VDS_state_p_channel(VDD, ID, RD, RSS)   
    if VDS <= VGS - abs(VPO):
        result = "Saturated"
        details = f"State 3 with VGS = {VGS } V , ID = {ID} mA , VDS={VDS} V "
    else:
        result = "Not Saturated"
        details =  f"State 3 with VGS = {VGS } V , ID = {ID} mA , VDS={VDS} V "
    return result, details

def state_4_p_channel(VDD, RD, RSS, K, VT):
    ID , VSG  = calculate_IDandVGS_state_4_p_channel(K, RSS, VT)
    VSD = calculate_VDS_state_p_channel(VDD, ID, RD , RSS)
    if VSD > abs(VSG - VT):
        result = "Saturated"
        details = f"State 4 (p-channel) with VSG ={VSG } V , ID = {ID} mA, VSD = {VSD} V "
    else:
        result = "Not Saturated"
        details = f"State 4 (p-channel) with VSG ={VSG } V , ID={ID} mA , VSD={VSD} V "
    return result, details

def state_5_p_channel(VDD, RD, RG1, RG2, RSS, IDSS, VPO):
    Vth=calculate_Vth_p_channel(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_5_p_channel(Vth,RSS,IDSS,VPO)
    VDS = calculate_VDS_state_p_channel(VDD, ID, RD , RSS)
    if VDS> VGS - VPO:
        result = "Saturated"
        details = f"State 5 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
    else:
        result = "Not Saturated"
        details = f"State 5 with Vth={Vth} V ,VGS ={VGS } V , ID={ID} mA , VDS={VDS} V "
    return result, details

def state_6_p_channel(VDD, RD, RG1, RG2, RSS, K, VT):
    Vth=calculate_Vth_p_channel(VDD,RG1,RG2)
    ID , VGS  = calculate_IDandVGS_state_6_p_channel(Vth,RSS,K,VT)
    VDS = calculate_VDS_state_p_channel(VDD, ID, RD , RSS)
    if VDS> VGS - VT:
        result = "Saturated"
        details = f"State 6 with VGS ={VGS } V , ID={ID} mA , VDS={VDS} V ,Vth = {Vth} V"
    else:
        result = "Not Saturated"
        details = f"State 5 with Vth={Vth} V ,VGS ={VGS } V, ID={ID} mA, VDS={VDS} V "
    return result, details

def state_7_p_channel(VDD, RD, RG, K, VT):
    ID, VDS = calculate_IDandVDS_state_7_p_channel(VDD, RD, K, VT)
    VGS = VDS

    if VDS >= VGS - abs(VT):
        result = "Saturated" 
        details = f"State 7 with VGS = {VGS:.2f} V , ID = {ID:.6f} mA , VDS = {VDS:.2f} V "
    else:
        result = "Operating in the linear region or invalid. Try again!"
        details = f"State 7 with VGS = {VGS:.2f} V , ID = {ID:.6f} mA , VDS = {VDS:.2f} V "
    return result, details