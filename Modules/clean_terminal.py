import os

def limpiar_terminal():
    if os.name == 'nt':
        os.system('cls') # Windows
    else:
        os.system('clear') # Linux

