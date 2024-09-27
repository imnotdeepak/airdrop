import os
from typing import List, Tuple

from secure_drop import commands, utils
from secure_drop.singletons.NetworkManager import NetworkManager


class REPL:
    """Encapsulates SecureDrop's main REPL and its helper functions.
    """

    def run(self):
        """Runs the REPL.
        """

        NetworkManager().start()
        self.__print_help_command_prompt()
        while True:
            command, args = self.__get_command_and_args()
            self.__execute(command, args)

    @staticmethod
    def __print_help_command_prompt():
        print("Type \"help\" for commands.")

    @staticmethod
    def __get_command_and_args() -> Tuple[str, List[str]]:
        """Retrieves the user's desired command and arguments, if any.

        Returns:
            Tuple[str, List[str]]: A tuple in which the first element represents the user's desired 
                command and the second represents the user's arguments.
        """

        user_input = input("secure_drop> ").lower().split()
        if len(user_input) == 0:
            return "", []
        elif len(user_input) == 1:
            return user_input[0], []
        else:
            return user_input[0], user_input[1:]

    def __execute(self, command: str, args: List[str]):
        """Executes a given command obtained from the REPL.

        Args:
            command (str): The command to execute.
        """

        if command == "help":
            commands.help()
        elif command == "add":
            commands.add_contact()
        elif command == "list":
            commands.list_contacts()
        elif command == "send":
            if len(args) != 2:
                print("Usage: send <contact-email> <file>")
                return
            email, file_path = args
            arguments_valid = True
            if not utils.is_valid_email(email):
                print("Please enter a valid email address.")
                arguments_valid = False
            if not os.path.isfile(file_path):
                print(f"Unable to find specified file: {file_path}")
                arguments_valid = False
            if not arguments_valid:
                return
            commands.send_file(email, file_path)
        elif command in ["y", "n"] and NetworkManager().is_waiting_for_send_file_consent():
            if command == "y":
                NetworkManager().consent_to_receive_file()
                print("Receiving file...")
            else:
                NetworkManager().reject_receiving_file()
                print("Rejected file.")
        elif command == "exit":
            exit_app()
        else:
            print(f"Received unrecognized command: {command}")
            self.__print_help_command_prompt()


def exit_app():
    """Exits the SecureDrop application and informs the user.
    """

    print("Stopping all network resources...")
    NetworkManager().stop()
    print("Network resources stopped.")
    print("Exiting SecureDrop.")
    exit(0)
