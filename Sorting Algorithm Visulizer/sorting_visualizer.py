"""
Sorting Algorithm Visualizer — v2 (Modern Dark UI)
----------------------------------------------------
A polished, dark-themed Python + Tkinter desktop app that visualizes
how popular sorting algorithms work in real time.

Tech stack: Python 3, Tkinter (standard library only — no installs needed)

Algorithms included:
    - Bubble Sort
    - Selection Sort
    - Insertion Sort
    - Merge Sort
    - Quick Sort

Run:
    python sorting_visualizer_v2.py
"""

import random
import time
import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------------
# THEME / COLOR PALETTE
# ----------------------------------------------------------------------
BG_MAIN       = "#0f111a"   # app background
BG_PANEL      = "#161925"   # sidebar / card background
BG_CANVAS     = "#0b0d14"   # chart background
FG_TEXT       = "#e6e6f0"   # primary text
FG_MUTED      = "#8b8fa3"   # secondary text
ACCENT        = "#7c5cff"   # primary accent (purple)
ACCENT_HOVER  = "#9277ff"
ACCENT_2      = "#3fd6c5"   # teal accent for secondary button
BAR_LOW       = (56, 189, 248)    # cool blue  (rgb)
BAR_HIGH      = (124, 92, 255)    # violet     (rgb)
COLOR_COMPARE = "#ff6b6b"   # red   — elements being compared
COLOR_SWAP    = "#ffb020"   # amber — elements being swapped/written
COLOR_PIVOT   = "#3fd6c5"   # teal  — pivot element
COLOR_SORTED  = "#4ade80"   # green — finalized / sorted
FONT_FAMILY   = "Segoe UI"


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB tuples."""
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class RoundedButton(tk.Canvas):
    """A flat, rounded, hover-aware button drawn on a Canvas (nicer than stock tk.Button)."""

    def __init__(self, parent, text, command, bg=ACCENT, hover=ACCENT_HOVER,
                 fg="#ffffff", width=170, height=40, font_size=11, **kwargs):
        super().__init__(parent, width=width, height=height, bg=BG_PANEL,
                          highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover
        self.fg_color = fg
        self.width = width
        self.height = height
        self.disabled = False
        self.text = text
        self.font_size = font_size

        self._draw(bg)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self, color):
        self.delete("all")
        state_fg = FG_MUTED if self.disabled else self.fg_color
        fill = "#2a2d3a" if self.disabled else color
        self._round_rect(2, 2, self.width - 2, self.height - 2, 14, fill=fill, outline="")
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                          fill=state_fg, font=(FONT_FAMILY, self.font_size, "bold"))

    def _on_enter(self, _):
        if not self.disabled:
            self._draw(self.hover_color)

    def _on_leave(self, _):
        if not self.disabled:
            self._draw(self.bg_color)

    def _on_click(self, _):
        if not self.disabled and self.command:
            self.command()

    def set_disabled(self, disabled: bool):
        self.disabled = disabled
        self._draw(self.bg_color)

    def set_text(self, text):
        self.text = text
        self._draw(self.hover_color if False else self.bg_color)


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1150x680")
        self.root.minsize(1000, 620)
        self.root.configure(bg=BG_MAIN)

        self.array = []
        self.array_size = 55
        self.speed = 12          # ms delay, lower = faster
        self.sorting = False
        self.comparisons = 0
        self.swaps = 0
        self.start_time = None

        self._setup_ttk_style()
        self._build_layout()
        self.generate_array()

    # ------------------------------------------------------------------
    # STYLE
    # ------------------------------------------------------------------
    def _setup_ttk_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TCombobox",
                         fieldbackground=BG_PANEL,
                         background=BG_PANEL,
                         foreground=FG_TEXT,
                         arrowcolor=FG_TEXT,
                         bordercolor=BG_PANEL,
                         lightcolor=BG_PANEL,
                         darkcolor=BG_PANEL,
                         padding=6)
        style.map("TCombobox", fieldbackground=[("readonly", BG_PANEL)])

        style.configure("Horizontal.TScale",
                         background=BG_PANEL,
                         troughcolor="#262a3a",
                         sliderthickness=16)

    # ------------------------------------------------------------------
    # LAYOUT
    # ------------------------------------------------------------------
    def _build_layout(self):
        # ----- Header -----
        header = tk.Frame(self.root, bg=BG_MAIN, pady=18, padx=24)
        header.pack(side=tk.TOP, fill=tk.X)

        tk.Label(header, text="Sorting Algorithm Visualizer",
                 bg=BG_MAIN, fg=FG_TEXT,
                 font=(FONT_FAMILY, 20, "bold")).pack(side=tk.LEFT)

        tk.Label(header, text="Watch how algorithms think, one comparison at a time",
                 bg=BG_MAIN, fg=FG_MUTED,
                 font=(FONT_FAMILY, 10)).pack(side=tk.LEFT, padx=16)

        # ----- Body: sidebar (controls) + main (canvas + stats) -----
        body = tk.Frame(self.root, bg=BG_MAIN)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=24, pady=(0, 20))

        self._build_sidebar(body)
        self._build_main_panel(body)

    def _card(self, parent, **pack_opts):
        card = tk.Frame(parent, bg=BG_PANEL, padx=18, pady=16)
        card.pack(**pack_opts)
        return card

    def _section_label(self, parent, text):
        tk.Label(parent, text=text.upper(), bg=BG_PANEL, fg=FG_MUTED,
                 font=(FONT_FAMILY, 9, "bold")).pack(anchor="w", pady=(0, 6))

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_MAIN, width=260)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)

        card = self._card(sidebar, fill=tk.BOTH, expand=True)

        # Algorithm picker
        self._section_label(card, "Algorithm")
        self.algo_var = tk.StringVar(value="Bubble Sort")
        algo_menu = ttk.Combobox(
            card, textvariable=self.algo_var,
            values=["Bubble Sort", "Selection Sort", "Insertion Sort",
                    "Merge Sort", "Quick Sort"],
            state="readonly", font=(FONT_FAMILY, 10)
        )
        algo_menu.pack(fill=tk.X, pady=(0, 18))

        # Array size
        self._section_label(card, "Array Size")
        self.size_value_lbl = tk.Label(card, text=str(self.array_size),
                                        bg=BG_PANEL, fg=ACCENT_2,
                                        font=(FONT_FAMILY, 10, "bold"))
        self.size_value_lbl.pack(anchor="e")
        self.size_slider = tk.Scale(
            card, from_=10, to=150, orient=tk.HORIZONTAL,
            command=self._on_size_change, bg=BG_PANEL, fg=FG_TEXT,
            troughcolor="#262a3a", highlightthickness=0, bd=0,
            activebackground=ACCENT, sliderrelief=tk.FLAT,
            showvalue=False
        )
        self.size_slider.set(self.array_size)
        self.size_slider.pack(fill=tk.X, pady=(0, 18))

        # Speed
        self._section_label(card, "Speed")
        self.speed_value_lbl = tk.Label(card, text="Fast",
                                         bg=BG_PANEL, fg=ACCENT_2,
                                         font=(FONT_FAMILY, 10, "bold"))
        self.speed_value_lbl.pack(anchor="e")
        self.speed_slider = tk.Scale(
            card, from_=1, to=100, orient=tk.HORIZONTAL,
            command=self._on_speed_change, bg=BG_PANEL, fg=FG_TEXT,
            troughcolor="#262a3a", highlightthickness=0, bd=0,
            activebackground=ACCENT, sliderrelief=tk.FLAT,
            showvalue=False
        )
        self.speed_slider.set(88)
        self.speed_slider.pack(fill=tk.X, pady=(0, 24))

        # Buttons
        self.generate_btn = RoundedButton(card, "🔀  New Array", self.generate_array,
                                           bg="#262a3a", hover="#323649", width=224)
        self.generate_btn.pack(pady=(0, 10))

        self.sort_btn = RoundedButton(card, "▶  Start Sorting", self.start_sorting,
                                       bg=ACCENT, hover=ACCENT_HOVER, width=224)
        self.sort_btn.pack()

        # Divider
        tk.Frame(card, bg="#262a3a", height=1).pack(fill=tk.X, pady=20)

        # Legend
        self._section_label(card, "Legend")
        legend_items = [
            (COLOR_COMPARE, "Comparing"),
            (COLOR_SWAP, "Swapping"),
            (COLOR_PIVOT, "Pivot"),
            (COLOR_SORTED, "Sorted"),
        ]
        for color, label in legend_items:
            row = tk.Frame(card, bg=BG_PANEL)
            row.pack(fill=tk.X, pady=3)
            dot = tk.Canvas(row, width=12, height=12, bg=BG_PANEL, highlightthickness=0)
            dot.create_oval(1, 1, 11, 11, fill=color, outline="")
            dot.pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(row, text=label, bg=BG_PANEL, fg=FG_MUTED,
                     font=(FONT_FAMILY, 9)).pack(side=tk.LEFT)

    def _build_main_panel(self, parent):
        main = tk.Frame(parent, bg=BG_MAIN)
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ----- Stats row -----
        stats_row = tk.Frame(main, bg=BG_MAIN)
        stats_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 14))

        self.stat_comparisons = self._stat_card(stats_row, "Comparisons", "0")
        self.stat_swaps = self._stat_card(stats_row, "Swaps / Writes", "0")
        self.stat_time = self._stat_card(stats_row, "Elapsed Time", "0.00s")
        self.stat_status = self._stat_card(stats_row, "Status", "Idle", value_color=ACCENT_2)

        # ----- Canvas card -----
        canvas_card = tk.Frame(main, bg=BG_PANEL, padx=4, pady=4)
        canvas_card.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_card, bg=BG_CANVAS, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.canvas.bind("<Configure>", lambda e: self.draw_array())

    def _stat_card(self, parent, title, value, value_color=FG_TEXT):
        card = tk.Frame(parent, bg=BG_PANEL, padx=16, pady=10)
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(card, text=title.upper(), bg=BG_PANEL, fg=FG_MUTED,
                 font=(FONT_FAMILY, 8, "bold")).pack(anchor="w")
        value_lbl = tk.Label(card, text=value, bg=BG_PANEL, fg=value_color,
                              font=(FONT_FAMILY, 16, "bold"))
        value_lbl.pack(anchor="w", pady=(2, 0))
        return value_lbl

    # ------------------------------------------------------------------
    # EVENT HANDLERS
    # ------------------------------------------------------------------
    def _on_size_change(self, val):
        self.size_value_lbl.config(text=str(val))
        if not self.sorting:
            self.array_size = int(val)
            self.generate_array()

    def _on_speed_change(self, val):
        v = int(val)
        # map slider 1..100 -> delay 60ms..0ms (higher slider = faster = lower delay)
        self.speed = max(0, int((100 - v) * 0.6))
        label = "Very Slow"
        if v > 80:
            label = "Very Fast"
        elif v > 60:
            label = "Fast"
        elif v > 35:
            label = "Medium"
        elif v > 15:
            label = "Slow"
        self.speed_value_lbl.config(text=label)

    # ------------------------------------------------------------------
    # ARRAY + DRAWING
    # ------------------------------------------------------------------
    def generate_array(self):
        if self.sorting:
            return
        self.array = [random.randint(20, 400) for _ in range(self.array_size)]
        self.comparisons = 0
        self.swaps = 0
        self._update_stats(status="Idle")
        self.draw_array()

    def draw_array(self, highlight=None):
        self.canvas.delete("all")
        highlight = highlight or {}

        c_width = self.canvas.winfo_width() or 800
        c_height = self.canvas.winfo_height() or 460
        n = len(self.array)
        if n == 0:
            return

        max_val = max(self.array) if self.array else 1
        gap = 2 if n <= 80 else 1
        bar_width = max((c_width - gap * n) / n, 1)

        for i, value in enumerate(self.array):
            x0 = i * (bar_width + gap)
            x1 = x0 + bar_width
            bar_h = (value / max_val) * (c_height - 20)
            y1 = c_height - 10
            y0 = y1 - bar_h

            if i in highlight:
                color = highlight[i]
            else:
                t = value / max_val
                color = lerp_color(BAR_LOW, BAR_HIGH, t)

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        self.root.update_idletasks()

    def _update_stats(self, status=None):
        self.stat_comparisons.config(text=f"{self.comparisons:,}")
        self.stat_swaps.config(text=f"{self.swaps:,}")
        if self.start_time is not None and self.sorting:
            elapsed = time.time() - self.start_time
            self.stat_time.config(text=f"{elapsed:.2f}s")
        if status:
            self.stat_status.config(text=status)

    # ------------------------------------------------------------------
    # CONTROL
    # ------------------------------------------------------------------
    def start_sorting(self):
        if self.sorting:
            return
        self.sorting = True
        self.comparisons = 0
        self.swaps = 0
        self.start_time = time.time()

        self.sort_btn.set_disabled(True)
        self.sort_btn.text = "Sorting..."
        self.sort_btn._draw(ACCENT)
        self.generate_btn.set_disabled(True)
        self.size_slider.config(state=tk.DISABLED)

        algo = self.algo_var.get()
        self._update_stats(status=f"Running {algo}")

        algorithms = {
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": lambda: self.merge_sort(0, len(self.array) - 1),
            "Quick Sort": lambda: self.quick_sort(0, len(self.array) - 1),
        }
        algorithms[algo]()

        self.draw_array(highlight={i: COLOR_SORTED for i in range(len(self.array))})
        self._update_stats(status="Sorted ✓")

        self.sorting = False
        self.sort_btn.set_disabled(False)
        self.sort_btn.text = "▶  Start Sorting"
        self.sort_btn._draw(ACCENT)
        self.generate_btn.set_disabled(False)
        self.size_slider.config(state=tk.NORMAL)

    def _delay(self):
        if self.speed > 0:
            time.sleep(self.speed / 1000)
        self._update_stats()

    # ------------------------------------------------------------------
    # ALGORITHMS
    # ------------------------------------------------------------------
    def bubble_sort(self):
        arr = self.array
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparisons += 1
                self.draw_array({j: COLOR_COMPARE, j + 1: COLOR_COMPARE})
                self._delay()
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    self.draw_array({j: COLOR_SWAP, j + 1: COLOR_SWAP})
                    self._delay()

    def selection_sort(self):
        arr = self.array
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.comparisons += 1
                self.draw_array({min_idx: COLOR_SWAP, j: COLOR_COMPARE})
                self._delay()
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self.swaps += 1

    def insertion_sort(self):
        arr = self.array
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                self.comparisons += 1
                arr[j + 1] = arr[j]
                self.swaps += 1
                self.draw_array({j: COLOR_COMPARE, j + 1: COLOR_SWAP})
                self._delay()
                j -= 1
            arr[j + 1] = key
            self.draw_array({j + 1: COLOR_SWAP})
            self._delay()

    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self._merge(left, mid, right)

    def _merge(self, left, mid, right):
        arr = self.array
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]

        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            self.comparisons += 1
            self.draw_array({k: COLOR_COMPARE})
            self._delay()
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            self.swaps += 1
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
            self.swaps += 1
            self.draw_array({k - 1: COLOR_SWAP})
            self._delay()

        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
            self.swaps += 1
            self.draw_array({k - 1: COLOR_SWAP})
            self._delay()

    def quick_sort(self, low, high):
        if low < high:
            pi = self._partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def _partition(self, low, high):
        arr = self.array
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            self.draw_array({j: COLOR_COMPARE, high: COLOR_PIVOT})
            self._delay()
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swaps += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swaps += 1
        return i + 1


def main():
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
