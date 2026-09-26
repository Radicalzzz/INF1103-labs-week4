# Set inventory to 0 in the start
inventory = 0
entries = 0
rejected_entries = 0

# Function of user input. Handles prompt, input validation and return a valid integer.
def get_valid_input():
    global rejected_entries # global variable to call the variable outside of the function
    while True:
        user_input = input("\nPlease enter the number of items to add to inventory or type 'exit' to quit: ")
        if user_input.lower() == "exit":
            return "exit"

        if user_input.startswith('-') and user_input[1:].replace('.', '').isdigit():
            print("Invalid input. Please enter a non-negative integer or type 'exit' to exit.")
            rejected_entries += 1
            continue

        if not user_input.isdigit():
            print("Invalid input. Please enter an integer number or type 'exit' to quit.")
            rejected_entries += 1
            continue

        return int(user_input)

# Function to add units to inventory
def process_delivery(current_total, new_value):
    current_total = current_total + new_value
    return current_total

# Function to take the delivery amount and tax
def calculate_tax(amount):
    amount = amount * 0.1
    return amount

# Function to print final summary
def generate_report(total_units, failed_attempts):
    print("\n--- Final Summary --- ")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

while True:
    # Get input from user
    user_input = get_valid_input()

    # Stop program if user enters "exit"
    if user_input == "exit":
        generate_report(inventory, rejected_entries)
        break

    # Process the delivery
    inventory = process_delivery(inventory, user_input)

    # Calcuating the tax
    tax = calculate_tax(user_input)

    # Count valid delivery other than "exit"
    entries += 1

    print("Inventory updated. Current stock:", inventory)
    print(f"Tax for this delivery: ${tax}")
    print("Number of entries:", entries)
    print("Number of Failed/Rejected Entries:", rejected_entries)

    if inventory > 500:
        print("Inventory exceeds 500 units.")
        generate_report(inventory, rejected_entries)
        break