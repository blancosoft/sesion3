import tkinter as tk
from tkinter import messagebox, ttk


SETS = {
    "Novato": (0.0, 0.0, 5.0),
    "Intermedio": (2.0, 5.0, 8.0),
    "Experto": (5.0, 10.0, 20.0),
}


def membresia_triangular(value, left, peak, right):
    """Calcula el grado de pertenencia de una funcion triangular."""
    if value <= left or value >= right:
        return 0.0
    if left < value <= peak:
        return (value - left) / (peak - left)
    return (right - value) / (right - peak)


def evaluar_conductor(years):
    degrees = {
        name: membresia_triangular(years, *vertices)
        for name, vertices in SETS.items()
    }
    best_name = max(degrees, key=degrees.get)
    return degrees, best_name


class FuzzyWorkshopApp(tk.Tk):
    COLORS = {
        "background": "#0d1b2a",
        "panel": "#172b3f",
        "panel_light": "#203b53",
        "text": "#f4f7f9",
        "muted": "#a8bac8",
        "mint": "#58d6b0",
        "coral": "#ff8d78",
        "line": "#35526a",
        "white": "#ffffff",
    }

    def __init__(self):
        super().__init__()
        self.title("Laboratorio de Logica Difusa")
        self.geometry("1180x760")
        self.minsize(980, 650)
        self.configure(bg=self.COLORS["background"])
        self._configure_styles()
        self._build_interface()
        self._draw_membership_chart()
        self._calculate()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "App.TFrame",
            background=self.COLORS["background"],
        )
        style.configure(
            "Panel.TFrame",
            background=self.COLORS["panel"],
        )
        style.configure(
            "Title.TLabel",
            background=self.COLORS["background"],
            foreground=self.COLORS["text"],
            font=("Segoe UI Semibold", 24),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.COLORS["background"],
            foreground=self.COLORS["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "PanelTitle.TLabel",
            background=self.COLORS["panel"],
            foreground=self.COLORS["text"],
            font=("Segoe UI Semibold", 13),
        )
        style.configure(
            "Body.TLabel",
            background=self.COLORS["panel"],
            foreground=self.COLORS["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Value.TLabel",
            background=self.COLORS["panel"],
            foreground=self.COLORS["mint"],
            font=("Segoe UI Semibold", 20),
        )
        style.configure(
            "Action.TButton",
            background=self.COLORS["mint"],
            foreground=self.COLORS["background"],
            font=("Segoe UI Semibold", 10),
            padding=(16, 10),
            borderwidth=0,
        )
        style.map(
            "Action.TButton",
            background=[("active", "#7ee7c8"), ("pressed", "#43b895")],
        )
        style.configure(
            "Treeview",
            background=self.COLORS["panel_light"],
            fieldbackground=self.COLORS["panel_light"],
            foreground=self.COLORS["text"],
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.COLORS["line"],
            foreground=self.COLORS["white"],
            font=("Segoe UI Semibold", 9),
            padding=8,
        )
        style.map("Treeview", background=[("selected", "#2e665f")])

    def _build_interface(self):
        outer = ttk.Frame(self, style="App.TFrame", padding=(30, 26, 30, 24))
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer, style="App.TFrame")
        header.pack(fill="x", pady=(0, 22))
        ttk.Label(header, text="LOGICA DIFUSA", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Taller de laboratorio · Evaluacion de experiencia comercial",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        content = ttk.Frame(outer, style="App.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        self._build_controls(content)
        self._build_results(content)

    def _build_controls(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=22)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        panel.configure(width=300)
        panel.grid_propagate(False)

        ttk.Label(panel, text="Entrada del laboratorio", style="PanelTitle.TLabel").pack(anchor="w")
        ttk.Label(
            panel,
            text="Ingresa los anos de experiencia de tres conductores para evaluar su perfil difuso.",
            style="Body.TLabel",
            wraplength=245,
            justify="left",
        ).pack(anchor="w", pady=(8, 20))

        ttk.Label(panel, text="Conductores (anos)", style="Body.TLabel").pack(anchor="w")
        self.years_var = tk.StringVar(value="3, 6, 12")
        self.years_entry = tk.Entry(
            panel,
            textvariable=self.years_var,
            bg=self.COLORS["panel_light"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["mint"],
            relief="flat",
            font=("Segoe UI", 13),
        )
        self.years_entry.pack(fill="x", ipady=10, pady=(7, 8))
        ttk.Label(
            panel,
            text="Ejemplo: 3, 6, 12",
            style="Body.TLabel",
        ).pack(anchor="w")

        ttk.Button(panel, text="Evaluar conductores", style="Action.TButton", command=self._calculate).pack(
            fill="x", pady=(22, 28)
        )

        ttk.Label(panel, text="Conjuntos difusos", style="PanelTitle.TLabel").pack(anchor="w")
        for name, vertices in SETS.items():
            row = ttk.Frame(panel, style="Panel.TFrame")
            row.pack(fill="x", pady=(14, 0))
            color = self._set_color(name)
            swatch = tk.Canvas(row, width=10, height=10, bg=self.COLORS["panel"], highlightthickness=0)
            swatch.create_oval(1, 1, 9, 9, fill=color, outline=color)
            swatch.pack(side="left", padx=(0, 8))
            ttk.Label(row, text=name, style="Body.TLabel").pack(side="left")
            ttk.Label(row, text=self._format_vertices(vertices), style="Body.TLabel").pack(side="right")

        ttk.Label(
            panel,
            text="El grado de verdad va de 0.0 a 1.0. Un conductor puede pertenecer parcialmente a varias categorias.",
            style="Body.TLabel",
            wraplength=245,
            justify="left",
        ).pack(anchor="w", pady=(28, 0))

    def _build_results(self, parent):
        results = ttk.Frame(parent, style="App.TFrame")
        results.grid(row=0, column=1, sticky="nsew")
        results.columnconfigure(0, weight=1)
        results.rowconfigure(1, weight=1)
        results.rowconfigure(2, weight=1)

        self.status_var = tk.StringVar(value="Resultados listos")
        status = ttk.Frame(results, style="Panel.TFrame", padding=(18, 13))
        status.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        ttk.Label(status, textvariable=self.status_var, style="Body.TLabel").pack(side="left")
        ttk.Label(status, text="MAX de membresias", style="Body.TLabel").pack(side="right")

        table_panel = ttk.Frame(results, style="Panel.TFrame", padding=18)
        table_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        table_panel.columnconfigure(0, weight=1)
        table_panel.rowconfigure(1, weight=1)
        ttk.Label(table_panel, text="Resultado por conductor", style="PanelTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        columns = ("driver", "years", "novice", "intermediate", "expert", "best")
        self.tree = ttk.Treeview(table_panel, columns=columns, show="headings", selectmode="browse")
        headings = {
            "driver": "CONDUCTOR",
            "years": "ANOS",
            "novice": "NOVATO",
            "intermediate": "INTERMEDIO",
            "expert": "EXPERTO",
            "best": "MEJOR AJUSTE",
        }
        widths = {"driver": 95, "years": 75, "novice": 90, "intermediate": 105, "expert": 90, "best": 125}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.tag_configure("even", background="#1c354b")
        self.tree.tag_configure("odd", background="#203b53")

        chart_panel = ttk.Frame(results, style="Panel.TFrame", padding=18)
        chart_panel.grid(row=2, column=0, sticky="nsew")
        chart_panel.columnconfigure(0, weight=1)
        chart_panel.rowconfigure(1, weight=1)
        ttk.Label(chart_panel, text="Funciones de pertenencia", style="PanelTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        self.chart = tk.Canvas(
            chart_panel,
            height=205,
            bg=self.COLORS["panel_light"],
            highlightthickness=0,
        )
        self.chart.grid(row=1, column=0, sticky="nsew")
        self.chart.bind("<Configure>", lambda _event: self._draw_membership_chart())

    def _calculate(self):
        try:
            raw_values = [item.strip() for item in self.years_var.get().split(",") if item.strip()]
            years = [float(item) for item in raw_values]
            if not years:
                raise ValueError("Escribe al menos un valor.")
            if any(value < 0 for value in years):
                raise ValueError("Los anos de experiencia no pueden ser negativos.")
        except ValueError as error:
            messagebox.showerror("Entrada no valida", str(error))
            return

        for item in self.tree.get_children():
            self.tree.delete(item)
        for index, years_value in enumerate(years, start=1):
            degrees, best_name = evaluar_conductor(years_value)
            self.tree.insert(
                "",
                "end",
                values=(
                    f"Conductor {index}",
                    self._format_number(years_value),
                    self._format_number(degrees["Novato"]),
                    self._format_number(degrees["Intermedio"]),
                    self._format_number(degrees["Experto"]),
                    best_name,
                ),
                tags=("even" if index % 2 == 0 else "odd",),
            )
        self.status_var.set(f"{len(years)} conductor(es) evaluado(s) correctamente")

    def _draw_membership_chart(self):
        if not hasattr(self, "chart"):
            return
        self.chart.delete("all")
        width = max(self.chart.winfo_width(), 500)
        height = max(self.chart.winfo_height(), 205)
        left, right, top, bottom = 48, width - 24, 18, height - 36
        x_max = 20.0

        self.chart.create_line(left, bottom, right, bottom, fill=self.COLORS["line"], width=1)
        self.chart.create_line(left, top, left, bottom, fill=self.COLORS["line"], width=1)
        for tick in range(0, 21, 5):
            x_pos = left + (right - left) * tick / x_max
            self.chart.create_line(x_pos, bottom, x_pos, top, fill="#29475d", dash=(2, 5))
            self.chart.create_text(x_pos, bottom + 15, text=str(tick), fill=self.COLORS["muted"], font=("Segoe UI", 8))
        for degree in (0, 0.5, 1):
            y_pos = bottom - (bottom - top) * degree
            self.chart.create_text(left - 18, y_pos, text=f"{degree:g}", fill=self.COLORS["muted"], font=("Segoe UI", 8))

        for name, (start, peak, end) in SETS.items():
            points = []
            for value in (start, peak, end):
                x_pos = left + (right - left) * value / x_max
                degree = membresia_triangular(value + 0.000001, start, peak, end) if value == peak else 0
                if value == peak:
                    degree = 1
                y_pos = bottom - (bottom - top) * degree
                points.extend((x_pos, y_pos))
            color = self._set_color(name)
            self.chart.create_line(*points, fill=color, width=3, smooth=False)
            label_x = points[2] + 4
            label_y = points[3] - 10
            self.chart.create_text(label_x, label_y, text=name, anchor="w", fill=color, font=("Segoe UI Semibold", 9))
        self.chart.create_text(right, height - 8, text="anos de experiencia", anchor="e", fill=self.COLORS["muted"], font=("Segoe UI", 8))

    @staticmethod
    def _format_vertices(vertices):
        return "(" + ", ".join(str(int(value)) for value in vertices) + ")"

    @staticmethod
    def _format_number(value):
        return f"{value:.3f}".rstrip("0").rstrip(".")

    def _set_color(self, name):
        return {"Novato": self.COLORS["coral"], "Intermedio": "#f7c873", "Experto": self.COLORS["mint"]}[name]


if __name__ == "__main__":
    app = FuzzyWorkshopApp()
    app.mainloop()