from colorama import Fore
from colorama import Style

def log(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")