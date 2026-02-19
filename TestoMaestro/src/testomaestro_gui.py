# TestoMaestro
# Diritti d'autore (c) 2026 Igor Vesentini
# Licenza: MIT

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
from datetime import datetime
from info_app import APP_NAME, APP_VERSION, APP_AUTHOR, APP_YEAR, APP_LICENSE

# ===== Theme e font moderni =====
BG_COLOR = "#f5f5f5"            # Sfondo finestra
FRAME_COLOR = "#e8e8e8"         # Colori frame
ENTRY_BG = "#ffffff"             # Background entry / optionmenu
ACCENT_COLOR = "#4a90e2"        # Colore accenti / bordi
FONT_PREVIEW = ("Consolas", 10) # Monospazio per anteprima
FONT_DEFAULT = ("Segoe UI", 10)

FRAME_BG_COLOR = "#e0e0e0"  # grigio chiaro pastello
LABEL_BG_COLOR = "#e0e0e0"

class TestoMaestroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v.{APP_VERSION}")


        # ===== Step 1: sfondo chiaro e dimensione finestra =====
        BG_COLOR = "#f5f5f5"
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("900x600")

        # Variabili
        self.file_path = tk.StringVar()
        self.last_folder = os.getcwd()
        self.file_type = tk.StringVar(value="fisso")  # default fisso
        self.csv_header = tk.BooleanVar(value=True)
        self.csv_separator = tk.StringVar(value=",")

        self.preview_text = None

        # Liste dinamiche per multi-filtro e multi-ordinamento
        self.filter_rows = []
        self.sort_rows = []

        # Dati colonne CSV (aggiornati al caricamento del file)
        self.csv_columns = []

        self.create_widgets()

    def update_filters_dropdown(self):
        if self.file_type.get() != "csv":
            return

        for row in self.filter_rows:
            col_var = row["col_var"]
            col_widget = row["col_widget"]

            if isinstance(col_widget, ttk.OptionMenu):
                menu = col_widget["menu"]
                menu.delete(0, "end")

                for c in self.csv_columns:
                    menu.add_command(
                        label=c,
                        command=lambda value=c, v=col_var: v.set(value)
                    )

                if self.csv_columns:
                    col_var.set(self.csv_columns[0])

    def create_widgets(self):
        style = ttk.Style()
        style.configure("My.TLabelframe", background=FRAME_BG_COLOR, font=FONT_DEFAULT)
        style.configure("My.TLabelframe.Label", background=FRAME_BG_COLOR, font=FONT_DEFAULT)
        style.configure("My.TLabel", background=LABEL_BG_COLOR, font=FONT_DEFAULT)
        style.configure("My.TButton", font=FONT_DEFAULT)
        style.configure("My.TEntry", font=FONT_DEFAULT)
    
        # ===== Selezione file =====
        file_frame = ttk.LabelFrame(self.root, text="File di input", style="My.TLabelframe")
        file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        entry_file = ttk.Entry(
            file_frame,
            textvariable=self.file_path,
            width=50,
            state="readonly",
            font=FONT_DEFAULT
        )
        entry_file.grid(row=0, column=0, padx=5, pady=5)
    
        btn_browse = ttk.Button(file_frame, text="Sfoglia...", command=self.browse_file, style="My.TButton")
        btn_browse.grid(row=0, column=1, padx=5, pady=5)
    
        # ===== Bottone Info in alto a destra =====
        self.btn_info = ttk.Button(
            self.root,
            text="Info",
            width=6,                   # compatto
            command=self.show_app_info, # funzione che mostrerà nome, versione, licenza ecc.
            style="My.TButton"
        )
        # posizionato sopra tutto, ancorato in alto a destra
        self.btn_info.place(relx=1.0, x=-10, y=10, anchor="ne")   
        
        # ===== Filtri =====
        self.filter_frame = ttk.LabelFrame(self.root, text="Filtri (multi)", style="My.TLabelframe")
        self.filter_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.update_filter_labels()
        self.add_filter_row(start_row=1)
        btn_add_filter = ttk.Button(self.filter_frame, text="+ Aggiungi filtro", command=self.add_filter_row, style="My.TButton")
        btn_add_filter.grid(row=99, column=0, columnspan=5, pady=5, sticky="w")
    
        # ===== Ordinamenti =====
        self.sort_frame = ttk.LabelFrame(self.root, text="Ordinamenti (multi)", style="My.TLabelframe")
        self.sort_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.update_sort_labels()
        self.add_sort_row()
        btn_add_sort = ttk.Button(self.sort_frame, text="+ Aggiungi ordinamento", command=self.add_sort_row, style="My.TButton")
        btn_add_sort.grid(row=99, column=0, columnspan=3, pady=5, sticky="w")
    
        # ===== Anteprima =====
        preview_frame = ttk.LabelFrame(self.root, text="Anteprima (prime 10 righe)", style="My.TLabelframe")
        preview_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
    
        self.preview_text = tk.Text(preview_frame, height=10, width=80, state="disabled", font=FONT_PREVIEW)
        self.preview_text.grid(row=0, column=0, padx=5, pady=5)
    
        # ===== Pulsanti =====
        self.btn_execute = ttk.Button(self.root, text="Esegui", command=self.execute, style="My.TButton")
        self.btn_execute.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.btn_execute.grid_remove()
    
        self.btn_preview_out = ttk.Button(self.root, text="Mostra anteprima output", command=self.show_output_preview, style="My.TButton")
        self.btn_preview_out.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.btn_preview_out.grid_remove()
    
        # Espandi anteprima quando finestra ridimensionata
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    # ===== Label guida dinamica per filtri =====
    def update_filter_labels(self):
        for widget in self.filter_frame.grid_slaves(row=0):
            widget.destroy()
    
        if self.file_type.get() == "csv":
            ttk.Label(self.filter_frame, text="Colonna", style="My.TLabel").grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="Filtro", style="My.TLabel").grid(row=0, column=1, padx=5, pady=2)
        else:
            ttk.Label(self.filter_frame, text="Da", style="My.TLabel").grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="A", style="My.TLabel").grid(row=0, column=1, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="Filtro", style="My.TLabel").grid(row=0, column=2, padx=5, pady=2)
            ttk.Label(self.filter_frame, text="Operatore", style="My.TLabel").grid(row=0, column=3, padx=5, pady=2)

    # ===== Multi-filtro =====
    def add_filter_row(self, start_row=1):
        row_idx = start_row + len(self.filter_rows)
    
        if self.file_type.get() == "csv":
            col_var = tk.StringVar()
            val_var = tk.StringVar()
    
            # OptionMenu con font moderno
            col_menu = ttk.OptionMenu(
                self.filter_frame,
                col_var,
                *(self.csv_columns if self.csv_columns else ["-"])
            )
            col_menu.config(width=15)
            col_menu["menu"].config(font=FONT_DEFAULT)
    
            val_entry = ttk.Entry(self.filter_frame, textvariable=val_var, width=15, font=FONT_DEFAULT)
            op_var = None
            op_menu = None
        else:
            col_start_var = tk.StringVar()
            col_end_var = tk.StringVar()
            val_var = tk.StringVar()
            op_var = tk.StringVar(value="=")
    
            col_entry_start = ttk.Entry(self.filter_frame, textvariable=col_start_var, width=8, font=FONT_DEFAULT)
            col_entry_end = ttk.Entry(self.filter_frame, textvariable=col_end_var, width=8, font=FONT_DEFAULT)
            col_menu = (col_entry_start, col_entry_end)
    
            val_entry = ttk.Entry(self.filter_frame, textvariable=val_var, width=15, font=FONT_DEFAULT)
            op_menu = ttk.OptionMenu(self.filter_frame, op_var, op_var.get(), "=", "!=", ">", "<", ">=", "<=", "~", "!~")
            op_menu.config(width=3)
            op_menu["menu"].config(font=FONT_DEFAULT)
    
        # Inserisci nella griglia
        if isinstance(col_menu, tuple):
            for i, w in enumerate(col_menu):
                w.grid(row=row_idx, column=i, padx=5, pady=2)
            val_entry.grid(row=row_idx, column=2, padx=5, pady=2)
            if op_menu:
                op_menu.grid(row=row_idx, column=3, padx=5, pady=2)
        else:
            col_menu.grid(row=row_idx, column=0, padx=5, pady=2)
            val_entry.grid(row=row_idx, column=1, padx=5, pady=2)
            if op_menu:
                op_menu.grid(row=row_idx, column=3, padx=5, pady=2)
    
        # Bottone ❌ con font moderno
        btn_remove = ttk.Button(self.filter_frame, text="❌", style="My.TButton")
        btn_remove.grid(row=row_idx, column=99, padx=5, pady=2)
    
        # Riga come dizionario
        row_dict = {
            "col_var": col_var if self.file_type.get() == "csv" else (col_start_var, col_end_var),
            "val_var": val_var,
            "col_widget": col_menu,
            "val_widget": val_entry,
            "op_var": op_var,
            "op_widget": op_menu,
            "btn_remove": btn_remove
        }
    
        # Assegna comando al bottone
        btn_remove.config(command=lambda r=row_dict: self.remove_filter_row_by_object(r))
        self.filter_rows.append(row_dict)

    def remove_filter_row_by_object(self, row):
        if row not in self.filter_rows:
            return
    
        # Distruggi tutti i widget della riga
        col_widget = row["col_widget"]
        val_widget = row["val_widget"]
        op_widget = row.get("op_widget")
        btn_remove = row.get("btn_remove")
    
        if isinstance(col_widget, tuple):
            for w in col_widget:
                w.destroy()
        else:
            col_widget.destroy()
    
        val_widget.destroy()
        if op_widget:
            op_widget.destroy()
        if btn_remove:
            btn_remove.destroy()
    
        # Rimuovi dalla lista
        self.filter_rows.remove(row)
    
        # Riallinea tutte le righe rimanenti
        for i, r in enumerate(self.filter_rows):
            col_w = r["col_widget"]
            val_w = r["val_widget"]
            op_w = r.get("op_widget")
            btn_w = r.get("btn_remove")
    
            if isinstance(col_w, tuple):
                for j, w in enumerate(col_w):
                    w.grid(row=i+1, column=j)
                val_w.grid(row=i+1, column=2)
                if op_w:
                    op_w.grid(row=i+1, column=3)
            else:
                col_w.grid(row=i+1, column=0)
                val_w.grid(row=i+1, column=1)
                if op_w:
                    op_w.grid(row=i+1, column=3)
            if btn_w:
                btn_w.grid(row=i+1, column=99)

    def remove_filter_row_by_frame(self, frame):
        # Trova la riga corrispondente
        for i, r in enumerate(self.filter_rows):
            if r["frame"] == frame:
                # distruggi tutto
                r["frame"].destroy()
                self.filter_rows.pop(i)
                break
        # Riallinea le righe rimanenti
        for idx, r in enumerate(self.filter_rows):
            r["frame"].grid(row=idx+1, column=0, columnspan=100, sticky="w", pady=2)

    def remove_filter_row(self, idx):
        if idx < 0 or idx >= len(self.filter_rows):
            return
    
        row = self.filter_rows[idx]
    
        # Distruggi i widget
        if isinstance(row["col_widget"], tuple):
            for w in row["col_widget"]:
                w.destroy()
        else:
            row["col_widget"].destroy()
        row["val_widget"].destroy()
        row["op_widget"].destroy()
        row["btn_widget"].destroy()
    
        self.filter_rows.pop(idx)
    
        # Riallinea tutte le righe
        for i, r in enumerate(self.filter_rows):
            # Colonne start/end o singola colonna
            if isinstance(r["col_widget"], tuple):
                for j, w in enumerate(r["col_widget"]):
                    w.grid(row=i+1, column=j)
            else:
                r["col_widget"].grid(row=i+1, column=0)
    
            r["val_widget"].grid(row=i+1, column=1 if isinstance(r["col_widget"], tk.Widget) else 2)
            r["op_widget"].grid(row=i+1, column=3)
            r["btn_widget"].grid(row=i+1, column=99)

    # ===== Multi-ordinamento =====
    def add_sort_row(self):
        row_idx = len(self.sort_rows) + 1 if self.file_type.get() != "csv" else len(self.sort_rows)
    
        if self.file_type.get() == "csv":
            col_var = tk.StringVar()
            order_var = tk.StringVar(value="Crescente")
    
            col_entry = ttk.Entry(self.sort_frame, textvariable=col_var, width=15, font=FONT_DEFAULT)
            col_entry.grid(row=row_idx, column=0, padx=5, pady=2)
    
            order_menu = ttk.OptionMenu(self.sort_frame, order_var, order_var.get(), "Crescente", "Decrescente")
            order_menu.config(width=10)
            order_menu["menu"].config(font=FONT_DEFAULT)
            order_menu.grid(row=row_idx, column=1, padx=5, pady=2)
    
            btn_remove = ttk.Button(self.sort_frame, text="❌", style="My.TButton")
            btn_remove.grid(row=row_idx, column=2, padx=5, pady=2)
    
            row_dict = {
                "col_var": col_var,
                "order_var": order_var,
                "col_widget": col_entry,
                "order_widget": order_menu,
                "btn_widget": btn_remove
            }
            btn_remove.config(command=lambda r=row_dict: self.remove_sort_row_by_object(r))
            self.sort_rows.append(row_dict)
    
        else:
            col_start_var = tk.StringVar()
            col_end_var = tk.StringVar()
            order_var = tk.StringVar(value="Crescente")
    
            col_entry_start = ttk.Entry(self.sort_frame, textvariable=col_start_var, width=8, font=FONT_DEFAULT)
            col_entry_end = ttk.Entry(self.sort_frame, textvariable=col_end_var, width=8, font=FONT_DEFAULT)
            col_entry_start.grid(row=row_idx, column=0, padx=5, pady=2)
            col_entry_end.grid(row=row_idx, column=1, padx=5, pady=2)
    
            order_menu = ttk.OptionMenu(self.sort_frame, order_var, order_var.get(), "Crescente", "Decrescente")
            order_menu.config(width=10)
            order_menu["menu"].config(font=FONT_DEFAULT)
            order_menu.grid(row=row_idx, column=2, padx=5, pady=2)
    
            btn_remove = ttk.Button(self.sort_frame, text="❌", style="My.TButton")
            btn_remove.grid(row=row_idx, column=5, padx=5, pady=2)
    
            row_dict = {
                "col_start_var": col_start_var,
                "col_end_var": col_end_var,
                "order_var": order_var,
                "col_start_widget": col_entry_start,
                "col_end_widget": col_entry_end,
                "order_widget": order_menu,
                "btn_widget": btn_remove
            }
            btn_remove.config(command=lambda r=row_dict: self.remove_sort_row_by_object(r))
            self.sort_rows.append(row_dict)

    def remove_sort_row_by_object(self, row):
        if row not in self.sort_rows:
            return

        # Distruggi tutti i widget della riga
        if self.file_type.get() == "csv":
            row["col_widget"].destroy()
            row["order_widget"].destroy()
            row["btn_widget"].destroy()
        else:
            row["col_start_widget"].destroy()
            row["col_end_widget"].destroy()
            row["order_widget"].destroy()
            row["btn_widget"].destroy()

        # Rimuovi dalla lista
        self.sort_rows.remove(row)

        # Riallinea tutte le righe rimanenti
        for i, r in enumerate(self.sort_rows):
            if self.file_type.get() == "csv":
                r["col_widget"].grid(row=i, column=0, padx=5, pady=2)
                r["order_widget"].grid(row=i, column=1, padx=5, pady=2)
                r["btn_widget"].grid(row=i, column=2, padx=5, pady=2)
            else:
                r["col_start_widget"].grid(row=i, column=0, padx=5, pady=2)
                r["col_end_widget"].grid(row=i, column=1, padx=5, pady=2)
                r["order_widget"].grid(row=i, column=2, padx=5, pady=2)
                r["btn_widget"].grid(row=i, column=5, padx=5, pady=2)

    def remove_sort_row(self, idx):
        row = self.sort_rows[idx]
        for widget in row[2:]:
            widget.destroy()
        self.sort_rows.pop(idx)
        for i, row in enumerate(self.sort_rows):
            row[2].grid(row=i, column=0)
            row[3].grid(row=i, column=1)
            row[4].grid(row=i, column=2)

    def check_fixed_sort_rows(self, lines):
        """
        Controlla le righe di ordinamento per file fisso.
        Ritorna una lista di messaggi di errore per le righe non valide.
        Ignora le righe completamente vuote.
        """
        error_list = []
        max_len = len(lines[0]) if lines else 0

        for idx, row in enumerate(self.sort_rows):
            start_var = row["col_start_var"]
            end_var = row["col_end_var"]
            order_var = row["order_var"]

            start_val = start_var.get().strip()
            end_val = end_var.get().strip()

            # riga completamente vuota
            if not start_val and not end_val:
                continue

            # entrambi devono essere valorizzati
            if not start_val or not end_val:
                error_list.append(f"Riga {idx+1}: entrambi i campi Da e A devono essere valorizzati")
                continue

            # controlli numerici
            if not start_val.isdigit() or int(start_val) <= 0:
                error_list.append(f"Riga {idx+1}: Da deve essere > 0")
            if not end_val.isdigit() or int(end_val) <= 0:
                error_list.append(f"Riga {idx+1}: A deve essere > 0")

            if start_val.isdigit() and end_val.isdigit():
                start, end = int(start_val), int(end_val)
                if end < start:
                    error_list.append(f"Riga {idx+1}: A non può essere minore di Da")
                if end > max_len:
                    error_list.append(f"Riga {idx+1}: A non può superare la lunghezza del file ({max_len})")

        return error_list

    # ===== File handling =====
    def browse_file(self):
        filetypes = (("All files", "*.*"), ("CSV files", "*.csv"), ("Fisso files", "*.txt"))
        filename = filedialog.askopenfilename(initialdir=self.last_folder, title="Seleziona file", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
            self.last_folder = os.path.dirname(filename)
            self.load_file()

    def update_csv_options(self, value):
        # Mostra/nascondi opzioni CSV
        if value == "csv":
            self.csv_frame.grid()
        else:
            self.csv_frame.grid_remove()

        # Aggiorna label filtri
        self.update_filter_labels()

        # Distruggi vecchie righe dei filtri
        for row in self.filter_rows:
                col_w = row.get("col_widget")
                if col_w:
                        if isinstance(col_w, tuple):
                                for i, w in enumerate(col_w):
                                        w.destroy()
                        else:
                                col_w.destroy()

                val_w = row.get("val_widget")
                if val_w:
                        val_w.destroy()

                op_w = row.get("op_widget")
                if op_w:
                        op_w.destroy()

                btn_w = row.get("btn_remove")
                if btn_w:
                        btn_w.destroy()

        self.filter_rows.clear()

        # Aggiungi una riga di filtro corretta per il nuovo tipo
        self.add_filter_row(start_row=1)

        # Ricarica file (opzionale)
        self.load_file()

        # Aggiorna intestazioni ordinamenti per file fisso
        if self.file_type.get() != "csv":
            self.update_sort_labels()

    def load_file(self):
        path = self.file_path.get()
        if not os.path.isfile(path):
            return
        try:
            if self.file_type.get() == "csv":
                sep = self.csv_separator.get()
                if sep == "\\t":
                    sep = "\t"
                try:
                    # Prova a leggere con pandas
                    df = pd.read_csv(path, sep=sep, header=0 if self.csv_header.get() else None, dtype=str)
    
                    # ===== PATCH: verifica parsing reale =====
                    if len(df.columns) == 1 and sep not in str(df.columns[0]):
                        raise ValueError("Separatore non valido, fallback raw")
                    # ===== FINE PATCH =====
    
                    self.csv_columns = (
                        list(df.columns)
                        if self.csv_header.get()
                        else [str(i + 1) for i in range(len(df.columns))]
                    )
                    self.update_filters_dropdown()
                    self.show_preview(df)
    
                except Exception:
                    # Fallback: mostra file raw
                    with open(path, "r", encoding="utf-8") as f:
                        lines = [f.readline().rstrip("\n") for _ in range(10)]
                    preview = "\n".join(lines)
                    self.preview_text.config(state="normal")
                    self.preview_text.delete(1.0, tk.END)
                    self.preview_text.insert(tk.END, preview)
                    self.preview_text.config(state="disabled")
            else:
                with open(path, "r", encoding="utf-8") as f:
                    lines = [f.readline().rstrip("\n") for _ in range(10)]
                preview = "\n".join(lines)
                self.preview_text.config(state="normal")
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, preview)
                self.preview_text.config(state="disabled")
    
            # Mostra pulsanti esegui e anteprima
            self.btn_execute.grid()
            self.btn_preview_out.grid()
    
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
            highlight_positions = []

            if self.file_type.get() == "csv":
                sep = self.csv_separator.get()
                if sep == "\\t":
                    sep = "\t"
                import pandas as pd

                df = pd.read_csv(path, sep=sep, header=0 if self.csv_header.get() else None, dtype=str)
                
                for row in self.filter_rows:
                    col = row["col_var"].get()
                    val = row["val_var"].get()
                    if col and val and col in df.columns:
                        df = df[df[col].astype(str) == str(val)]
                
                preview = df.head(10).to_string(index=False)

            else:  # file fisso
                with open(path, "r", encoding="utf-8") as f:
                    lines = [f.readline().rstrip("\n") for _ in range(10)]

                # --- controlli filtri ---
                errors = self.check_fixed_filter_rows(lines)
                if errors:
                    alert_msg = "Controlli campi filtro:\n" + "\n".join(errors)
                    self.show_error(alert_msg)
                    return  # non applica filtri se ci sono errori

                # raccolta filtri e highlight
                filters_list = []
                highlight_positions = []
                for row in self.filter_rows:
                    start_val = row["col_var"][0].get()
                    end_val   = row["col_var"][1].get()
                    val       = row["val_var"].get()
                    op        = row["op_var"].get() or "="

                    if start_val.isdigit() and end_val.isdigit() and val:
                        start, end = int(start_val), int(end_val)
                        filters_list.append((start, end, op, val))
                        highlight_positions.append((start-1, end))

                # applica filtri
                from engine import apply_filters_fixed, sort_fixed
                filtered_lines = apply_filters_fixed(lines, filters_list) if filters_list else lines

                # raccolta ordinamenti
                sorts_list = []
                for row in self.sort_rows:
                    start_val = row["col_start_var"].get()
                    end_val   = row["col_end_var"].get()
                    order_val = row["order_var"].get()
                    if start_val.isdigit() and end_val.isdigit():
                        ascending = order_val.lower() == "crescente"
                        sorts_list.append(((int(start_val), int(end_val)), ascending))

                # applica ordinamenti
                if sorts_list:
                    filtered_lines = sort_fixed(filtered_lines, sorts_list)

                # mostra nel widget
                self.preview_text.config(state="normal")
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, "\n".join(filtered_lines))

                # evidenzia colonne dei filtri
                for start, end in highlight_positions:
                    for i, line in enumerate(filtered_lines):
                        line_len = len(line)
                        s = min(start, line_len)
                        e = min(end, line_len)
                        if s < e:
                            self.preview_text.tag_add(f"hl{i}", f"{i+1}.{s}", f"{i+1}.{e}")
                            self.preview_text.tag_config(f"hl{i}", background="yellow")

                # sottolinea le colonne degli ordinamenti
                for idx, (cols, ascending) in enumerate(sorts_list):
                    start, end = cols
                    for i, line in enumerate(filtered_lines):
                        line_len = len(line)
                        s = min(start-1, line_len)
                        e = min(end, line_len)
                        if s < e:
                            self.preview_text.tag_add(f"sort{i}_{idx}", f"{i+1}.{s}", f"{i+1}.{e}")
                            self.preview_text.tag_config(f"sort{i}_{idx}", underline=1)

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
                col = row["col_var"].get().strip()
                val = row["val_var"].get().strip()
                if col and not val:
                    self.show_error(f"Filtro mancante per colonna '{col}'")
                    return
                elif col and val:
                    filters_list.append((col, val))
            else:  # file fisso
                start = row["col_var"][0].get()
                end = row["col_var"][1].get()
                val = row["val_var"].get()
                op = row["op_var"].get() if row["op_var"] and hasattr(row["op_var"], "get") else "="
                if start and end:
                    filters_list.append((int(start), int(end), op, val))

        # Raccogli ordinamenti
        sorts_list = []
        for row in self.sort_rows:
            if self.file_type.get() == "csv":
                col_var = row["col_var"]
                order_var = row["order_var"]
                col_val = col_var.get()
                order_val = order_var.get()
                if col_val:
                    sorts_list.append((col_val, order_val))
            else:  # file fisso
                start_val = row["col_start_var"].get()
                end_val   = row["col_end_var"].get()
                order_val = row["order_var"]

                if start_val.isdigit() and end_val.isdigit():
                    # gestiamo boolean e string
                    if isinstance(order_val, bool):
                        ascending = order_val
                    else:
                        # se è un Tkinter StringVar o una stringa normale
                        order_str = order_val.get() if hasattr(order_val, "get") else str(order_val)
                        ascending = order_str.lower() == "crescente"

                    sorts_list.append(((int(start_val), int(end_val)), ascending))

        # Scrittura file output
        try:
            from engine import apply_filters_csv, apply_filters_fixed, sort_csv, sort_fixed

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            in_file = self.file_path.get()
            base, ext = os.path.splitext(os.path.basename(in_file))
            out_file = os.path.join(os.path.dirname(in_file), f"{base}_TestoMaestro_{timestamp}{ext}")

            # --- Carica dati e applica filtri e ordinamenti ---
            if self.file_type.get() == "csv":
                sep = self.csv_separator.get()
                if sep == "\\t":
                    sep = "\t"
                rows = [line.rstrip("\n").split(sep) for line in open(in_file, encoding="utf-8")]
                header = rows[0] if self.csv_header.get() else None
                data_rows = rows[1:] if self.csv_header.get() else rows

                if filters_list:
                    data_rows = apply_filters_csv(data_rows, filters_list)

                if sorts_list:
                    sort_sets = []
                    for col_str, order in sorts_list:
                        ascending = str(order).lower() in ["crescente", "asc"]
                        if "-" in col_str:
                            start, end = map(int, col_str.split("-"))
                            cols = list(range(start - 1, end))  # 0-based
                        else:
                            cols = [int(col_str) - 1]  # 0-based
                        sort_sets.append((cols, ascending))
                    data_rows = sort_csv(data_rows, sort_sets)

                if header:
                    data_rows.insert(0, header)

                with open(out_file, "w", encoding="utf-8") as f:
                    for row in data_rows:
                        f.write(sep.join([str(c) for c in row]) + "\n")

            else:  # file fisso
                lines = [line.rstrip("\n") for line in open(in_file, encoding="utf-8")]

                # --- controlli filtri ---
                filter_errors = self.check_fixed_filter_rows(lines)
                # --- controlli ordinamenti ---
                sort_errors = self.check_fixed_sort_rows(lines)
                all_errors = filter_errors + sort_errors
                if all_errors:
                    self.show_error("Errori rilevati:\n" + "\n".join(all_errors))
                    return

                if filters_list:
                    lines = apply_filters_fixed(lines, filters_list)

                if sorts_list:
                    sort_sets = []
                    for (start, end), ascending in sorts_list:
                        sort_sets.append(((start, end), ascending))
                    lines = sort_fixed(lines, sort_sets)

                with open(out_file, "w", encoding="utf-8") as f:
                    for line in lines:
                        f.write(line + "\n")

            messagebox.showinfo("Esegui", f"File prodotto: {out_file}")

        except Exception as e:
            self.show_error(f"Errore durante l'esecuzione:\n{e}")

    def show_error(self, msg):
        messagebox.showerror("Errore", msg)

    def check_fixed_filter_rows(self, lines):
        """
        Controlla le righe di filtro per file fisso.
        Ritorna una lista di tuple (riga_idx, messaggio) per le righe che non rispettano i requisiti.
        Non considera righe completamente vuote.
        """
        error_list = []
        max_len = len(lines[0]) if lines else 0

        for idx, row in enumerate(self.filter_rows):
            start_var, end_var = row["col_var"]
            val_var = row["val_var"]
            op_var = row["op_var"]

            start_val = start_var.get().strip()
            end_val = end_var.get().strip()
            val = val_var.get()
            op = op_var.get() if op_var else "="

            # se la riga è completamente vuota, la saltiamo
            if not start_val and not end_val and not val:
                continue

            # tutti i campi devono essere valorizzati se almeno uno è impostato
            if not start_val or not end_val or val is None:
                error_list.append(f"Riga {idx+1}: tutti i campi Da, A, Filtro devono essere valorizzati")
                continue

            # controlli numerici Da e A
            if not start_val.isdigit() or int(start_val) <= 0:
                error_list.append(f"Riga {idx+1}: Campo Da obbligatorio e > 0")
            if not end_val.isdigit() or int(end_val) <= 0:
                error_list.append(f"Riga {idx+1}: Campo A obbligatorio e > 0")

            if start_val.isdigit() and end_val.isdigit():
                start, end = int(start_val), int(end_val)
                if end < start:
                    error_list.append(f"Riga {idx+1}: Campo A non può essere minore di Da")
                if end > max_len:
                    error_list.append(f"Riga {idx+1}: Campo A non può superare la lunghezza del file ({max_len})")

                # lunghezza del filtro
                if op not in ["~", "!~"]:  # operatori contiene/non contiene
                    if len(val) != (end - start + 1):
                        error_list.append(f"Riga {idx+1}: Lunghezza Filtro deve essere {end - start + 1}")
                else:
                    if len(val) > (end - start + 1):
                        error_list.append(f"Riga {idx+1}: Lunghezza Filtro non può superare {end - start + 1}")

        return error_list

    def update_sort_labels(self):
        for widget in self.sort_frame.grid_slaves(row=0):
            widget.destroy()
    
        if self.file_type.get() != "csv":
            ttk.Label(self.sort_frame, text="Da", style="My.TLabel").grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(self.sort_frame, text="A", style="My.TLabel").grid(row=0, column=1, padx=5, pady=2)
            ttk.Label(self.sort_frame, text="Ordinamento", style="My.TLabel").grid(row=0, column=2, padx=5, pady=2)

    def show_app_info(self):
        info_text = f"{APP_NAME} v.{APP_VERSION}\n© {APP_YEAR} {APP_AUTHOR}\nLicenza: {APP_LICENSE}"
        messagebox.showinfo("Informazioni App", info_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestoMaestroGUI(root)
    root.mainloop()
