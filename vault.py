import os
from time import sleep
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from services.file_service import save_data_to_file, load_data_from_file
from services.encryption_service import encrypt, decrypt

console = Console()


def add_password(password_object, password_list):
    new_list = password_list.copy()
    new_list.append(password_object)
    return new_list


def prompt_add_password():
    website_name = Prompt.ask("Enter website name").lower()
    username = Prompt.ask("Enter username for {}".format(website_name))
    password = Prompt.ask("Enter password")
    return {"website_name": website_name, "username": username, "password": password}


def handle_add_account(password_list, master_password):
    account_object = prompt_add_password()
    new_password_list = add_password(account_object, password_list)
    write(new_password_list, master_password)
    console.print("Your new account and password have been saved \n")
    console.print("Returning...")
    return new_password_list


def handle_show_account(p_list):
    a = prompt_account_name()
    b = None
    for i in range(len(p_list)):
        if p_list[i]["website_name"] == a:
            b = [p_list[i]]
    print_accounts(b)


def prompt_account_name():
    a = Prompt.ask("Enter website name").lower()
    console.print("\n")
    return a

def delete_account_from_list(account_list, account_name):
    for account in account_list:
        new_account_list = []
        if account["website_name"] != account_name:
            new_account_list.append(account)
        return new_account_list
def handle_delete_account(account_list):
    nbr_accounts = len(account_list)
    website_to_delete = prompt_account_name()
    new_account_list = delete_account_from_list(account_list, website_to_delete)
    save_account_list(new_account_list, new_account_list["password"])




    if len(account_list) == nbr_accounts:
        console.print("No accounts were found matching this website name!")
    else:
        console.print("Account {} successfully deleted from vault".format(a))


def handle_quit():
    console.print("Quitting...")
    quit()

def load_account_list(password):
    """Load the account list from the encrypted vault"""
    ciphered_data = load_data_from_file("./ciphered_vault")
    return decrypt(ciphered_data, password)


def save_account_list(password_list, password):
    """Save the account list in the encrypted vault"""
    ciphered_list = encrypt(password_list, password)
    save_data_to_file("./ciphered_vault", ciphered_list)


def handle_login_existing_account():
    password = input("Enter your master password: ")
    console.print("")

    # Try and decipher the vault to check master password
    try:
        password_list = load_account_list(password)
        return password_list, password
    except Exception:
        console.print("WRONG PASSWORD !\n")
        exit(1)


def handle_register_new_account():
    console.print("This is a new account !\n")
    password = Prompt.ask("Please enter a master password")
    console.print("")
    write([], password)
    return [], password


def show_options():
    table = Table(title="Options")

    table.add_column("Option", style="cyan")
    table.add_column("Name", style="magenta")

    # adding the rows
    table.add_row("1", "Store new website account")
    table.add_row("2", "Retrieve website account")
    table.add_row("3", "Delete website account")
    table.add_row("4", "Quit the program")
    table.add_row("5", "Show all saved accounts")
    table.add_row("6", "Delete everything")

    console.print(table, justify="center")


def print_accounts(p_list):
    table = Table(title="Options")

    table.add_column("Account name", style="cyan")
    table.add_column("User name", style="magenta")
    table.add_column("Password", style="magenta")

    # adding the rows
    for i in range(len(p_list)):
        table.add_row(p_list[i]["website_name"], p_list[i]["username"], p_list[i]["password"])

    console.print(table, justify="center")


def main():
    files = os.listdir()
    console.clear()
    console.print("[blue underline]WELCOME TO PASSKEEP", justify="center")

    # Account already exists
    if "ciphered_vault" in files:
        p_list, master_password = handle_login_existing_account()

    # Account creation phase
    else:
        p_list, master_password = handle_register_new_account()

    while True:
        console.rule()

        show_options()

        option = Prompt.ask("What do you want to do ? ")

        if option == "1":
            p_list = handle_add_account(p_list, master_password)

        elif option == "2":
            handle_show_account(p_list)

        elif option == "3":
            handle_delete_account(p_list)
        elif option == "4":
            handle_quit()
        elif option == "5":
            print_accounts(p_list)
        elif option == "6":
            pass
        else:
            print("Invalid command...")
            print("Restarting...")
            sleep(1)


if __name__ == "__main__":
    main()
