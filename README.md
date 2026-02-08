# Parana Database Reader (Python)

A Python CLI application that reads and explores data from a real-world SQLite database (`parana.db`), designed as a portfolio project to demonstrate clean code structure, database access, and command-line interaction.

---

## 📌 Project Overview

This project connects to an existing SQLite database and allows users to browse and query shopper data through an interactive command-line menu.

It follows a **clean separation of concerns**:
- `db.py` → database access & SQL logic
- `app.py` → CLI menu, user input, and output formatting

The database schema represents a realistic e-commerce system (shoppers, products, orders, baskets).

---

---

## ⚙️ Requirements

- Python **3.10+**
- SQLite (included with Python)
- No external dependencies

---

## ▶️ How to Run

Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/python-db-reader.git
cd python-db-reader
