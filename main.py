import argparse

from classes.Dotfiles import Dotfiles


def mainFunc():
    df = Dotfiles()

    parser = argparse.ArgumentParser(
        description="Manage dotfiles linking from HOME directory and .config"
    )
    parser.add_argument("-r", action="store_true", help="Remove dotfiles")
    args = parser.parse_args()

    if args.r:
        df.deleteLinks()
        print("Links to dotfiles deleted successfully.")
    else:
        df.start()
        print("Dotfiles linked successfully.")


if __name__ == "__main__":
    mainFunc()
