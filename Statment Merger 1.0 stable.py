import csv
import datetime
import tkinter as tk
from tkinter import filedialog, ttk

import openpyxl

# Stable 1.0

class CSVDataViewer(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("CSV Data Viewer")
        self.geometry("600x400")

        self.data = data

        # Find non-empty columns
        columns = [col for col in data[0] if col.strip()] if data else []

        self.table = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.table.heading(col, text=col)
        self.table.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=self.scrollbar.set)

        for row in data[1:]:
            self.table.insert("", "end", values=row)

        self.save_button = ttk.Button(self, text="Save as", command=self.save_as)
        self.save_button.grid(row=1, column=0, pady=10)

        self.close_button = ttk.Button(self, text="Close program", command=self.destroy)
        self.close_button.grid(row=2, column=0, pady=10)

    def save_as(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("Excel files", "*.xlsx")], defaultextension=".xlsx")
        if file_path:
            wb = openpyxl.Workbook()
            ws = wb.active
            for row in self.data:
                ws.append(row)
            wb.save(file_path)


class CSVFileProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Processor")
        self.root.geometry("600x140")
        self.root.resizable(False, False)

        self.label1 = tk.Label(root, text="File 1:")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.file_path_var1 = tk.StringVar()
        self.file_path_entry1 = tk.Entry(root, textvariable=self.file_path_var1, width=50, state="disabled")
        self.file_path_entry1.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button1 = tk.Button(root, text="Browse", command=lambda: self.browse_file(1))
        self.browse_button1.grid(row=0, column=2, padx=5, pady=5)

        self.clear_button1 = tk.Button(root, text="Clear Selection", command=lambda: self.clear_selection(1))
        self.clear_button1.grid(row=0, column=3, padx=5, pady=5)

        self.label2 = tk.Label(root, text="File 2:")
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.file_path_var2 = tk.StringVar()
        self.file_path_entry2 = tk.Entry(root, textvariable=self.file_path_var2, width=50, state="disabled")
        self.file_path_entry2.grid(row=1, column=1, padx=5, pady=5)

        self.browse_button2 = tk.Button(root, text="Browse", command=lambda: self.browse_file(2))
        self.browse_button2.grid(row=1, column=2, padx=5, pady=5)

        self.clear_button2 = tk.Button(root, text="Clear Selection", command=lambda: self.clear_selection(2))
        self.clear_button2.grid(row=1, column=3, padx=5, pady=5)

        self.process_button = tk.Button(root, text="Process", command=self.process_files, state="disabled")
        self.process_button.grid(row=2, column=0, columnspan=4, pady=10)

    def browse_file(self, file_num):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            if file_num == 1:
                self.file_path_var1.set(file_path)
            elif file_num == 2:
                self.file_path_var2.set(file_path)

            self.check_process_button_state()

    def clear_selection(self, file_num):
        if file_num == 1:
            self.file_path_var1.set("")
        elif file_num == 2:
            self.file_path_var2.set("")

        self.check_process_button_state()

    def check_process_button_state(self):
        if self.file_path_var1.get() and self.file_path_var2.get():
            self.process_button["state"] = "normal"
        else:
            self.process_button["state"] = "disabled"

    def process_files(self):
        def process_amex(file_data):
            result = []
            for row in file_data[1:]:
                date = datetime.datetime.strptime(row[0], '%m/%d/%Y').date().strftime('%m/%d/%Y')
                result.append([date, row[2], row[1], "", -1 * float(row[4])])
            return result

        def process_capital_one(file_data):
            result = []
            for row in file_data[1:-1]:
                date = datetime.datetime.strptime(row[0], '%Y-%m-%d').date().strftime('%m/%d/%Y')
                acc_name, description, category = row[2], row[3], row[4]
                debit, credit = float(row[5]) if row[5] else 0.0, float(row[6]) if row[6] else 0.0
                result.append([date, acc_name, description, category, (credit - debit)])
            return result

        file_data1 = []
        file_data2 = []

        amex_headers = ['Date', 'Description', 'Card Member', 'Account #', 'Amount']
        capital_one_headers = ['Transaction Date', 'Posted Date', 'Card No.', 'Description', 'Category', 'Debit', 'Credit']

        file_path1 = self.file_path_var1.get()
        file_path2 = self.file_path_var2.get()

        with open(file_path1, newline='') as file1, open(file_path2, newline='') as file2:
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)
            for row in reader1:
                file_data1.append(row)
            for row in reader2:
                file_data2.append(row)

        final_result = []

        if file_data1[0] == amex_headers:
            final_result.extend(process_amex(file_data1))
        else:
            final_result.extend(process_capital_one(file_data1))

        if file_data2[0] == amex_headers:
            final_result.extend(process_amex(file_data2))
        else:
            final_result.extend(process_capital_one(file_data2))

        # Sort final_result by date in ascending order
        final_result.sort(key=lambda x: datetime.datetime.strptime(x[0], '%m/%d/%Y'))



        final_result = [['Date', 'Acc # or Name', 'Description', 'Category', 'Amount']] + final_result

        viewer = CSVDataViewer(self.root, final_result)
        viewer.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    app = CSVFileProcessor(root)
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    root.mainloop()