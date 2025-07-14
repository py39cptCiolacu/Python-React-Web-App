# ✈️ Aircraft Parts Management – Tech Exercise

This is a desktop-style full-stack application built using **Flask**, **React**, and **PyWebView**. The app allows users to upload Excel files containing data on aircrafts, parts, and materials, and then performs automatic correlation and allows modifications through a clean, React-based interface.

---

## ⚙️ Features

- 📤 Upload Excel files for:
  - Aircrafts
  - Parts
  - Materials

- 🔗 Automatic linking between aircrafts, parts, and materials
- ✏️ Modify uploaded data directly from the interface
- 📊 Display structured views for easier navigation
- 🖥️ Runs as a native-like desktop application using `pywebview`
- 🧠 Database interactions via SQLAlchemy
- 🧬 Alembic-based schema migrations

---

## 🧱 Tech Stack

### Backend
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [pandas](https://pandas.pydata.org/) – Excel parsing
- [pywebview](https://pywebview.flowrl.com/) – Desktop wrapper

### Frontend
- [React](https://reactjs.org/)
- CSS / Tailwind 

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/py39cptCiolacu/tech_exercise.git
cd Python-React-Web-App

### 2. Install dependencies

```bash
pip install -r requiements.txt

### 3. Create and populate db

```back
python /back/utils/populate_db.py

### 4. Open frontend

```bash
cd /front
npm run dev


### 5. Start the application

```bash
python run_application.py

