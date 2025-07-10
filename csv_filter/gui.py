# --- INIZIO PATCH DRAG & DROP UNIVERSALE ---
try:
    from tkinterdnd2 import TkinterDnD
    TKDND_AVAILABLE = True
except ImportError:
    TKDND_AVAILABLE = False
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import csv
import webbrowser
from filter_logic import filter_major_release, filter_fix_release, EXPECTED_HEADERS
from version_utils import parse_version, detect_encoding

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0", relief='solid', borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    def hide(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class CSVFilterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 CSV Filter - Interfaccia Grafica")
        self.root.geometry("950x750")
        self.root.configure(bg='#f0f0f0')

        # Variabili
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.delimiter = tk.StringVar(value=";")
        self.filter_type = tk.StringVar(value="major")
        self.version_from = tk.StringVar()
        self.version_to = tk.StringVar()
        self.version_exact = tk.StringVar()
        self.last_dir = os.getcwd()
        self.preview_rows = []
        self.preview_headers = []
        self.input_row_count = tk.IntVar(value=0)
        self.output_row_count = tk.IntVar(value=0)
        self.preview_n = tk.IntVar(value=5)
        self.drag_label = None  # label per istruzione drag&drop
        self.col_header_status = tk.StringVar(value="")
        self.col_header_color = tk.StringVar(value="#005fa3")
        self.setup_ui()
        self.setup_drag_and_drop()

    def setup_ui(self):
        # Frame centrale con larghezza massima
        center_frame = tk.Frame(self.root, bg='#f0f0f0')
        center_frame.grid(row=0, column=0, sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        center_frame.grid_propagate(False)
        center_frame.config(width=900)
        main_frame = ttk.Frame(center_frame, padding="10 10 10 10")
        main_frame.pack(expand=True, fill='y')
        main_frame.columnconfigure(1, weight=1)

        title_label = ttk.Label(main_frame, text="🔧 CSV Filter", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        self.create_file_section(main_frame)
        self.create_preview_section(main_frame)
        self.create_options_section(main_frame)
        self.create_filter_section(main_frame)
        self.create_buttons(main_frame)
        self.create_log_section(main_frame)

    def create_file_section(self, parent):
        file_frame = ttk.LabelFrame(parent, text="📁 File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)

        # Riquadro drag & drop sopra il campo File CSV di input
        dragdrop_frame = tk.Frame(file_frame, bd=2, relief='groove', bg='#f8f8f8', highlightbackground='#aaa', highlightcolor='#aaa', highlightthickness=1, height=48)
        dragdrop_frame.grid(row=0, column=0, columnspan=5, sticky='ew', pady=(0, 6), padx=(0,0))
        dragdrop_frame.grid_propagate(False)
        dragdrop_label = tk.Label(dragdrop_frame, text="⬇️  Trascina qui il file CSV  (o clicca)", font=('Arial', 11, 'bold'), fg='#005fa3', bg='#f8f8f8', justify='center')
        dragdrop_label.place(relx=0.5, rely=0.5, anchor='center')
        if TKDND_AVAILABLE:
            def drop(event):
                files = self.root.tk.splitlist(event.data)
                if files:
                    file = files[0]
                    if file.lower().endswith('.csv'):
                        self.input_file.set(file)
                        base_name = os.path.splitext(file)[0]
                        # Output predefinito in output/
                        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
                        if os.path.isdir(output_dir):
                            output_path = os.path.join(output_dir, f"{base_name}_filtered.csv")
                        else:
                            output_path = os.path.splitext(file)[0] + "_filtered.csv"
                        self.output_file.set(output_path)
                        self.detect_delimiter_and_preview(file)
                        self.open_output_btn.config(state='disabled')
                        self.log_message(f"✅ File caricato tramite Drag & Drop: {os.path.basename(file)}", tag='success')
                        # Highlight breve del riquadro
                        orig = dragdrop_frame.cget('bg')
                        dragdrop_frame.config(bg='#b6fcb6')
                        self.root.after(1200, lambda: dragdrop_frame.config(bg=orig))
            dragdrop_frame.drop_target_register('DND_Files')
            dragdrop_frame.dnd_bind('<<Drop>>', drop)
            # Clic sul riquadro = apri file dialog
            dragdrop_frame.bind('<Button-1>', lambda e: self.browse_input_file())
            dragdrop_label.bind('<Button-1>', lambda e: self.browse_input_file())
        else:
            dragdrop_label.config(text="ℹ️ Drag & Drop non disponibile su questo sistema senza tkinterdnd2.")
            dragdrop_frame.config(bg='#f0e0e0')

        # Sposta tutto il resto in basso di una riga
        ttk.Label(file_frame, text="File CSV di input:").grid(row=1, column=0, sticky=tk.W, pady=5)
        input_entry = ttk.Entry(file_frame, textvariable=self.input_file, width=60)
        input_entry.grid(row=1, column=1, sticky="ew", padx=(10, 5), pady=5)
        ttk.Button(file_frame, text="Sfoglia", command=self.browse_input_file).grid(row=1, column=2, pady=5)
        ttk.Label(file_frame, textvariable=self.input_row_count, foreground='blue').grid(row=1, column=3, sticky=tk.W, padx=(10,0))
        ttk.Label(file_frame, text="righe").grid(row=1, column=4, sticky=tk.W)

        # Sezione informativa sulle colonne richieste (più compatta)
        info_frame = tk.Frame(file_frame, bg='#eaf4fb', bd=1, relief='solid', height=110)
        info_frame.grid(row=4, column=0, columnspan=5, sticky=tk.W+tk.E, pady=(6, 0), padx=(0,0))
        info_frame.grid_propagate(False)
        info_title = tk.Label(info_frame, text="Colonne richieste per il CSV (ordine e nomi esatti):", bg='#eaf4fb', fg='#005fa3', font=('Arial', 9, 'bold'), anchor='w')
        info_title.pack(anchor='w', padx=8, pady=(3,0))
        columns = [
            ("#", "Numero del ticket"),
            ("Oggetto", "Titolo o descrizione breve"),
            ("# Fixed on", "Versione in cui il ticket è stato risolto"),
            ("# Fixed also on", "Altre versioni in cui il ticket è stato risolto"),
            ("# Major release", "Versione di rilascio principale")
        ]
        for col, desc in columns:
            tk.Label(info_frame, text=f"•  {col}", bg='#eaf4fb', fg='#222', font=('Consolas', 9, 'bold')).pack(anchor='w', padx=16, pady=0, side='top')
            tk.Label(info_frame, text=f"    {desc}", bg='#eaf4fb', fg='#444', font=('Arial', 8), anchor='w').pack(anchor='w', padx=32, pady=(0,1), side='top')
        tk.Label(info_frame, text="Esempio intestazione:", bg='#eaf4fb', fg='#005fa3', font=('Arial', 8, 'italic')).pack(anchor='w', padx=8, pady=(2,0))
        tk.Label(info_frame, text="#;Oggetto;# Fixed on;# Fixed also on;# Major release", bg='#eaf4fb', fg='#005fa3', font=('Consolas', 9), anchor='w').pack(anchor='w', padx=16, pady=(0,3))

        ttk.Label(file_frame, text="File CSV di output:").grid(row=2, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(file_frame, textvariable=self.output_file, width=60)
        output_entry.grid(row=2, column=1, sticky="ew", padx=(10, 5), pady=5)
        ttk.Button(file_frame, text="Sfoglia", command=self.browse_output_file).grid(row=2, column=2, pady=5)
        ttk.Label(file_frame, textvariable=self.output_row_count, foreground='green').grid(row=2, column=3, sticky=tk.W, padx=(10,0))
        ttk.Label(file_frame, text="righe").grid(row=2, column=4, sticky=tk.W)

        # Check verde/rosso accanto ai file
        def file_check_label(var):
            def update(*_):
                path = var.get()
                if path and os.path.exists(path):
                    label.config(text="✔", fg="green")
                else:
                    label.config(text="✖", fg="red")
            label = tk.Label(file_frame, text="", font=("Arial", 12, "bold"), bg='#f0f0f0')
            var.trace_add('write', lambda *_: update())
            update()
            return label
        input_check = file_check_label(self.input_file)
        input_check.grid(row=1, column=5, padx=(5,0))
        output_check = file_check_label(self.output_file)
        output_check.grid(row=2, column=5, padx=(5,0))
        # Tooltip
        Tooltip(input_check, "File di input esistente")
        Tooltip(output_check, "File di output esistente o scrivibile")
        Tooltip(dragdrop_label, "Trascina qui il file CSV oppure clicca per selezionare")
        Tooltip(input_entry, "Percorso del file CSV di input")
        Tooltip(output_entry, "Percorso del file CSV di output")

        # Validazione colonne live
        col_header_label = tk.Label(info_frame, textvariable=self.col_header_status, bg='#eaf4fb', fg='#005fa3', font=('Arial', 9, 'bold'), anchor='w')
        col_header_label.pack(anchor='w', padx=8, pady=(0,2))
        self.col_header_label = col_header_label

    def create_preview_section(self, parent):
        # Splitter tra preview e log
        paned = ttk.Panedwindow(parent, orient=tk.VERTICAL)
        paned.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        preview_frame = ttk.Labelframe(paned, text="👁 Anteprima CSV (prime N righe)", padding="10")
        paned.add(preview_frame, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        ttk.Label(preview_frame, text="N righe da mostrare:").grid(row=0, column=0, sticky=tk.W)
        spin = ttk.Spinbox(preview_frame, from_=1, to=100, textvariable=self.preview_n, width=5, command=self.update_preview)
        spin.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        self.preview_table = scrolledtext.ScrolledText(preview_frame, height=8, width=110, state='disabled', font=('Consolas', 10))
        self.preview_table.grid(row=1, column=0, columnspan=5, sticky="ew")
        Tooltip(spin, "Numero di righe da mostrare in anteprima")
        Tooltip(self.preview_table, "Anteprima del contenuto CSV")
        self.paned = paned

    def update_preview(self):
        self.preview_table.config(state='normal')
        self.preview_table.delete(1.0, tk.END)
        n = self.preview_n.get()
        if self.preview_headers:
            self.preview_table.insert(tk.END, '\t'.join(self.preview_headers) + '\n')
            for row in self.preview_rows[:n]:
                self.preview_table.insert(tk.END, '\t'.join(row) + '\n')
        self.preview_table.config(state='disabled')

    def create_options_section(self, parent):
        options_frame = ttk.LabelFrame(parent, text="⚙️ Opzioni", padding="10")
        options_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)

        ttk.Label(options_frame, text="Delimiter:").grid(row=0, column=0, sticky=tk.W, pady=5)
        delimiter_combo = ttk.Combobox(options_frame, textvariable=self.delimiter, values=[";", ",", "\t", "|"], width=10)
        delimiter_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        ttk.Label(options_frame, text="Tipo di filtro:").grid(row=1, column=0, sticky=tk.W, pady=5)
        filter_radio = ttk.Frame(options_frame)
        filter_radio.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Radiobutton(filter_radio, text="Major Release", variable=self.filter_type, value="major", command=self.on_filter_type_change).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(filter_radio, text="Fix Release", variable=self.filter_type, value="fix", command=self.on_filter_type_change).pack(side=tk.LEFT)

    def create_filter_section(self, parent):
        self.filter_frame = ttk.LabelFrame(parent, text="🎯 Parametri Filtro", padding="10")
        self.filter_frame.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        self.filter_frame.columnconfigure(1, weight=1)
        self.create_major_filter_widgets()

    def create_major_filter_widgets(self):
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.filter_frame, text="Versione precedente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_from = ttk.Entry(self.filter_frame, textvariable=self.version_from, width=20)
        entry_from.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Label(self.filter_frame, text="(es. 6.95.0)").grid(row=0, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        ttk.Label(self.filter_frame, text="Versione di rilascio:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_to = ttk.Entry(self.filter_frame, textvariable=self.version_to, width=20)
        entry_to.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Label(self.filter_frame, text="(es. 6.97.0)").grid(row=1, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        entry_from.focus_set()

    def create_fix_filter_widgets(self):
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.filter_frame, text="Versione di FIX:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_fix = ttk.Entry(self.filter_frame, textvariable=self.version_exact, width=20)
        entry_fix.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Label(self.filter_frame, text="(es. 6.96.1)").grid(row=0, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        entry_fix.focus_set()

    def on_filter_type_change(self):
        if self.filter_type.get() == "major":
            self.create_major_filter_widgets()
        else:
            self.create_fix_filter_widgets()

    def create_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=4, pady=(0, 10))
        ttk.Button(button_frame, text="🚀 Esegui Filtro", command=self.execute_filter, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Pulisci Log", command=self.clear_log).pack(side=tk.LEFT)
        self.open_output_btn = ttk.Button(button_frame, text="📂 Apri file output", command=self.open_output_file, state='disabled')
        self.open_output_btn.pack(side=tk.LEFT, padx=(10, 0))

    def create_log_section(self, parent):
        # Usa lo stesso panedwindow per log
        log_frame = ttk.Labelframe(self.paned, text="📋 Log", padding="10")
        self.paned.add(log_frame, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(6, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=110)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.tag_config('success', foreground='green')
        self.log_text.tag_config('error', foreground='red')
        self.log_text.tag_config('info', foreground='blue')
        Tooltip(self.log_text, "Log delle operazioni e messaggi di errore")

    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Seleziona file CSV di input",
            initialdir=self.last_dir,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.last_dir = os.path.dirname(filename)
            self.input_file.set(filename)
            # Output predefinito in output/
            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
            if os.path.isdir(output_dir):
                output_path = os.path.join(output_dir, f"{base_name}_filtered.csv")
            else:
                output_path = os.path.splitext(filename)[0] + "_filtered.csv"
            self.output_file.set(output_path)
            self.detect_delimiter_and_preview(filename)
            self.open_output_btn.config(state='disabled')

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Salva file CSV di output",
            initialdir=self.last_dir,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.last_dir = os.path.dirname(filename)
            self.output_file.set(filename)

    def detect_delimiter_and_preview(self, filename):
        try:
            encoding = detect_encoding(filename)
            with open(filename, 'r', encoding=encoding) as f:
                sample = f.read(2048)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample, delimiters=';,\t|')
            self.delimiter.set(dialect.delimiter)
            with open(filename, 'r', encoding=encoding) as f:
                reader = csv.reader(f, delimiter=dialect.delimiter)
                rows = list(reader)
                self.preview_headers = rows[0] if rows else []
                self.preview_rows = rows[1:] if len(rows) > 1 else []
                self.input_row_count.set(len(rows)-1 if len(rows)>0 else 0)
            # Validazione colonne live
            if [h.strip() for h in self.preview_headers] == [h.strip() for h in EXPECTED_HEADERS]:
                self.col_header_status.set("✔ Colonne OK")
                self.col_header_label.config(fg="green")
            else:
                self.col_header_status.set(f"✖ Colonne non valide!\nAtteso: {EXPECTED_HEADERS}\nTrovato: {self.preview_headers}")
                self.col_header_label.config(fg="red")
            self.update_preview()
            self.log_message(f"ℹ️ Delimiter rilevato: '{dialect.delimiter}' (encoding: {encoding})", tag='info')
        except Exception as e:
            self.preview_headers = []
            self.preview_rows = []
            self.input_row_count.set(0)
            self.col_header_status.set("")
            self.update_preview()
            self.log_message(f"⚠️ Impossibile rilevare il delimitatore o leggere il file: {e}", tag='error')

    def open_output_file(self):
        output_path = self.output_file.get()
        if output_path and os.path.exists(output_path):
            webbrowser.open(output_path)
        else:
            messagebox.showerror("Errore", "Il file di output non esiste!")

    def log_message(self, message, tag=None):
        self.log_text.config(state='normal')
        if tag:
            self.log_text.insert(tk.END, f"{message}\n", tag)
        else:
            self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

    def validate_inputs(self):
        if not self.input_file.get():
            messagebox.showerror("Errore", "Seleziona un file CSV di input!")
            return False
        if not self.output_file.get():
            messagebox.showerror("Errore", "Seleziona un file CSV di output!")
            return False
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Errore", "Il file di input non esiste!")
            return False
        return True

    def execute_filter(self):
        if not self.validate_inputs():
            return
        try:
            self.log_message("🔧 Avvio filtro CSV...", tag='info')
            if self.filter_type.get() == "major":
                if not self.version_from.get() or not self.version_to.get():
                    messagebox.showerror("Errore", "Inserisci entrambe le versioni per il filtro Major!")
                    return
                if not parse_version(self.version_from.get()) or not parse_version(self.version_to.get()):
                    messagebox.showerror("Errore", "Formato versioni non valido! Usa il formato X.Y.Z")
                    return
                self.log_message(f"📊 Filtro Major Release: da {self.version_from.get()} a {self.version_to.get()}", tag='info')
                count = filter_major_release(
                    self.input_file.get(),
                    self.output_file.get(),
                    self.version_from.get(),
                    self.version_to.get(),
                    self.delimiter.get()
                )
            else:
                if not self.version_exact.get():
                    messagebox.showerror("Errore", "Inserisci la versione di FIX!")
                    return
                if not parse_version(self.version_exact.get()):
                    messagebox.showerror("Errore", "Formato versione non valido! Usa il formato X.Y.Z")
                    return
                self.log_message(f"🔧 Filtro Fix Release: versione {self.version_exact.get()}", tag='info')
                count = filter_fix_release(
                    self.input_file.get(),
                    self.output_file.get(),
                    self.version_exact.get(),
                    self.delimiter.get()
                )
            self.log_message(f"✅ Filtro completato! {count} righe trovate e scritte in {self.output_file.get()}", tag='success')
            self.output_row_count.set(count)
            messagebox.showinfo("Successo", f"Filtro completato!\n{count} righe trovate e scritte in:\n{self.output_file.get()}")
            self.open_output_btn.config(state='normal')
        except ValueError as ve:
            error_msg = str(ve)
            self.log_message(f"❌ Errore: {error_msg}", tag='error')
            messagebox.showerror("Errore", error_msg)
        except Exception as e:
            error_msg = f"Errore imprevisto: {str(e)}"
            self.log_message(f"❌ {error_msg}", tag='error')
            messagebox.showerror("Errore", error_msg)

    def setup_drag_and_drop(self):
        def drop(event):
            files = self.root.tk.splitlist(event.data)
            if files:
                file = files[0]
                if file.lower().endswith('.csv'):
                    self.input_file.set(file)
                    base_name = os.path.splitext(os.path.basename(file))[0]
                    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
                    if os.path.isdir(output_dir):
                        output_path = os.path.join(output_dir, f"{base_name}_filtered.csv")
                    else:
                        output_path = os.path.splitext(file)[0] + "_filtered.csv"
                    self.output_file.set(output_path)
                    self.detect_delimiter_and_preview(file)
                    self.open_output_btn.config(state='disabled')
                    self.log_message(f"✅ File caricato tramite Drag & Drop: {os.path.basename(file)}", tag='success')
                    # Highlight breve del riquadro
                    orig = dragdrop_frame.cget('bg')
                    dragdrop_frame.config(bg='#b6fcb6')
                    self.root.after(1200, lambda: dragdrop_frame.config(bg=orig))
        if TKDND_AVAILABLE:
            self.root.drop_target_register('DND_Files')
            self.root.dnd_bind('<<Drop>>', drop)
        else:
            self.log_message("ℹ️ Drag & Drop non disponibile su questo sistema senza tkinterdnd2.", tag='info')

# --- FINE PATCH DRAG & DROP UNIVERSALE ---

def main():
    if TKDND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = CSVFilterGUI(root)
    root.state('zoomed')  # Massimizza la finestra all'avvio (Windows)
    root.mainloop()

if __name__ == "__main__":
    main() 