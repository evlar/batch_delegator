import os
import time
import csv
import bittensor as bt

# Function to print text in colored format
def color_text(text, text_color=37, background_color=40, bold=False):
    return f"\033[{';'.join([str(1 if bold else 0), str(text_color), str(background_color)])}m{text}\033[0m"

# Function for the raining banner effect
def raining_banner(lines, speed=0.2):
    os.system('cls' if os.name == 'nt' else 'clear')
    for line in lines:
        colored_line = ""
        for char in line:
            if char == '+':
                colored_line += color_text(char, text_color=33, background_color=40)
            elif char == '.':
                colored_line += color_text(char, text_color=34, background_color=40)
            elif char in "BATCH DELEGATOR":
                colored_line += color_text(char, text_color=32, background_color=40, bold=True)
            else:
                colored_line += char
        print(colored_line)
        time.sleep(speed)
    time.sleep(1)  # Pause before clearing the screen

# Your custom ASCII Banner for "BATCH DELEGATOR"
banner_lines = [
    "++++++++++++++++++++++++++++++++++++++++++++++",
    "+  .    .    .    .    .    .    .    .    . +",
    "+  .    .    .  BATCH DELEGATOR  .    .    . +",
    "+  .    .    .    .    .    .    .    .    . +",
    "++++++++++++++++++++++++++++++++++++++++++++++"
]

raining_banner(banner_lines)

# Reading data from a CSV file
csv_file_path = 'validator_hotkeys.csv'  # Update this to your CSV file path
addresses = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        name = row['Name'].strip()
        address = row['Address'].strip()

        if not all([name, address]):
            continue

        addresses.append({'Name': name, 'Address': address})

# Display all addresses and ask for selection
print("Available Addresses:")
for i, entry in enumerate(addresses, 1):
    print(f"{i}. {color_text(entry['Name'], text_color=33)} ({entry['Address']})")

print(color_text("Enter the numbers of the addresses you want to process, separated by commas (e.g., 1,3,5): ", text_color=32, background_color=40), end="")
selected_indices = input()
selected_indices = [int(i) for i in selected_indices.split(',') if i.isdigit()]

# Initialize subtensor connection
config = bt.subtensor.config()
network = 'finney'
chain_endpoint = None

try:
    sub = bt.subtensor(config=config, network=network)
except Exception as e:
    print(f"Failed to connect to the Subtensor: {e}")
    exit(1)

# Initialize your sending wallet
wallet_name = input("Enter your wallet name: ").strip()
try:
    MY_WALLET = bt.wallet(name=wallet_name)
except Exception as e:
    print(f"Failed to initialize wallet '{wallet_name}': {e}")
    exit(1)

# Prepare transactions
transactions = []
wait_time_after_undelegation = 20  # 20 seconds wait time after undelegation

for index in selected_indices:
    if index > len(addresses):
        print(f"Invalid selection: {index}")
        continue

    entry = addresses[index - 1]

    while True:
        action = input(f"Enter {color_text('delegate', text_color=32, background_color=40)} or {color_text('undelegate', text_color=31, background_color=40)} for {color_text(entry['Name'], text_color=33, background_color=40)}: ").strip().lower()
        
        if action == 'delegate':
            colored_action = color_text(action, text_color=32, background_color=40)  # Green for 'delegate'
            break
        elif action == 'undelegate':
            colored_action = color_text(action, text_color=31, background_color=40)  # Red for 'undelegate'
            break
        print("Invalid input. Please enter either 'delegate' or 'undelegate'.")

    amount_str = input(f'Enter the amount to {colored_action} (or type "all" for all available tokens): ').strip()
    amount = None if amount_str.lower() == 'all' else float(amount_str)

    transactions.append((action, entry, amount))

# Confirm Transactions
print("\nPlanned Transactions:")
for i, (action, entry, amount) in enumerate(transactions, 1):
    colored_action = color_text(action, text_color=32 if action == 'delegate' else 31, background_color=40)
    print(f"{i}. {colored_action} to {entry['Name']} ({entry['Address']}) with amount {'all' if amount is None else amount}")

confirmation = input("\nDo you want to proceed with these transactions? (yes/no): ").strip().lower()
if confirmation != 'yes':
    print("Transactions canceled.")
    exit(0)

# Execute Transactions
for action, entry, amount in transactions:
    try:
        if action == 'delegate':
            success = sub.delegate(wallet=MY_WALLET, delegate_ss58=entry['Address'], amount=amount, wait_for_inclusion=True, wait_for_finalization=False, prompt=True)
        elif action == 'undelegate':
            success = sub.undelegate(wallet=MY_WALLET, delegate_ss58=entry['Address'], amount=amount, wait_for_inclusion=True, wait_for_finalization=False, prompt=True)

            if success and amount is not None:
                print(f"Waiting {wait_time_after_undelegation} seconds for undelegation to complete...")
                time.sleep(wait_time_after_undelegation)

        if success:
            colored_action = color_text(action, text_color=32 if action == 'delegate' else 31, background_color=40)
            print(f"Successfully processed {colored_action} for {entry['Name']} ({entry['Address']})")
        else:
            print(f"Failed to process {action} for {entry['Name']} ({entry['Address']})")
    except Exception as e:
        print(f"An error occurred while processing {action} for {entry['Name']} ({entry['Address']}): {e}")

# Final message
print("\n" + color_text("Thank you for using BATCH DELEGATOR!\nDonations gratefully received to ", text_color=33, background_color=40) +
      color_text("5C5a4aGX8zfApCRY2W3Cs9MBwmBjpMDZhVqemzy1rbg632Uo", text_color=32, background_color=40, bold=True))

