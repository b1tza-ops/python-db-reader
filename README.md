# Parana Database Reader (Python)

A Python-based command-line application for exploring and querying data from a real-world SQLite database (`parana.db`).
This project is built as a **portfolio piece** to demonstrate clean code structure, database interaction, and scalable design thinking.

---

## 📌 Project Overview

The Parana Database Reader is a CLI tool that connects to an existing SQLite database and allows users to browse and inspect shopper-related data through an interactive menu.

The project focuses on:

* clean separation of concerns
* readable and maintainable Python code
* safe, parameterized SQL queries
* realistic database structures (e-commerce style schema)

---

## 🧱 Project Structure

```
python-db-reader/
├── app.py        # CLI application (menu, input handling, output formatting)
├── db.py         # Database access layer (SQL queries only)
├── data/
│   └── parana.db # Public SQLite database (sample / non-sensitive data)
├── README.md
└── .gitignore
```

---

## ⚙️ Requirements

* Python **3.10+**
* SQLite (included with Python standard library)
* No third-party dependencies required

---

## ▶️ How to Run

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/python-db-reader.git
cd python-db-reader
```

Run the application:

```bash
python app.py
```

---

## 🧭 Application Features

### Interactive CLI Menu

```
1) List shoppers
2) Search shoppers (name/email)
3) View shopper by ID
4) Exit
```

### Implemented Functionality

* List shoppers with configurable limits
* Search shoppers by name or email (case-insensitive)
* View full shopper details using a unique ID
* Read-only access to the database
* Parameterized SQL queries to prevent injection
* Clear separation between database logic and application logic

---

## 🗄️ Database Information

* Database engine: **SQLite**
* Database file: `data/parana.db`
* Schema type: E-commerce style

Primary table used:

* `shoppers`

Example fields:

* `shopper_id`
* `shopper_first_name`
* `shopper_surname`
* `shopper_email_address`
* `date_of_birth`
* `gender`
* `date_joined`

The database included in this repository contains **sample / non-sensitive data only** and is provided for demonstration purposes.

---

## 🧠 Design Principles

* **Separation of concerns**

  * `db.py` contains only database access and SQL
  * `app.py` handles CLI logic and user interaction

* **Readability over cleverness**
  Code is intentionally explicit and easy to follow.

* **Scalable foundation**
  The structure allows easy extension with new features, queries, or interfaces.

---

## 🛣️ Project Roadmap

### Phase 1 – Core Database Exploration ✅ (Completed)

* [x] Connect to an existing SQLite database
* [x] Implement read-only database queries
* [x] Display shopper data in a CLI
* [x] Add an interactive menu system
* [x] Separate database logic from application logic
* [x] Document the project clearly

---

### Phase 2 – Enhanced Data Access 🔜

* [ ] Join tables (shoppers → orders → products)
* [ ] Display shopper order history
* [ ] Add advanced filters (gender, join date, email domain)
* [ ] Add pagination support for large datasets

---

### Phase 3 – Data Export & Reporting 🔜

* [ ] Export query results to CSV
* [ ] Generate basic analytics (counts, summaries)
* [ ] Create simple text-based reports
* [ ] Optional JSON export for integration use cases

---

### Phase 4 – CLI & Usability Improvements 🔜

* [ ] Add command-line arguments (`--limit`, `--search`)
* [ ] Improve error handling and input validation
* [ ] Add help / usage screen
* [ ] Optional colored CLI output

---

### Phase 5 – Code Quality & Testing 🔜

* [ ] Add unit tests for database functions
* [ ] Introduce a test database / fixtures
* [ ] Improve inline documentation
* [ ] Apply formatting and linting standards

---

### Phase 6 – Scalability & Extensions 🔜

* [ ] PostgreSQL implementation of the database layer
* [ ] Configuration via environment variables
* [ ] REST API version (Flask or FastAPI)
* [ ] Dockerized deployment

---

## 👤 Author

**Paul Scripcariu**
Python • Databases • Backend Fundamentals

---

## 📄 License

This project is provided for educational and portfolio purposes.
