# 🔢 Sorting Algorithm Visualizer

A desktop application built with **Python** and **Tkinter** that visually demonstrates how classic sorting algorithms work in real time — bar by bar, comparison by comparison.

Built as a B.Tech final year mini-project to strengthen understanding of algorithm complexity and visualization.

---

## 📌 Features

- Visualizes 5 popular sorting algorithms:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Merge Sort
  - Quick Sort
- Adjustable **array size** (10–100 elements)
- Adjustable **sorting speed**
- Randomized array generation with one click
- Live bar-chart animation with color-coded comparisons and swaps
- Built entirely with Python's standard library — **no external dependencies**

---

## 🖥️ Demo

Bars are compared (red), swapped (orange), and turn green once the array is fully sorted.

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
**Your Name**
B.Tech (Final Year)
[LinkedIn](#) • [GitHub](#)

---

## 📄 License
This project is licensed under the MIT License — feel free to use it for learning purposes.
