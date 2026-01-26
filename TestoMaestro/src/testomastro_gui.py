import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd

class TestoMastroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TestoMastro - GUI")

        # Variabili
        self.file_path = tk.StringVar()
        self.last_folder = os.getcwd()
        self.file_type = tk.StringVar(value="fisso")
        self.csv_header = tk.BooleanVar(value=True)
        self.csv_separator = tk.StringVar(value=",")
        self.sort_column = tk.StringVar()
        self.sort_order = tk.StringVar(value="Crescente")
        self.filter_column = tk.StringVar()
        self.filter_value = tk.StringVar()

        self.preview_text = None

        self.create_widgets()

    def create_widgets(self):
        # ===== Selezione file =====
        file_frame = ttk.LabelFrame(self.root, text="File di input")
        file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        entry_file = ttk.Entry(
            file_frame,
            textvariable=self.file_path,
            width=50,
            state="readonly"
        )
        entry_file.grid(row=0, column=0, padx=5, pady=5)

        btn_browse = ttk.Button(file_frame, text="Sfoglia...", command=self.browse_file)
        btn_browse.grid(row=0, column=1, padx=5, pady=5)

        # ===== Tipo file =====
        type_frame = ttk.LabelFrame(self.root, text="Tipo file")
        type_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(type_frame, text="Seleziona tipo:").grid(row=0, column=0, padx=5, pady=5)
        type_menu = ttk.OptionMenu(type_frame, self.file_type, self.file_type.get(), "fisso", "csv", command=self.update_csv_options)
        type_menu.grid(row=0, column=1, padx=5, pady=5)

        # CSV options
        self.csv_frame = ttk.Frame(type_frame)
        self.csv_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.chk_header = ttk.Checkbutton(self.csv_frame, text="Header", variable=self.csv_header)
        self.chk_header.grid(row=0, column=0, padx=5, pady=2)

        ttk.Label(self.csv_frame, text="Separatore:").grid(row=0, column=1, padx=5, pady=2)
        self.sep_menu = ttk.OptionMenu(self.csv_frame, self.csv_separator, self.csv_separator.get(), ",", ";", "\\t", "|")
        self.sep_menu.grid(row=0, column=2, padx=5, pady=2)

        self.csv_frame.grid_remove()  # inizialmente nascosto se file fisso

        # ===== Ordinamento e filtri =====
        param_frame = ttk.LabelFrame(self.root, text="Ordinamento e filtri")
        param_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(param_frame, text="Colonna da ordinare:").grid(row=0, column=0, padx=5, pady=2)
        self.entry_sort_col = ttk.Entry(param_frame, textvariable=self.sort_column, width=15)
        self.entry_sort_col.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(param_frame, text="Ordine:").grid(row=0, column=2, padx=5, pady=2)
        sort_menu = ttk.OptionMenu(param_frame, self.sort_order, self.sort_order.get(), "Crescente", "Decrescente")
        sort_menu.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(param_frame, text="Filtro colonna:").grid(row=1, column=0, padx=5, pady=2)
        self.entry_filter_col = ttk.Entry(param_frame, textvariable=self.filter_column, width=15)
        self.entry_filter_col.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(param_frame, text="Contiene valore:").grid(row=1, column=2, padx=5, pady=2)
        self.entry_filter_val = ttk.Entry(param_frame, textvariable=self.filter_value, width=15)
        self.entry_filter_val.grid(row=1, column=3, padx=5, pady=2)

        # ===== Anteprima =====
        preview_frame = ttk.LabelFrame(self.root, text="Anteprima (prime 10 righe)")
        preview_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.preview_text = tk.Text(preview_frame, height=10, width=80, state="disabled")
        self.preview_text.grid(row=0, column=0, padx=5, pady=5)

        # ===== Pulsante Esegui =====
        btn_execute = ttk.Button(self.root, text="Esegui", command=self.execute)
        btn_execute.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Espandi anteprima quando finestra ridimensionata
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def browse_file(self):
        filetypes = (("All files", "*.*"), ("CSV files", "*.csv"), ("Fisso files", "*.txt"))
        filename = filedialog.askopenfilename(initialdir=self.last_folder, title="Seleziona file", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
            self.last_folder = os.path.dirname(filename)
            self.load_file()

    def update_csv_options(self, value):
        if value == "csv":
            self.csv_frame.grid()
        else:
            self.csv_frame.grid_remove()
        self.load_file()  # ricarica preview

    def load_file(self):
        path = self.file_path.get()
        if not os.path.isfile(path):
            return
        try:
            if self.file_type.get() == "csv":
                sep = self.csv_separator.get()
                if sep == "\\t":
                    sep = "\t"
                df = pd.read_csv(path, sep=sep, header=0 if self.csv_header.get() else None)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    lines = [f.readline().rstrip("\n") for _ in range(10)]
                preview = "\n".join(lines)

                self.preview_text.config(state="normal")
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, preview)
                self.preview_text.config(state="disabled")
        except Exception as e:
            self.show_error(f"Errore nel caricamento del file:\n{e}")

    def show_preview(self, df):
        preview = df.head(10).to_string(index=False)
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        self.preview_text.config(state="disabled")

    def execute(self):
        path = self.file_path.get()
        if not os.path.isfile(path):
            self.show_error("File non valido!")
            return
        # Qui si collegherà la logica di TestoMastro
        messagebox.showinfo("Esegui", "Esecuzione completata (dummy).")

    def show_error(self, msg):
        messagebox.showerror("Errore", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestoMastroGUI(root)
    root.mainloop()
