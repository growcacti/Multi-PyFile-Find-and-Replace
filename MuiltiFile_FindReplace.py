import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import os

class FindReplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Find and Replace in Files')

        # GUI Components
        self.setup_gui()

    def setup_gui(self):
        # Select Directory Button
        select_button = tk.Button(self.root, text="Select Directory", command=self.select_directory)
        select_button.grid(row=0, column=0, padx=10, pady=10)

        # Directory Label
        self.directory_label = tk.Label(self.root, text="                                 ", fg="blue")
        self.directory_label.grid(row=1, column=0, padx=10)

        # List Box
        self.list_box = Listbox(self.root, width=80, height=40)
        self.list_box.grid(row=2, column=0, rowspan=3, columnspan=9, padx=10, pady=10)

        # Find and Replace Entries
        self.setup_find_replace_entries()

        # Buttons
        self.setup_buttons()
        tk.Label(self.root, text="Skip Lines:").grid(row=16, column=0, sticky='e', padx=10)
        self.skip_lines_spinbox = tk.Spinbox(self.root, from_=0, to=10, width=5)
        self.skip_lines_spinbox.grid(row=16, column=1, padx=10)
    def setup_find_replace_entries(self):
        tk.Label(self.root, text="Find:").grid(row=13, column=0, sticky='e', padx=10)
        self.find_entry = tk.Entry(self.root)
        self.find_entry.grid(row=13, column=1, padx=10)

        tk.Label(self.root, text="Replace With:").grid(row=14, column=0, sticky='e', padx=10)
        self.replace_entry = tk.Entry(self.root)
        self.replace_entry.grid(row=14, column=1, padx=10)

    def setup_buttons(self):
        find_button = tk.Button(self.root, text="Find", command=self.find_in_files)
        find_button.grid(row=15, column=0, padx=10, pady=10)

        replace_button = tk.Button(self.root, text="Replace", command=lambda: self.find_in_files(True))
        replace_button.grid(row=15, column=1, padx=10, pady=10)

        skiplines_button = tk.Button(self.root, text="Skip # line Replace", command=lambda: self.find_in_files(True, 3))
        skiplines_button.grid(row=16, column=1, padx=10, pady=10)
        skiplines_button = tk.Button(self.root, text="Skip # Line Replace", command=self.skip_line_replace)
        skiplines_button.grid(row=17, column=1, padx=10, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        self.directory_label.config(text=directory)


    def skip_line_replace(self):
        skip_lines = int(self.skip_lines_spinbox.get())
        self.find_in_files(True, skip_lines)

        

   
    def find_in_files(self, replace=False, skip_lines=0):
        directory = self.directory_label.cget("text")
        find_word = self.find_entry.get()
        replace_word = self.replace_entry.get() if replace else None

        self.list_box.delete(0, tk.END)  # Clear existing entries in the list box

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        try:
                            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                                content = f.read()
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred while processing {file_path}: {e}")
                            continue

                    count = content.count(find_word)
                    if count > 0:
                        if replace and replace_word:
                            content = content.replace(find_word, replace_word)
                            with open(file_path, 'w') as f:
                                f.write(content)
                            self.list_box.insert(tk.END, f"{file}: Replaced {count} occurrences")
                        else:
                            self.list_box.insert(tk.END, f"{file}: Found {count} occurrences")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FindReplaceApp(root)
    root.mainloop()
