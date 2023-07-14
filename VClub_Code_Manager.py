import tkinter as tk
from tkinter import messagebox, font
import sqlite3
from datetime import datetime


conn = sqlite3.connect('function_manager.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tags TEXT,
                comments TEXT,
                arguments TEXT,
                return_type TEXT,
                code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
             )''')
conn.commit()

window = tk.Tk()
window.title("V-Club | Code Manager")
window.iconbitmap(r"C:\Users\K VIVEK KUMAR\OneDrive\Desktop\T-Run\VClub.ico")

input_font = font.Font(family="Arial", size=12)

def add_function():
    tags = entry_tags.get()
    comments = entry_comments.get()
    arguments = entry_arguments.get()
    return_type = entry_return_type.get()
    code = entry_code.get("1.0", tk.END)

    if tags and comments and arguments and return_type and code:
        c.execute("INSERT INTO functions (tags, comments, arguments, return_type, code) VALUES (?, ?, ?, ?, ?)",
                  (tags, comments, arguments, return_type, code))
        conn.commit()
        messagebox.showinfo("Success", "Function added successfully!")
        clear_entries()
        search_functions()
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

def search_functions():
    listbox.delete(0, tk.END)
    search_query = entry_search.get()

    c.execute("SELECT id, comments, arguments, return_type FROM functions WHERE tags LIKE ? OR comments LIKE ?",
              ('%{}%'.format(search_query), '%{}%'.format(search_query)))
    functions = c.fetchall()

    for function in functions:
        function_id = function[0]
        comments = function[1]
        arguments = function[2]
        return_type = function[3]
        listbox.insert(tk.END, f"ID: {function_id}\nComments: {comments}\nArguments: {arguments}\nReturn Type: {return_type}\n{'-' * 50}")

def open_function():
    selected_index = listbox.curselection()

    if selected_index:
        function_id = listbox.get(selected_index).split('\n')[0].split(': ')[1]
        selected_function = c.execute("SELECT tags, comments, arguments, return_type, code FROM functions WHERE id=?", (function_id,)).fetchone()

        if selected_function:
            tags = selected_function[0]
            comments = selected_function[1]
            arguments = selected_function[2]
            return_type = selected_function[3]
            code = selected_function[4]

            edit_window = tk.Toplevel()
            edit_window.title(comments)

            label_tags = tk.Label(edit_window, text="Tags:")
            entry_tags = tk.Entry(edit_window, font=input_font)
            entry_tags.insert(tk.END, tags)

            label_comments = tk.Label(edit_window, text="Comments:")
            entry_comments = tk.Entry(edit_window, font=input_font)
            entry_comments.insert(tk.END, comments)

            label_arguments = tk.Label(edit_window, text="Arguments:")
            entry_arguments = tk.Entry(edit_window, font=input_font)
            entry_arguments.insert(tk.END, arguments)

            label_return_type = tk.Label(edit_window, text="Return Type:")
            entry_return_type = tk.Entry(edit_window, font=input_font)
            entry_return_type.insert(tk.END, return_type)

            label_code = tk.Label(edit_window, text="Code:")
            entry_code = tk.Text(edit_window, height=10, width=50, font=input_font)
            entry_code.insert(tk.END, code)

            def save_changes():
                tags = entry_tags.get()
                comments = entry_comments.get()
                arguments = entry_arguments.get()
                return_type = entry_return_type.get()
                code = entry_code.get("1.0", tk.END)

                if tags and comments and arguments and return_type and code:
                    c.execute("UPDATE functions SET tags=?, comments=?, arguments=?, return_type=?, code=?, modified_at=? WHERE id=?",
                              (tags, comments, arguments, return_type, code, datetime.now(), function_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Function modified successfully!")
                    edit_window.destroy()
                    search_functions()
                else:
                    messagebox.showerror("Error", "Please fill in all the fields.")

            def delete_function():
                result = messagebox.askyesno("Confirmation", "Are you sure you want to delete this function?")

                if result == tk.YES:
                    c.execute("DELETE FROM functions WHERE id=?", (function_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Function deleted successfully!")
                    edit_window.destroy()
                    search_functions()

            btn_save = tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#4287f5", fg="white")
            btn_delete = tk.Button(edit_window, text="Delete Function", command=delete_function, bg="#f54242", fg="white")

            label_tags.pack()
            entry_tags.pack()
            label_comments.pack()
            entry_comments.pack()
            label_arguments.pack()
            entry_arguments.pack()
            label_return_type.pack()
            entry_return_type.pack()
            label_code.pack()
            entry_code.pack()
            btn_save.pack()
            btn_delete.pack()

        else:
            messagebox.showerror("Error", "Function not found.")

    else:
        messagebox.showerror("Error", "Please select a function to modify.")

def clear_entries():
    entry_tags.delete(0, tk.END)
    entry_comments.delete(0, tk.END)
    entry_arguments.delete(0, tk.END)
    entry_return_type.delete(0, tk.END)
    entry_code.delete("1.0", tk.END)

label_tags = tk.Label(window, text="Tags:")
entry_tags = tk.Entry(window, font=input_font)

label_comments = tk.Label(window, text="Comments:")
entry_comments = tk.Entry(window, font=input_font)

label_arguments = tk.Label(window, text="Arguments:")
entry_arguments = tk.Entry(window, font=input_font)

label_return_type = tk.Label(window, text="Return Type:")
entry_return_type = tk.Entry(window, font=input_font)

label_code = tk.Label(window, text="Code:")
entry_code = tk.Text(window, height=10, width=50, font=input_font)

btn_add = tk.Button(window, text="Add Function", command=add_function, bg="#34c924", fg="white")
btn_search = tk.Button(window, text="Search", command=search_functions, bg="#4287f5", fg="white")
btn_modify = tk.Button(window, text="Modify Function", command=open_function, bg="#f5a742", fg="white")

listbox = tk.Listbox(window, width=60)
scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)

label_search = tk.Label(window, text="Search:")
entry_search = tk.Entry(window)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=4)
window.grid_columnconfigure(2, weight=2)
window.grid_rowconfigure(1, weight=1)

label_tags.grid(row=0, column=0, sticky="e")
entry_tags.grid(row=0, column=1, padx=10, pady=5, sticky="we")

label_comments.grid(row=1, column=0, sticky="e")
entry_comments.grid(row=1, column=1, padx=10, pady=5, sticky="we")

label_arguments.grid(row=2, column=0, sticky="e")
entry_arguments.grid(row=2, column=1, padx=10, pady=5, sticky="we")

label_return_type.grid(row=3, column=0, sticky="e")
entry_return_type.grid(row=3, column=1, padx=10, pady=5, sticky="we")

label_code.grid(row=4, column=0, sticky="ne")
entry_code.grid(row=4, column=1, padx=10, pady=5, sticky="we")

btn_add.grid(row=5, column=0, columnspan=2, pady=10)

listbox.grid(row=0, column=2, rowspan=6, padx=10, pady=10, sticky="ns")
scrollbar.grid(row=0, column=3, rowspan=6, sticky="ns")

label_search.grid(row=6, column=0, sticky="e")
entry_search.grid(row=6, column=1, padx=10, pady=5, sticky="we")

btn_search.grid(row=6, column=2, padx=5, pady=5)
btn_modify.grid(row=7, column=2, padx=5, pady=5)

window.mainloop()
