# Set inventory to 0 in the start
inventory = 0
entries = 0
rejected_entries = 0
transaction_history = []

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
def generate_report(total_units, failed_attempts, history):
    print("\n--- Final Summary --- ")
    print("Total Units Processed:", total_units)
    print("Transaction History:")

    orders = {}

    for order_id, quantity in history:
        if order_id not in orders:
            orders[order_id] = []

        orders[order_id].append(quantity)

    for order_id, quantities in orders.items():
        print(f"ID: {order_id}, " + ", ".join(str(quantity) for quantity in quantities))

    print("Number of Failed/Rejected Entries:", failed_attempts)

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            total_line = file.readline().strip()

            if total_line:
                total_file = int(total_line)
            else:
                total_file = 0

            history = []

            for line in file:
                line = line.strip()

                if line:
                    order_id, quantity = line.split(",")
                    history.append((int(order_id), int(quantity)))

            return  total_file, history

    except FileNotFoundError:
        # inventory = 0, transaction_history is a list
        return 0, []

def save_inventory(total_units, history):
    with open("inventory.txt", "w") as file:
        # Converts [100, 100, 200] into 100,100,200 for inventory.txt
        file.write(str(total_units) + "\n")

        # Save each order
        for order_id, quantity in history:
            file.write(f"{order_id}, {quantity}\n")

inventory, transaction_history = load_inventory()

if transaction_history:
    current_order_id = transaction_history[-1][0] + 1
else:
    current_order_id = 1

order_added = False

while True:
    # Get input from user
    user_input = get_valid_input()

    # Stop program if user enters "exit"
    if user_input == "exit":
        save_inventory(inventory, transaction_history)
        generate_report(inventory, rejected_entries, transaction_history)
        print("\nInventory successfully saved to inventory.txt")
        break

    # Process the delivery
    inventory = process_delivery(inventory, user_input)

    # Store the transaction in history
    transaction_history.append((current_order_id,user_input))

    order_added = True

    print(f"\nNew Order Added: {user_input}")

    # Save immediately after every transaction
    save_inventory(inventory, transaction_history)

    # Calcuating the tax
    tax = calculate_tax(user_input)

    # Count valid delivery other than "exit"
    entries += 1

    print("Inventory updated. Current stock:", inventory)
    print(f"Tax for this delivery: ${tax}")
    print("Number of entries:", entries)
    print("Number of Failed/Rejected Entries:", rejected_entries)
    print("\nCurrent Orders:")

    orders = {}

    for order_id, quantity in transaction_history:
        if order_id not in orders:
            orders[order_id] = []
        
        orders[order_id].append(quantity)
    
    for order_id, quantities in orders.items():
        print(f"ID: {order_id}, " + ", ".join(str(quantity) for quantity in quantities))

