from secure_drop import input_helpers, utils
from secure_drop.registration import register_user
from secure_drop.REPL import REPL, exit_app
from secure_drop.singletons.LoginManager import LoginManager


def main():
    """SecureDrop's entry point.
    """

    try:
        if utils.user_registered(): # Log the user in and run SecureDrop
            login_manager = LoginManager()
            while not login_manager.logged_in():
                email, password = input_helpers.get_email_and_password_for_login()
                login_manager.login_user(email, password)
                if login_manager.max_login_attempts_exceeded():
                    exit_app()
            print("Welcome to SecureDrop!")
            repl = REPL()
            repl.run()
        else: # Register the user
            print("No users are registered with this client.")
            user_choice = ""
            while user_choice not in ["n", "y"]:
                user_choice = input("Do you want to register a new user? (y/n)? ").lower()
            if user_choice == "y":
                credentials = input_helpers.get_credentials_for_registration()
                register_user(credentials)
                print("User registered.")
            exit_app()

    except KeyboardInterrupt:
        print()
        exit_app()


if __name__ == "__main__":
    main()
