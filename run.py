import input_n
import input_p

# Main function to select state
def main():
    print("Please select one of the following states:")
    print("1: n-channel")
    print("2: p-channel")

    try:
        selection = int(input("Your choice: "))
        
        if selection == 1:
            input_n.select_state()
        elif selection == 2:
            input_p.select_state()
        else:
            print("Invalid selection. Please choose 1 or 2.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Call the main function to execute
if __name__ == "__main__":
    main()
