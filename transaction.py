import csv
import os



class FinanceTracker:
    def __init__(self, file_name='transactions.csv'):
        # Sets up file in user's home directory
        self.file_name = os.path.join(os.path.expanduser("~"), file_name)
        print(f"Initializing FinanceTracker with file: {self.file_name}")
        
        # Create the file with headers if it doesn't exist
        if not os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['date', 'type', 'category', 'amount', 'description'])
                print("File created with headers.")
            except OSError as e:
                print(f"Error creating file: {e}")

    def add_transaction(self, date, t_type, category, amount, description):
        try:
            print(f"Adding transaction to file: {self.file_name}")
            with open(self.file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, t_type, category, amount, description])
            print(f"Transaction added: {date}, {t_type}, {category}, {amount}, {description}")
        except OSError as e:
            print(f"Error writing to file: {e}")

    def get_transactions(self):
        transactions = []
        try:
            with open(self.file_name, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append({
                        'date': row['date'],
                        'type': row['type'],
                        'category': row['category'],
                        'amount': row['amount'],
                        'description': row['description']
                    })
            print("Transactions read successfully.")
        except OSError as e:
            print(f"Error reading file: {e}")
        return transactions


# Example usage of the FinanceTracker class
tracker = FinanceTracker(file_name='transactions_local.csv')  # Use a new file name for this instance
tracker.add_transaction('2024-07-22', 'income', 'expense', 5000, 'Monthly salary')
print(tracker.get_transactions())
