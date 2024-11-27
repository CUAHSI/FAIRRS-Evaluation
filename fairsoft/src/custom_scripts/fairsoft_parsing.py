import pandas as pd 

def extract_indicators(fairsoft_dict):

    F1 = fairsoft_dict['F1']
    F2 = fairsoft_dict['F2']
    F3 = fairsoft_dict['F3']

    A1 = fairsoft_dict['A1']
    A2 = fairsoft_dict['A2']
    A3 = fairsoft_dict['A3']

    I1 = fairsoft_dict['I1']
    I2 = fairsoft_dict['I2']
    I3 = fairsoft_dict['I3']
                       
    R1 = fairsoft_dict['R1']
    R2 = fairsoft_dict['R2']
    R3 = fairsoft_dict['R3']
    R4 = fairsoft_dict['R3']

    return F1,F2,F3,A1,A2,A3,I1,I2,I3,R1,R2,R3,R4


