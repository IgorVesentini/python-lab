import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
from datetime import datetime

class TestoMaestroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TestoMaestro - GUI")

        # Variabili
        self.file_path = tk.StringVar()
        self.last_folder = os.getcwd()
        self.file_type = tk.StringVar(value="fisso")
        self.csv_header = tk.BooleanVar(value=True)
        self.csv_separator = tk.StringVar(value=",")
        
        self.preview_text = None

        # Liste dinamiche per multi-filtro e multi-ordinamento
        self.filter_rows = []
        self.sort_rows = []

        # Dati colonne CSV (aggiornati al caricamento del file)
        self.csv_columns = []

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
        type_menu = ttk.OptionMenu(
            type_frame, self.file_type, self.file_type.get(),
            "fisso", "csv", command=self.update_csv_options
        )
        type_menu.grid(row=0, column=1, padx=5, pady=5)

        # CSV options
        self.csv_frame = ttk.Frame(type_frame)
        self.csv_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.chk_header = ttk.Checkbutton(self.csv_frame, text="Header", variable=self.csv_header, command=self.update_filters_dropdown)
        self.chk_header.grid(row=0, column=0, padx=5, pady=2)

        ttk.Label(self.csv_frame, text="Separatore:").grid(row=0, column=1, padx=5, pady=2)
        self.sep_menu = ttk.OptionMenu(
            self.csv_frame, self.csv_separator, self.csv_separator.get(), ",", ";", "\\t", "|"
        )
        self.sep_menu.grid(row=0, column=2, padx=5, pady=2)

        self.csv_frame.grid_remove()  # nascosto inizialmente se file fisso

        # ===== Sezione Filtri =====
        self.filter_frame = ttk.LabelFrame(self.root, text="Filtri (multi)")
        self.filter_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Label guida filtri
        self.update_filter_labels()

        # Prima riga filtro
        self.add_filter_row(start_row=1)
        btn_add_filter = ttk.Button(self.filter_frame, text="+ Aggiungi filtro", command=self.add_filter_row)
        btn_add_filter.grid(row=99, column=0, columnspan=5, pady=5, sticky="w")

        # ===== Sezione Ordinamento =====
        self.sort_frame = ttk.LabelFrame(self.root, text="Ordinamenti (multi)")
        self.sort_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.add_sort_row()
        btn_add_sort = ttk.Button(self.sort_frame, text="+ Aggiungi ordinamento", command=self.add_sort_row)
        btn_add_sort.grid(row=99, column=0, columnspan=3, pady=5, sticky="w")

        # ===== Anteprima =====
        preview_frame = ttk.LabelFrame(self.root, text="Anteprima (prime 10 righe)")
        preview_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        self.preview_text = tk.Text(preview_frame, height=10, width=80, state="disabled")
        self.preview_text.grid(row=0, column=0, padx=5, pady=5)

        # ===== Pulsanti Esegui e Anteprima Output =====
        btn_execute = ttk.Button(self.root, text="Esegui", command=self.execute)
        btn_execute.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        btn_preview_out = ttk.Button(self.root, text="Mostra anteprima output", command=self.show_output_preview)
        btn_preview_out.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        # Espandi anteprima quando finestra ridimensionata
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    # ===== Label guida dinamica per filtri =====
    def update_filter_labels(self):
        for widget in self.filter_frame.grid_slaves(row=0):
            widget.destroy()
        if self.file_type.get() == "csv":
            ttk.Label(self.filter_frame, text="Colonna").grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="Valore filtro").grid(row=0, column=1, padx=5, pady=2)
        else:
            ttk.Label(self.filter_frame, text="Colonna da").grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="Colonna a").grid(row=0, column=1, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="Valore filtro").grid(row=0, column=2, padx=5, pady=2)

    # ===== Multi-filtro =====
    def add_filter_row(self, start_row=1):
        row_idx = start_row + len(self.filter_rows)
        if self.file_type.get() == "csv":
            col_var = tk.StringVar()
            col_menu = ttk.OptionMenu(self.filter_frame, col_var, *(self.csv_columns if self.csv_columns else ["-"]))
            col_menu.grid(row=row_idx, column=0, padx=5, pady=2)
            val_var = tk.StringVar()
            val_entry = ttk.Entry(self.filter_frame, textvariable=val_var, width=15)
            val_entry.grid(row=row_idx, column=1, padx=5, pady=2)
            col_widget = col_menu
        else:
            col_start_var = tk.StringVar()
            col_end_var = tk.StringVar()
            col_start_entry = ttk.Entry(self.filter_frame, textvariable=col_start_var, width=8)
            col_end_entry = ttk.Entry(self.filter_frame, textvariable=col_end_var, width=8)
            col_start_entry.grid(row=row_idx, column=0, padx=5, pady=2)
            col_end_entry.grid(row=row_idx, column=1, padx=5, pady=2)
            val_var = tk.StringVar()
            val_entry = ttk.Entry(self.filter_frame, textvariable=val_var, width=15)
            val_entry.grid(row=row_idx, column=2, padx=5, pady=2)
            col_var = (col_start_var, col_end_var)
            col_widget = (col_start_entry, col_end_entry)

        btn_remove = ttk.Button(self.filter_frame, text="❌", command=lambda idx=row_idx: self.remove_filter_row(idx))
        btn_remove.grid(row=row_idx, column=99, padx=5, pady=2)
        self.filter_rows.append((col_var, val_var, col_widget, val_entry, btn_remove))

    def remove_filter_row(self, idx):
        row = self.filter_rows[idx]
        if isinstance(row[2], tuple):
            for w in row[2]:
                w.destroy()
        else:
            row[2].destroy()
        row[3].destroy()
        row[4].destroy()
        self.filter_rows.pop(idx)
        for i, row in enumerate(self.filter_rows):
            if isinstance(row[2], tuple):
                for j, w in enumerate(row[2]):
                    w.grid(row=i+1, column=j)
            else:
                row[2].grid(row=i+1, column=0)
            row[3].grid(row=i+1, column=1 if isinstance(row[2], tk.Widget) else 2)
            row[4].grid(row=i+1, column=99)

    def update_filters_dropdown(self):
        if self.file_type.get() != "csv":
            return
        for row in self.filter_rows:
            col_var = row[0]
            col_menu = row[2]
            menu = col_menu["menu"]
            menu.delete(0, "end")
            for c in self.csv_columns:
                menu.add_command(label=c, command=lambda value=c, v=col_var: v.set(value))

    # ===== Multi-ordinamento =====
    def add_sort_row(self):
        row_idx = len(self.sort_rows)
        col_var = tk.StringVar()
        order_var = tk.StringVar(value="Crescente")
        col_entry = ttk.Entry(self.sort_frame, textvariable=col_var, width=15)
        col_entry.grid(row=row_idx, column=0, padx=5, pady=2)
        order_menu = ttk.OptionMenu(self.sort_frame, order_var, order_var.get(), "Crescente", "Decrescente")
        order_menu.grid(row=row_idx, column=1, padx=5, pady=2)
        btn_remove = ttk.Button(self.sort_frame, text="❌", command=lambda idx=row_idx: self.remove_sort_row(idx))
        btn_remove.grid(row=row_idx, column=2, padx=5, pady=2)
        self.sort_rows.append((col_var, order_var, col_entry, order_menu, btn_remove))

    def remove_sort_row(self, idx):
        row = self.sort_rows[idx]
        for widget in row[2:]:
            widget.destroy()
        self.sort_rows.pop(idx)
        for i, row in enumerate(self.sort_rows):
            row[2].grid(row=i, column=0)
            row[3].grid(row=i, column=1)
            row[4].grid(row=i, column=2)

    # ===== File handling =====
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
        self.update_filter_labels()
        self.load_file()

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
                self.csv_columns = list(df.columns) if self.csv_header.get() else [str(i+1) for i in range(len(df.columns))]
                self.update_filters_dropdown()
                self.show_preview(df)
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

    # ===== Anteprima dinamica output =====
    def show_output_preview(self):
        path = self.file_path.get()
        if not os.path.isfile(path):
            self.show_error("File non valido!")
            return
        try:
            # Applicare filtri
            if self.file_type.get() == "csv":
                sep = self.csv_separator.get()
                if sep == "\\t":
                    sep = "\t"
                df = pd.read_csv(path, sep=sep, header=0 if self.csv_header.get() else None)
                for row in self.filter_rows:
                    col = row[0].get()
                    val = row[1].get()
                    if col and val:
                        df = df[df[col].astype(str).str.contains(val)]
                preview = df.head(10).to_string(index=False)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    lines = [f.readline().rstrip("\n") for _ in range(10)]
                # evidenzia colonne
                highlight_positions = []
                for row in self.filter_rows:
                    start = row[0][0].get()
                    end = row[0][1].get()
                    if start.isdigit() and end.isdigit():
                        highlight_positions.append((int(start)-1, int(end)))  # 1-based to 0-based
                preview_lines = []
                for line in lines:
                    preview_lines.append(line)
                preview = "\n".join(preview_lines)

            # Mostra nel widget con highlight (solo fisso)
            self.preview_text.config(state="normal")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, preview)
            # Highlight per fisso
            if self.file_type.get() == "fisso":
                for start, end in highlight_positions:
                    for i, line in enumerate(lines):
                        line_len = len(line)
                        s = min(start, line_len)
                        e = min(end, line_len)
                        if s < e:
                            self.preview_text.tag_add(f"hl{i}", f"{i+1}.{s}", f"{i+1}.{e}")
                            self.preview_text.tag_config(f"hl{i}", background="yellow")
            self.preview_text.config(state="disabled")
        except Exception as e:
            self.show_error(f"Errore nell'anteprima output:\n{e}")

    # ===== Esegui =====
    def execute(self):
        path = self.file_path.get()
        if not os.path.isfile(path):
            self.show_error("File non valido!")
            return

        # Raccogli filtri
        filters_list = []
        for row in self.filter_rows:
            if self.file_type.get() == "csv":
                col = row[0].get()
                val = row[1].get()
                if col:
                    filters_list.append((col, val))
            else:
                start = row[0][0].get()
                end = row[0][1].get()
                val = row[1].get()
                if start and end:
                    filters_list.append((start, end, val))

        # Raccogli ordinamenti
        sorts_list = [(col.get(), order.get()) for col, order, *rest in self.sort_rows if col.get()]

        # Scrittura file output
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            in_file = self.file_path.get()
            base, ext = os.path.splitext(os.path.basename(in_file))
            out_file = os.path.join(os.path.dirname(in_file), f"{base}_TestoMaestro_{timestamp}{ext}")
            with open(out_file, "w", encoding="utf-8") as f:
                if self.file_type.get() == "csv":
                    f.write("CSV dummy output\n")
                else:
                    f.write("Fisso dummy output\n")
            messagebox.showinfo("Esegui", f"Esecuzione completata.\nFile scritto: {out_file}\nFiltri: {filters_list}\nOrdinamenti: {sorts_list}")
        except Exception as e:
            self.show_error(f"Errore durante l'esecuzione:\n{e}")

    def show_error(self, msg):
        messagebox.showerror("Errore", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestoMaestroGUI(root)
    root.mainloop()
