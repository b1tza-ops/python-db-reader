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
python3 app.py


## 🛣️ Project Roadmap

This roadmap outlines the planned evolution of the project, focusing on clean architecture, incremental features, and best practices.

### Phase 1 – Core Database Exploration ✅ (Completed)
- [x] Connect to an existing SQLite database
- [x] Implement read-only queries
- [x] Display shopper data in CLI
- [x] Add interactive menu system
- [x] Separate database logic from application logic

---

### Phase 2 – Enhanced Data Access 🔜
- [ ] Add table joins (shoppers → orders → products)
- [ ] Display shopper order history
- [ ] Add filters (gender, date joined, email domain)
- [ ] Pagination support for large datasets

---

### Phase 3 – Data Export & Reporting 🔜
- [ ] Export query results to CSV
- [ ] Add summary statistics (total shoppers, gender split)
- [ ] Generate simple text-based reports
- [ ] Optional JSON export for API usage

---

### Phase 4 – Usability & CLI Improvements 🔜
- [ ] Add command-line arguments (`--limit`, `--search`)
- [ ] Improve input validation and error handling
- [ ] Add colored CLI output (optional)
- [ ] Add help / usage screen

---

### Phase 5 – Code Quality & Testing 🔜
- [ ] Add unit tests for database queries
- [ ] Introduce test database / fixtures
- [ ] Improve documentation and inline comments
- [ ] Enforce formatting and linting standards

---

### Phase 6 – Scalability & Extensions 🔜
- [ ] PostgreSQL version of the database layer
- [ ] Configuration via environment variables
- [ ] Web API version (Flask or FastAPI)
- [ ] Containerization with Docker
