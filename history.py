import tkinter as tk
from tkinter import messagebox
import pandas as pd





# Define the FinanceTracker class
class FinanceTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, date, t_type, category, amount, description):
        self.transactions.append({
            'date': date,
            'type': t_type,
            'category': category,
            'amount': amount,
            'description': description
        })

    def get_transactions(self):
        return pd.DataFrame(self.transactions)

# Initialize the tracker instance
tracker = FinanceTracker()

def add_transaction():
    date = entry_date.get()
    t_type = entry_type.get()
    category = entry_category.get()
    amount = entry_amount.get()
    description = entry_description.get()
    tracker.add_transaction(date, t_type, category, amount, description)
    messagebox.showinfo("Success", "Transaction added successfully")
    display_transactions()

def display_transactions():
    transactions = tracker.get_transactions()
    listbox_transactions.delete(0, tk.END)
    for index, row in transactions.iterrows():
        listbox_transactions.insert(tk.END, f"{row['date']} - {row['type']} - {row['category']} - ${row['amount']} - {row['description']}")

root = tk.Tk()
root.title("Finance Tracker")

tk.Label(root, text="Date").grid(row=0)
tk.Label(root, text="Type").grid(row=1)
tk.Label(root, text="Category").grid(row=2)
tk.Label(root, text="Amount").grid(row=3)
tk.Label(root, text="Description").grid(row=4)

entry_date = tk.Entry(root)
entry_type = tk.Entry(root)
entry_category = tk.Entry(root)
entry_amount = tk.Entry(root)
entry_description = tk.Entry(root)

entry_date.grid(row=0, column=1)
entry_type.grid(row=1, column=1)
entry_category.grid(row=2, column=1)
entry_amount.grid(row=3, column=1)
entry_description.grid(row=4, column=1)

tk.Button(root, text='Add', command=add_transaction).grid(row=5, column=1, pady=4)

listbox_transactions = tk.Listbox(root, width=50)
listbox_transactions.grid(row=6, columnspan=2)

display_transactions()

root.mainloop()



