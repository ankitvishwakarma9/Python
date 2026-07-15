# 🔢 Sorting Algorithm Visualizer

A desktop application built with **Python** and **Tkinter** that visually demonstrates how classic sorting algorithms work in real time — bar by bar, comparison by comparison.

Built as a B.Tech final year mini-project to strengthen understanding of algorithm complexity and visualization.

---

## 📌 Features

- 🎨 **Modern dark-themed UI** — custom rounded buttons, card-based layout, gradient-colored bars
- Visualizes 5 popular sorting algorithms:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Merge Sort
  - Quick Sort
- Adjustable **array size** (10–150 elements) via a styled slider
- Adjustable **sorting speed** (Very Slow → Very Fast)
- Live **stats dashboard**: comparisons, swaps/writes, elapsed time, and current status
- Color-coded legend (Comparing / Swapping / Pivot / Sorted)
- Randomized array generation with one click
- Height-based gradient bar coloring (blue → violet) for a cleaner visual read
- Built entirely with Python's standard library — **no external dependencies**

---

## 🖥️ Demo

Bars are colored by value on a blue→violet gradient. During sorting: **red** = comparing, **amber** = swapping/writing, **teal** = pivot (Quick Sort), and the whole array turns **green** once fully sorted.

---

## ⚙️ Tech Stack

- **Language:** Python 3
- **GUI Library:** Tkinter (comes bundled with Python)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed
- Tkinter (usually pre-installed with Python; on Linux you may need `sudo apt-get install python3-tk`)

### Run the project
```bash
git clone https://github.com/<your-username>/sorting-visualizer.git
cd sorting-visualizer
python sorting_visualizer.py
```

---

## 📂 Project Structure
```
sorting-visualizer/
│
├── sorting_visualizer.py   # Main application file
├── README.md                # Project documentation
└── .gitignore                # Ignored files for git
```

---

## 🧠 Algorithms & Time Complexity

| Algorithm       | Best Case  | Average Case | Worst Case | Space |
|-----------------|-----------|---------------|------------|-------|
| Bubble Sort     | O(n)      | O(n²)         | O(n²)      | O(1)  |
| Selection Sort  | O(n²)     | O(n²)         | O(n²)      | O(1)  |
| Insertion Sort  | O(n)      | O(n²)         | O(n²)      | O(1)  |
| Merge Sort      | O(n log n)| O(n log n)    | O(n log n) | O(n)  |
| Quick Sort      | O(n log n)| O(n log n)    | O(n²)      | O(log n) |

---

## 🔮 Future Improvements
- Add Heap Sort and Radix Sort
- Add step counter / comparison counter on screen
- Add a "Pause/Resume" button
- Convert to a web app using Pygame or JavaScript/Canvas

---

## 👤 Author
Ankit Vishwakarma
B.Tech (Final Year)
[LinkedIn](#) • [GitHub](#)

---

## 📄 License
This project is licensed under the MIT License — feel free to use it for learning purposes.
