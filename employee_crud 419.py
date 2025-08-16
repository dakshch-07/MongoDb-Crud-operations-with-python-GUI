import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["employees_db"]
collection = db["employees"]

# Functions
def insert_employee():
    emp_id = entry_id.get()
    name = entry_name.get()
    position = entry_position.get()
    salary = entry_salary.get()

    if emp_id and name and position and salary:
        try:
            emp_id = int(emp_id)
            salary = float(salary)
            collection.insert_one({
                "emp_id": emp_id,
                "name": name,
                "position": position,
                "salary": salary
            })
            messagebox.showinfo("✅ Success", "Employee added successfully!")
            show_employees()
        except ValueError:
            messagebox.showerror("❌ Error", "ID must be integer and Salary must be a number.")
    else:
        messagebox.showwarning("⚠ Warning", "Please fill all fields.")

def update_employee():
    emp_id = entry_id.get()
    if emp_id:
        new_salary = entry_salary.get()
        if new_salary:
            try:
                new_salary = float(new_salary)
                result = collection.update_one({"emp_id": int(emp_id)}, {"$set": {"salary": new_salary}})
                if result.modified_count > 0:
                    messagebox.showinfo("✅ Success", "Salary updated successfully!")
                    show_employees()
                else:
                    messagebox.showwarning("⚠ Warning", "No record found.")
            except ValueError:
                messagebox.showerror("❌ Error", "Salary must be a number.")
        else:
            messagebox.showwarning("⚠ Warning", "Enter new salary.")
    else:
        messagebox.showwarning("⚠ Warning", "Enter Employee ID.")

def delete_employee():
    emp_id = entry_id.get()
    if emp_id:
        result = collection.delete_one({"emp_id": int(emp_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("✅ Success", "Employee deleted successfully!")
            show_employees()
        else:
            messagebox.showwarning("⚠ Warning", "No record found.")
    else:
        messagebox.showwarning("⚠ Warning", "Enter Employee ID to delete.")

def show_employees():
    for row in tree.get_children():
        tree.delete(row)
    for i, emp in enumerate(collection.find()):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=(emp["emp_id"], emp["name"], emp["position"], emp["salary"]), tags=(tag,))

# GUI Setup
root = tk.Tk()
root.title("Employee Management - MongoDB CRUD")
root.geometry("850x600")
root.configure(bg="#E3F2FD")  # Light blue background

# Style
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#1565C0", foreground="white")
style.configure("Treeview", font=("Arial", 11), rowheight=25)
style.map("Treeview", background=[("selected", "#1E90FF")])

# Row colors
tree_tags = {
    "evenrow": {"background": "#BBDEFB"},
    "oddrow": {"background": "#E3F2FD"}
}

# Input Frame
frame_input = tk.Frame(root, bg="#E3F2FD")
frame_input.pack(pady=10)

labels = ["Employee ID", "Name", "Position", "Salary"]
entries = []
for i, label in enumerate(labels):
    tk.Label(frame_input, text=label, font=("Arial", 11, "bold"), bg="#E3F2FD").grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = tk.Entry(frame_input, font=("Arial", 11), width=25)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

entry_id, entry_name, entry_position, entry_salary = entries

# Buttons Frame
frame_buttons = tk.Frame(root, bg="#E3F2FD")
frame_buttons.pack(pady=10)

# Custom colored buttons
btn_insert = tk.Button(frame_buttons, text="Insert", command=insert_employee, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=10)
btn_update = tk.Button(frame_buttons, text="Update", command=update_employee, font=("Arial", 11, "bold"), bg="#FF9800", fg="white", width=10)
btn_delete = tk.Button(frame_buttons, text="Delete", command=delete_employee, font=("Arial", 11, "bold"), bg="#F44336", fg="white", width=10)
btn_show   = tk.Button(frame_buttons, text="Show", command=show_employees, font=("Arial", 11, "bold"), bg="#2196F3", fg="white", width=10)

btn_insert.grid(row=0, column=0, padx=10, pady=5)
btn_update.grid(row=0, column=1, padx=10, pady=5)
btn_delete.grid(row=0, column=2, padx=10, pady=5)
btn_show.grid(row=0, column=3, padx=10, pady=5)

# Table
columns = ("ID", "Name", "Position", "Salary")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=180)

for tag, cfg in tree_tags.items():
    tree.tag_configure(tag, background=cfg["background"])

tree.pack(pady=10)

root.mainloop()
