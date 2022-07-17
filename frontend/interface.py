"""Contains class UserInterface."""
import sys
import os
import colorama
from colorama import Fore, Style
from backend.brain import Brain
from config import colorama_cfg as color


class UserInterface:
    """Class representing the user interface.

    This class implements methods about Human-Machine interaction
        whether it is printing outputs from the program or asking inputs
        from the user in order for them to browse the menus and options.
    A UserInterface instance stores an instance of the DBManager class
        to read and write data from and to the program's database.
    """

    def __init__(self):
        """Inits a user interface.

        After initializing attributes, prints the main menu and asks the
        user what they wish to do. See ask_user_input() documentation
            for additional information.
        Initializes colorama to handle colors inside the terminal.

        Attributes:
            brain: An instance of class brain.

        """
        os.system('cls||clear')
        self.brain = Brain()
        self.ask_user_input()
        colorama.init(autoreset=True)

    def ask_user_input(self):
        """Prints the main menu to the user and then asks them what they
        wish to do."""

        user_choice = 'N'
        while user_choice != '4':
            self.print_main_menu()
            user_choice = input("What do you want to do? ")
            user_choice = user_choice.strip()
            self.process_main_menu(user_choice)

    @staticmethod
    def print_main_menu():
        """Prints main menu detailing which action the user can do."""

        os.system('cls||clear')
        print(color.header_red.format("Main Menu"))
        print("0: Find Substitutes")
        print("1: Browse saved substitutes ")
        print("2: Update the database")
        print("3: Delete all saved substitutes")
        print("4: Exit program")

    def process_main_menu(self, user_choice):
        """Triggers the specific action the user chose to do.

        Args:
            user_choice: The char the user typed to decide what they
                wish to do.
        """

        if user_choice not in ['0', '1', '2', '3', '4']:
            print(f"{Fore.RED}{Style.BRIGHT}Invalid choice.\n"
                  f"Please, try again.{Style.RESET_ALL}")
        if user_choice == '0':
            self.browse_categories_v2()
        if user_choice == '1':
            self.browse_saved_products_v2()
        if user_choice == '2':
            self.update_db()
        if user_choice == '3':
            self.delete_saved_substitutes()
        if user_choice == '4':
            sys.exit(0)

    def update_db(self):
        """Interacts with the user regarding updating the database.

        Makes sure the user understand what they do then makes use of
            method update_db() from Brain class to proceed to the
            database update. See method update_db() documentation
            inside class Brain for additional information.

        """

        user_choice = input(f"{Style.BRIGHT}{Fore.RED}Are you sure you "
                            f"want to update the database? "
                            f"This will delete all your favorites as well. "
                            f"{Style.RESET_ALL} y/[n] ")
        user_choice = user_choice.strip().lower()
        if user_choice == "y":
            os.system('cls||clear')
            print(f"{color.plus_prfx}Updating database...")
            self.brain.update_db()
            input(f"{Style.DIM}Database updated."
                  f" Press enter key...{Style.RESET_ALL}")

    def delete_saved_substitutes(self):
        """Drops the entire program database.

        Makes sure the user understand what they do then makes use of
            method clear_db() in class DBManager to proceed to the
            deletion. See clear_db() documentation inside class
            DBManager for additional information.
        """

        user_choice = input(f"{Style.BRIGHT}{Fore.RED}Are you sure you "
                            f"want to erase all saved substitutes? "
                            f"{Style.RESET_ALL} y/[n] ")
        user_choice = user_choice.strip().lower()
        if user_choice == "y":
            print(f"{color.minus_prfx} Erasing...")
            self.brain.clear_saved_substitutes()
            input(f"{Style.DIM}Substitutes erased."
                  f" Press enter key...{Style.RESET_ALL}")

    def print_categories(self):
        """Prints the categories if there are any to print."""

        if not self.brain.categories_list:
            input("No categories yet, please update the database.")
        else:
            for category in self.brain.categories_list:
                print(f"{category.id}: {category.french_name}")

    def browse_categories_v2(self):
        """Starts the process to find substitutes to a product.

        It then proceed to print the categories to the user using
            print_categories().
        Method makes use of get_input_as_int() method to ask for user
            input and process it.
        """

        keep_running = True
        while keep_running:
            os.system('cls||clear')
            print(color.header_yellow.format("Find substitutes"))
            print("0 Go back")
            self.print_categories()
            user_choice = len(self.brain.categories_list) + 1
            while user_choice > len(self.brain.categories_list):
                user_choice = self.get_input_as_int(
                    "Chose a category (id number): ")
            if user_choice == 0:
                keep_running = False
                self.ask_user_input()
            elif user_choice < 0 or user_choice > len(
                    self.brain.categories_list):
                input(f"{Fore.RED}Invalid, try again...{Style.RESET_ALL}")
            else:
                self.browse_products_from_cat_v2(
                    self.brain.categories_list[user_choice - 1])

    def browse_products_from_cat_v2(self, category):
        """Navigates through products from a category.

        Args:
            category: The specified category.
        """

        page = 0
        keep_running = True
        while keep_running:
            os.system('cls||clear')
            if not category:
                input("Nothing to display yet, press enter key...")
                keep_running = False
            else:
                print(color.header_yellow.format(f"Browsing "
                                                 f"{category.french_name}"))
                print(f"Page: {page}")
                self.brain.fetch_brands_from_product_page(page, category)
                category.print_product_registry_page(page)
                user_choice = input(
                    "Please, chose what to do\n"
                    "[p]revious, [n]ext, [b]ack or type product number: ")
            user_choice = user_choice.strip().lower()
            keep_running, page = self.process_input_navigation(
                user_choice, category, page, keep_running)

    def process_input_navigation(
            self, user_choice, cat, page, keep_running):
        """Processes the user input regarding navigation in products.

        Args:
            user_choice: The user input.
            cat: The category that is being browsed.
            page: The current page.
            keep_running: Wether to keep running or not.

        Returns:
            keep_running: False if user wants to stop.
            page: the next page asked by the user.

        """

        if user_choice.isdecimal():
            user_choice = int(user_choice)
            if len(cat.product_registry[page]) >= user_choice > 0:
                keep_running = True
                os.system('cls||clear')
                print("Chosen product:")
                cat.product_registry[page][user_choice - 1].print_product()
                input("Press enter to continue.")
                self.print_substitutes(
                    cat.product_registry[page][user_choice - 1])
            else:
                input("Please enter a valid number. Press enter to continue.")
        else:
            keep_running, page = \
                self.page_navigation(user_choice,
                                     page, keep_running,
                                     len(cat.product_registry) - 1)
        return keep_running, page

    @staticmethod
    def page_navigation(user_choice, page, keep_running, max_page):
        """Determines which page user wants to navigate to.

        Args:
            user_choice: The user input
            page: integer indexing the current page
            keep_running: boolean indicating if user wants to keep
                browsing
            max_page: integer indexing the last page.

        Returns:

        """
        if user_choice not in ['p', 'n', 'b']:
            print("Invalid action")
        else:
            if user_choice == "p":
                page -= 1
                if page < 0:
                    page = max_page
            if user_choice == "n":
                page += 1
                if page > max_page:
                    page = 0
            if user_choice == "b":
                keep_running = False
        return keep_running, page

    def print_substitutes(self, product):
        """Browses substitutes to a product.

        Args:
            product: The product to replace.
        """

        self.brain.get_substitutes_to_product(product)
        page = 0
        keep_running = True
        while keep_running:
            os.system('cls||clear')
            if not product:
                input("Nothing to display yet, press enter key...")
                keep_running = False
            else:
                print(color.header_yellow.format(f"Substitutes to "
                                                 f"{product.french_name}"))
                print(f"Page: {page}")
                self.brain.fetch_brands_from_subst_page(page, product)
                product.print_substitute_registry_page(page)
                user_choice = input(
                    "Please, chose what to do\n"
                    "[p]revious, [n]ext, [b]ack or type product number: ")
            user_choice = user_choice.strip().lower()
            keep_running, page = self.process_input_nav_sub(user_choice,
                                                            product,
                                                            page,
                                                            keep_running)

    def process_input_nav_sub(self, user_choice, product, page, keep_running):
        """Processes the user input regarding navigation in substitutes.

        Args:
            user_choice: The user input.
            product: The product that is being browsed.
            page: The current page.
            keep_running: Wether to keep running or not.

        Returns:
            keep_running: False if user wants to stop.
            page: the next page asked by the user.

        """

        if user_choice.isdecimal():
            user_choice = int(user_choice)
            if len(product.substitute_registry[page]) >= user_choice > 0:
                keep_running = True
                chosen = product.substitute_registry[page][user_choice - 1]
                self.brain.fetch_stores_from_subst(chosen)
                os.system('cls||clear')
                chosen.print_product()
                self.save_product_v2(chosen, product)
            else:
                input("Please enter a valid number. Press enter to continue.")
        else:
            keep_running, page = \
                self.page_navigation(user_choice,
                                     page, keep_running,
                                     len(product.substitute_registry) - 1)
        return keep_running, page

    def save_product_v2(self, substitute, product):
        """Saves a substitute to the database.

        Method makes use of save_to_db() method from class DBManager to
            save substitute to database. Refer to this specific method for
            additional information.

        Args:
            substitute: The substitute that needs to be saved.
            product: The product to replace.
        """

        user_choice = input(f"{Fore.GREEN}Do you want to save"
                            f" {substitute.french_name}"
                            f"{Style.RESET_ALL} y/[n] ")
        if user_choice == "y":
            print(f"{color.plus_prfx}"
                  f"Saving {substitute.french_name} to database. ")
            success = self.brain.save_substitute_v2(substitute, product)
            if success:
                input(f"{color.plus_prfx}Product saved. Press enter key...")
            else:
                input(f"{color.minus_prfx}Product already saved. Press enter.")

    def browse_saved_products_v2(self):
        """Browses all saved substitutes by user."""

        page = 0
        keep_running = True
        while keep_running:
            os.system('cls||clear')
            # check if there are saved products
            if not self.brain.subst_reg \
                    and not self.brain.saved_sub_buf:
                input(f"{Fore.RED}"
                      f"Nothing to display yet{Style.RESET_ALL}"
                      f", press enter key...")
                keep_running = False
            else:
                print(color.header_green.format("Browsing substitutes"))
                print(f"Page: {page}")
                self.brain.buffer_check()
                self.brain.print_subst_reg_page(page)
                user_choice = input(
                    "Please, chose what to do\n"
                    "[p]revious, [n]ext, [b]ack or type product number: ")
                user_choice = user_choice.strip().lower()
                keep_running, page = self.process_input_saved(
                                                            user_choice,
                                                            page,
                                                            keep_running)

    def process_input_saved(self, choice, page, keep_running):
        """Processes the user input regarding navigation in favorites.

        Args:
            choice: The user input.
            page: The current page.
            keep_running: Wether to keep running or not.

        Returns:
            keep_running: False if user wants to stop.
            page: the next page asked by the user.

        """

        if choice.isdecimal():
            choice = int(choice)
            if len(self.brain.subst_reg[page]) \
                    >= choice > 0:
                keep_running = True
                chosen = \
                    self.brain.subst_reg[page][choice - 1]
                self.delet_fav_v2(chosen)
            else:
                print("Please enter a valid number")
        else:
            keep_running, page = \
                self.page_navigation(choice, page, keep_running,
                                     len(self.brain.subst_reg) - 1)
        return keep_running, page

    def delet_fav_v2(self, fav):
        """Starts process of deleting a favorite.

        A favorite can be linked to one or several products.
        del_mul_from_fav is used if favorite is linked to several
            products.
        del_single_fav is used if favorite is linked to only one
            product.

        Args:
            fav: The fovorite to process.
        """

        os.system('cls||clear')
        fav.print_product()
        if len(fav.substitute_to) > 1:
            self.del_mul_frm_fav(fav)
        elif len(fav.substitute_to) == 1:
            self.del_single_fav(fav)

    def del_single_fav(self, fav):
        """Handle favorite deletion when linked to only one product.

        Args:
            fav: The favorite to delete.
        """

        user_choice = input(f"{Fore.MAGENTA}Do you want to delete "
                            f"{fav.french_name} from your favorites?"
                            f"{Style.RESET_ALL} y/n: ")
        user_choice = user_choice.strip().lower()
        if user_choice == "y":
            self.brain.del_all_in_fav(fav)
        elif user_choice == "n":
            pass
        else:
            input(f"{Fore.RED}Invalid, try again...{Style.RESET_ALL}")
            self.delet_fav_v2(fav)

    def del_mul_frm_fav(self, fav):
        """Handle favorite deletion when linked to multiple product.

        Args:
            fav: The favorite product to delete.
        """

        user_choice = input(f"{Fore.MAGENTA}What do you want to remove? "
                            f"{Style.RESET_ALL}"
                            f"(product number or [a]ll or [b]ack): ")
        user_choice = user_choice.strip().lower()
        if user_choice.isdecimal():
            user_choice = int(user_choice)
            if user_choice < 0 or user_choice > len(fav.substitute_to):
                input(f"{Fore.RED}Invalid, try again...{Style.RESET_ALL}")
            else:
                self.brain.del_one_in_fav(fav, user_choice)
            self.delet_fav_v2(fav)
        if user_choice == 'a':
            self.brain.del_all_in_fav(fav)
        if user_choice == 'b':
            pass

    @staticmethod
    def get_input_as_int(message):
        """Converts user input into an integer for easier processing.

        Args:
            message: The user input

        Returns:
            The user input as an integer.
        """

        while True:
            try:
                message = message.strip()
                user_input = int(input(message))
            except ValueError:
                input(f"{Fore.RED}Invalid, try again...{Style.RESET_ALL}")
                continue
            else:
                return user_input
            break
