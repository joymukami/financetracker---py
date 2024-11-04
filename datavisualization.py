import os
import pandas as pd
import matplotlib.pyplot as plt
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
        data = {'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
                'category': ['food', 'entertainment', 'food'],
                'amount': [50, 100, 75],
                'type': ['expense', 'expense', 'expense']}
        return pd.DataFrame(data)

    def check_budget(self, category):
        print(f"Checking budget for {category}...")
        transactions = self.get_transactions()
        budgets = self.get_budgets()
        if category in budgets:
            spent = transactions[transactions['category'] == category]['amount'].sum()
            if spent > budgets[category]:
                messagebox.showwarning("Warning", f"You have exceeded your budget for {category}!")
            else:
                messagebox.showinfo("Budget", f"You have ${budgets[category] - spent} left for {category}")
        else:
            messagebox.showerror("Error", f"No budget set for {category}.")

    def plot_expenses_by_category(self):
        transactions = self.get_transactions()
        expenses = transactions[transactions['type'] == 'expense']
        expenses.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.show()

    def plot_income_vs_expenses(self):
        transactions = self.get_transactions()
        transactions['date'] = pd.to_datetime(transactions['date'])
        transactions.set_index('date', inplace=True)
        transactions.groupby('type')['amount'].resample('M').sum().unstack().plot(kind='bar')

        plt.title('Income vs. Expenses Over Time')
        plt.show()


# Initialize FinanceTracker instance
tracker = FinanceTracker()

# GUI functions
def set_budget_gui():
    category = entry_category.get()
    try:
        amount = float(entry_amount.get())
        tracker.set_budget(category, amount)
        messagebox.showinfo("Success", f"Budget set for {category}: {amount}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def check_budget_gui():
    category = entry_category.get()
    tracker.check_budget(category)

def plot_expenses_gui():
    tracker.plot_expenses_by_category()

def plot_income_vs_expenses_gui():
    tracker.plot_income_vs_expenses()


# Create the GUI window
root = tk.Tk()
root.title("Finance Tracker")

# Layout for the GUI
tk.Label(root, text="Category").grid(row=0)
tk.Label(root, text="Amount").grid(row=1)
entry_category = tk.Entry(root)
entry_amount = tk.Entry(root)
entry_category.grid(row=0, column=1)
entry_amount.grid(row=1, column=1)

tk.Button(root, text='Set Budget', command=set_budget_gui).grid(row=2, column=1, pady=4)
tk.Button(root, text='Check Budget', command=check_budget_gui).grid(row=3, column=1, pady=4)
tk.Button(root, text='Plot Expenses by Category', command=plot_expenses_gui).grid(row=4, column=1, pady=4)
tk.Button(root, text='Plot Income vs. Expenses', command=plot_income_vs_expenses_gui).grid(row=5, column=1, pady=4)

root.mainloop()
