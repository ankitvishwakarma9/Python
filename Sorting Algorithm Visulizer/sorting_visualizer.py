"""
Sorting Algorithm Visualizer
-----------------------------
A Python + Tkinter desktop app that visually demonstrates how popular
sorting algorithms work, bar by bar, comparison by comparison.

Author: <Your Name>
Tech stack: Python 3, Tkinter (standard library only — no extra installs needed)

Algorithms included:
    - Bubble Sort
    - Selection Sort
    - Insertion Sort
    - Merge Sort
    - Quick Sort

Run:
    python sorting_visualizer.py
"""

import random
import time
import tkinter as tk
from tkinter import ttk


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.array = []
        self.array_size = 50
        self.speed = 50          # lower = faster
        self.sorting = False

        self._build_controls()
        self._build_canvas()
        self.generate_array()

    # ---------------------------------------------------------------
    # UI SETUP
    # ---------------------------------------------------------------
    def _build_controls(self):
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(control_frame, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        self.algo_var = tk.StringVar(value="Bubble Sort")
        algo_menu = ttk.Combobox(
            control_frame,
            textvariable=self.algo_var,
            values=[
                "Bubble Sort",
                "Selection Sort",
                "Insertion Sort",
                "Merge Sort",
                "Quick Sort",
            ],
            state="readonly",
            width=15,
        )
        algo_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Array Size:").pack(side=tk.LEFT, padx=5)
        self.size_slider = tk.Scale(
            control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
            command=self._on_size_change
        )
        self.size_slider.set(self.array_size)
        self.size_slider.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=5)
        self.speed_slider = tk.Scale(
            control_frame, from_=1, to=100, orient=tk.HORIZONTAL,
            command=self._on_speed_change
        )
        self.speed_slider.set(100 - self.speed)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Generate New Array",
                  command=self.generate_array).pack(side=tk.LEFT, padx=10)

        self.sort_btn = tk.Button(control_frame, text="Start Sorting",
                                   bg="#4CAF50", fg="white",
                                   command=self.start_sorting)
        self.sort_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Ready", anchor="w")
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=10)

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", height=480)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _on_size_change(self, val):
        if not self.sorting:
            self.array_size = int(val)
            self.generate_array()

    def _on_speed_change(self, val):
        self.speed = 100 - int(val)

    # ---------------------------------------------------------------
    # ARRAY + DRAWING
    # ---------------------------------------------------------------
    def generate_array(self):
        if self.sorting:
            return
        self.array = [random.randint(10, 400) for _ in range(self.array_size)]
        self.draw_array()
        self.status_label.config(text="New array generated. Ready to sort.")

    def draw_array(self, highlight=None):
        self.canvas.delete("all")
        highlight = highlight or {}
        c_width = int(self.canvas["width"]) if self.canvas["width"] else 880
        c_width = self.canvas.winfo_width() or 880
        c_height = self.canvas.winfo_height() or 480

        n = len(self.array)
        bar_width = c_width / n

        for i, value in enumerate(self.array):
            x0 = i * bar_width
            y0 = c_height - value
            x1 = x0 + bar_width - 2
            y1 = c_height

            color = "#4A90D9"           # default bar color
            if i in highlight:
                color = highlight[i]    # e.g. "red" for compare, "green" for sorted

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        self.root.update_idletasks()

    # ---------------------------------------------------------------
    # CONTROL
    # ---------------------------------------------------------------
    def start_sorting(self):
        if self.sorting:
            return
        self.sorting = True
        self.sort_btn.config(state=tk.DISABLED)
        self.size_slider.config(state=tk.DISABLED)
        algo = self.algo_var.get()
        self.status_label.config(text=f"Sorting using {algo}...")

        algorithms = {
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": lambda: self.merge_sort(0, len(self.array) - 1),
            "Quick Sort": lambda: self.quick_sort(0, len(self.array) - 1),
        }
        algorithms[algo]()

        self.draw_array(highlight={i: "#2ECC71" for i in range(len(self.array))})
        self.status_label.config(text=f"{algo} complete! ({len(self.array)} elements)")
        self.sorting = False
        self.sort_btn.config(state=tk.NORMAL)
        self.size_slider.config(state=tk.NORMAL)

    def _delay(self):
        time.sleep(self.speed / 1000)

    # ---------------------------------------------------------------
    # ALGORITHMS
    # ---------------------------------------------------------------
    def bubble_sort(self):
        arr = self.array
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.draw_array({j: "red", j + 1: "red"})
                self._delay()
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.draw_array({j: "orange", j + 1: "orange"})
                    self._delay()

    def selection_sort(self):
        arr = self.array
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.draw_array({min_idx: "orange", j: "red"})
                self._delay()
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    def insertion_sort(self):
        arr = self.array
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                self.draw_array({j: "red", j + 1: "orange"})
                self._delay()
                j -= 1
            arr[j + 1] = key
            self.draw_array({j + 1: "orange"})
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
            self.draw_array({k: "red"})
            self._delay()
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
            self.draw_array({k - 1: "orange"})
            self._delay()

        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
            self.draw_array({k - 1: "orange"})
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
            self.draw_array({j: "red", high: "purple"})
            self._delay()
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


def main():
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
