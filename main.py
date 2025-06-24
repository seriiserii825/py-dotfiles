from classes.Dotfiles import Dotfiles

def mainFunc():
    df = Dotfiles()
    print("1) Linking dotfiles")
    print("2) Deleting links to dotfiles")
    choice = input("Choose an option (1 or 2): ").strip()
    if choice == "1":
        df.start()
        print("Dotfiles linked successfully.")
    elif choice == "2":
        df.deleteLinks()
        print("Links to dotfiles deleted successfully.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    mainFunc()
