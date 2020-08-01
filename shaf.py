#!/usr/bin/python3

from pyfiglet import Figlet
from art import text2art

import colorama as cl
import sys, os
import captcha

def clearScreen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def getBanner():
    # clearScreen()
    f = Figlet(font='doom')
    logo = f.renderText("SHAF")
    print(cl.Fore.RED + logo)
    description = "Scraper Hacking Forum" #v1.0.0"
    print(cl.Fore.BLUE + description)
    author_text = "By Santiago Rocha"
    print(cl.Fore.BLUE + author_text)

def menu():
    try:
        options = input("""
Select one of the modules below:

    [1] Login Form Inputs
    [2] Captcha Solver
    [3] Honeypots
    [4] Scraper
    [5] Exit
    Enter the module number: """)

        if options == str(1):
            import hiddenInputs
            print("*"*45)
            hiddenInputs.autVerif()
            print("*"*45)
        elif options == str(2):
            print("*"*45)
            captcha.captcha()
            print("*"*45)
        elif options == str(3):
            import hiddenInputs
            print("*"*45)
            hiddenInputs.hiddenVerif()
            print("*"*45)
        elif options == str(4):
            import scraper
            print("*"*45)
            scraper.run()
            print("*"*45)
        elif options == str(5):
            sys.exit
        else:
            print("\nOption not available. Please try again...")
            menu()

    except KeyboardInterrupt:
        menu()

def main():
    cl.init(autoreset=True)
    getBanner()
    menu()

if __name__ == "__main__":
    main()


