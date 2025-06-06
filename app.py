import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import csv

class DatabaseViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visor de SQLite")
        self.geometry("800x600")

        self.db_path = None
        self.conn = None

        self.create_widgets()

    def create_widgets(self):
        # Frame de selección de archivo
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        select_btn = ttk.Button(top_frame, text="Seleccionar DB", command=self.select_db)
        select_btn.pack(side=tk.LEFT)

        ttk.Label(top_frame, text="Employee ID:").pack(side=tk.LEFT, padx=5)
        self.employee_entry = ttk.Entry(top_frame, width=10)
        self.employee_entry.pack(side=tk.LEFT)

        ttk.Label(top_frame, text="Fecha (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(top_frame, width=12)
        self.date_entry.pack(side=tk.LEFT)

        search_btn = ttk.Button(top_frame, text="Buscar", command=self.update_table)
        search_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(top_frame, text="Exportar CSV", command=self.export_csv)
        export_btn.pack(side=tk.LEFT, padx=5)

        # Tabla
        self.tree = ttk.Treeview(self, columns=(), show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=scrollbar_x.set)

    def select_db(self):
        path = filedialog.askopenfilename(filetypes=[("SQLite DB", "*.db"), ("All files", "*.*")])
        if path:
            try:
                if self.conn:
                    self.conn.close()
                self.conn = sqlite3.connect(path)
                self.db_path = path
                self.update_table()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo abrir la base de datos: {e}")

    def build_query(self):
        query = "SELECT * FROM att_punches"
        params = []
        conditions = []

        emp = self.employee_entry.get().strip()
        if emp:
            conditions.append("employee_id = ?")
            params.append(emp)

        date = self.date_entry.get().strip()
        if date:
            conditions.append("date(punch_time) = ?")
            params.append(date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " LIMIT 100"
        return query, params

    def update_table(self):
        if not self.conn:
            return
        query, params = self.build_query()
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            cols = [description[0] for description in cur.description]
            self.build_tree(cols)
            self.populate_tree(rows)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Consulta fallida: {e}")

    def build_tree(self, columns):
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)

    def populate_tree(self, rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def export_csv(self):
        if not self.tree.get_children():
            messagebox.showinfo("Info", "No hay datos para exportar")
            return
        with open('resultado.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.tree['columns'])
            for child in self.tree.get_children():
                writer.writerow(self.tree.item(child)['values'])
        messagebox.showinfo("Exportado", "Datos exportados a resultado.csv")

if __name__ == '__main__':
    app = DatabaseViewer()
    app.mainloop()
