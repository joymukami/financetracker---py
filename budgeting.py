import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox

class FinanceTracker:
    def __init__(self):
        self.budget_file = 'C:\\Users\\Joy Mukami\\Documents\\Personal Finance Tracker\\budgets.csv'
        self.ensure_directory_exists(os.path.dirname(self.budget_file))
        print(f"Initializing FinanceTracker with file: {self.budget_file}")

    def ensure_directory_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created missing directory: {path}")

    def set_budget(self, category, amount):
        print("Setting budget...")
        budgets = self.get_budgets()
        budgets[category] = amount
        print("Saving budget to CSV...")
        pd.DataFrame(list(budgets.items()), columns=['category', 'budget']).to_csv(self.budget_file, index=False)
        print("Budget saved.")

    def get_budgets(self):
        try:
            print("Reading budgets from CSV...")
            budgets_df = pd.read_csv(self.budget_file)
            if budgets_df.empty or 'category' not in budgets_df.columns or 'budget' not in budgets_df.columns:
                return {}
            return budgets_df.set_index('category').to_dict()['budget']
        except FileNotFoundError:
            print("budgets.csv not found.")
            return {}
        except pd.errors.EmptyDataError:
            print("budgets.csv is empty.")
            return {}

    def get_transactions(self):
        # Dummy data: In practice, this would retrieve actual transaction data
        data = {'category': ['food', 'entertainment', 'rent'], 'amount': [50, 100, 75]}
        return pd.DataFrame(data)

    def check_budget(self, category):
        print(f"Checking budget for {category}...")
        transactions = self.get_transactions()
        budgets = self.get_budgets()
        if (category in budgets) and (transactions['category'] == category).any():
            spent = transactions[transactions['category'] == category]['amount'].sum()
            if spent > budgets[category]:
                print(f"Warning: You have exceeded your budget for {category}!")
                return f"Warning: You have exceeded your budget for {category}!"
            else:
                print(f"You have ${budgets[category] - spent} left for {category}")
                return f"You have ${budgets[category] - spent} left for {category}"
        else:
            print(f"No budget found for {category}.")
            return f"No budget found for {category}."

# GUI Application
def set_budget():
    category = entry_category.get()
    amount = entry_amount.get()
    
    if not amount.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid amount.")
        return
    
    tracker.set_budget(category, int(amount))
    messagebox.showinfo("Success", f"Budget set for {category}: ${amount}")

def check_budget():
    category = entry_category.get()
    result = tracker.check_budget(category)
    messagebox.showinfo("Budget Status", result)

def display_transactions():
    transactions = tracker.get_transactions()
    listbox_transactions.delete(0, tk.END)
    for index, row in transactions.iterrows():
        listbox_transactions.insert(tk.END, f"{row['category']}: ${row['amount']}")

# Initialize tracker
tracker = FinanceTracker()

# GUI Setup
root = tk.Tk()
root.title("Finance Tracker")

tk.Label(root, text="Category").grid(row=0, column=0)
tk.Label(root, text="Amount").grid(row=1, column=0)

entry_category = tk.Entry(root)
entry_amount = tk.Entry(root)

entry_category.grid(row=0, column=1)
entry_amount.grid(row=1, column=1)

tk.Button(root, text='Set Budget', command=set_budget).grid(row=2, column=0, pady=4)
tk.Button(root, text='Check Budget', command=check_budget).grid(row=2, column=1, pady=4)

# Transaction Display
tk.Label(root, text="Transactions").grid(row=3, columnspan=2)
listbox_transactions = tk.Listbox(root, width=50)
listbox_transactions.grid(row=4, columnspan=2)

# Display existing transactions
display_transactions()

root.mainloop()
