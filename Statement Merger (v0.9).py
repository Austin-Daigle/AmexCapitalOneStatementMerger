# version 0.9 (ux stable, minimal functionality)
import csv
import tkinter as tk
from tkinter import filedialog, ttk


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, justify="left", background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, _):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class CSVFileProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Processor")
        self.root.geometry("600x140")  # Modified dimensions
        self.root.resizable(False, False)

        # File 1 components
        self.label1 = tk.Label(root, text="File 1:")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.file_path_var1 = tk.StringVar()
        self.file_path_entry1 = tk.Entry(root, textvariable=self.file_path_var1, width=50, state="disabled")
        self.file_path_entry1.grid(row=0, column=1, padx=5, pady=5)
        ToolTip(self.file_path_entry1, "<No File Choosen>")

        self.browse_button1 = tk.Button(root, text="Browse", command=lambda: self.browse_file(1))
        self.browse_button1.grid(row=0, column=2, padx=5, pady=5)

        self.clear_button1 = tk.Button(root, text="Clear Selection", command=lambda: self.clear_selection(1))
        self.clear_button1.grid(row=0, column=3, padx=5, pady=5)

        # File 2 components
        self.label2 = tk.Label(root, text="File 2:")
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.file_path_var2 = tk.StringVar()
        self.file_path_entry2 = tk.Entry(root, textvariable=self.file_path_var2, width=50, state="disabled")
        self.file_path_entry2.grid(row=1, column=1, padx=5, pady=5)
        ToolTip(self.file_path_entry2, "<No File Choosen>")

        self.browse_button2 = tk.Button(root, text="Browse", command=lambda: self.browse_file(2))
        self.browse_button2.grid(row=1, column=2, padx=5, pady=5)

        self.clear_button2 = tk.Button(root, text="Clear Selection", command=lambda: self.clear_selection(2))
        self.clear_button2.grid(row=1, column=3, padx=5, pady=5)

        # Process button
        self.process_button = tk.Button(root, text="Process", command=self.process_files, state="disabled")
        self.process_button.grid(row=2, column=0, columnspan=4, pady=10)

    def browse_file(self, file_num):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            if file_num == 1:
                self.file_path_var1.set(file_path)
                #update the tool text for entry 1
                ToolTip(self.file_path_entry1, self.file_path_var1.get())
            elif file_num == 2:
                self.file_path_var2.set(file_path)
                #update the tool text for entry 2
                ToolTip(self.file_path_entry2, self.file_path_var2.get())

            self.check_process_button_state()

    def clear_selection(self, file_num):
        if file_num == 1:
            self.file_path_var1.set("")
            #update the tool text for entry 1
            ToolTip(self.file_path_entry1, "<No File Choosen>")
        elif file_num == 2:
            self.file_path_var2.set("")
            #update the tool text for entry 2
            ToolTip(self.file_path_entry2, "<No File Choosen>")

        self.check_process_button_state()

    def check_process_button_state(self):
        if self.file_path_var1.get() and self.file_path_var2.get():
            self.process_button["state"] = "normal"
        else:
            self.process_button["state"] = "disabled"

    def process_files(self):
        file_path1 = self.file_path_var1.get()
        file_path2 = self.file_path_var2.get()

        with open(file_path1, newline='') as file1, open(file_path2, newline='') as file2:
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)

            print("Contents of File 1:")
            for row in reader1:
                print(row)

            print("\nContents of File 2:")
            for row in reader2:
                print(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVFileProcessor(root)
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    root.mainloop()
