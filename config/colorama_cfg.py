"""
Colorama config file

This files defines colors and style used in the app to decorate text.
"""

from colorama import Fore, Style

plus_prfx = "[" + Fore.GREEN + "+" + Style.RESET_ALL + "] "

minus_prfx = "[" + Fore.RED + "-" + Style.RESET_ALL + "] "

header_red = Fore.CYAN + "=" * 40 + Style.RESET_ALL + \
         Fore.RED + Style.BRIGHT + "\n{}\n" + Style.RESET_ALL + \
         Fore.CYAN + "-" * 20 + Style.RESET_ALL

header_magenta = Fore.CYAN + "=" * 40 + Style.RESET_ALL + \
         Fore.MAGENTA + Style.BRIGHT + "\n{}\n" + Style.RESET_ALL + \
         Fore.CYAN + "-" * 20 + Style.RESET_ALL

header_yellow = Fore.CYAN + "=" * 40 + Style.RESET_ALL + \
         Fore.YELLOW + Style.BRIGHT + "\n{}\n" + Style.RESET_ALL + \
         Fore.CYAN + "-" * 20 + Style.RESET_ALL

header_blue = Fore.CYAN + "=" * 40 + Style.RESET_ALL + \
         Fore.BLUE + Style.BRIGHT + "\n{}\n" + Style.RESET_ALL + \
         Fore.CYAN + "-" * 20 + Style.RESET_ALL

header_green = Fore.CYAN + "=" * 40 + Style.RESET_ALL + \
              Fore.GREEN + Style.BRIGHT + "\n{}\n" + Style.RESET_ALL + \
              Fore.CYAN + "-" * 20 + Style.RESET_ALL

header_cyan = Fore.CYAN + "=" * 40 + Style.RESET_ALL + \
               Fore.CYAN + Style.BRIGHT + "\n{}\n" + Style.RESET_ALL + \
               Fore.CYAN + "-" * 20 + Style.RESET_ALL
