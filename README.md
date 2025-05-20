
# Lab Exception Tracking Portal

This Flask-based web application allows labs to manage device exception submissions, track their status, and import updated data via CSV. It also includes admin tools for managing exceptions and data import.

---

## 🚀 Features

- Import labs and computers from a CSV file
- Track exception status per device (Pending, Submitted, Needs Info, Complete)
- Labs can edit their own submissions unless status is "Complete"
- Bulk actions: Submit, Delete, Reset Justification (with warning)
- Admin panel for importing new/revised exception lists
- Bootstrap 5-based responsive UI
- Admin import supports overwrite, merge-update, retain, and revert modes
- Merge conflict resolution for duplicate device entries
- Conflict resolution interface allows side-by-side review and choice of preferred data

---

## 📁 Project Structure

```
.
├── app.py                  # Flask app with all routes and logic
├── etp.db                  # SQLite database file (auto-created)
├── templates/              # HTML templates (Bootstrap 5)
│   ├── base.html
│   ├── index.html
│   ├── lab.html
│   ├── edit_computer.html
│   ├── import_csv.html
│   └── conflicts.html
├── static/                 # (Optional) Custom CSS/JS if needed
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image config
├── docker-compose.yml      # Docker Compose service config
└── data/
    └── exceptions_sample.csv  # Example import data
```

---

## 📦 Setup Instructions

### ✅ Requirements

- Docker & Docker Compose OR
- Python 3.10+ and pip (for manual install)

### 🐳 Run via Docker Compose

```bash
docker compose up --build
```

Then open [http://localhost:8000](http://localhost:8000)

### 🦪 Manual Run (Local Python)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open [http://localhost:8000](http://localhost:8000)

---

## 📤 CSV Import Format

Upload a `.csv` file with the following columns:

- `Lab` (lab name)
- `ComputerName` (device name)
- `Owner` (optional)
- `Justification` (optional)

Example:

```
Lab,ComputerName,Owner,Justification
Lab A,PC001,alice@example.com,Needed for specialized software
Lab A,PC002,bob@example.com,
Lab B,PC101,,Long-term scientific workload
```

When importing, admins can choose how to handle existing data:

- **Overwrite**: Replace existing records completely.
- **Merge-Update**: Update existing records with new values from CSV.
- **Retain**: Keep existing records unchanged.
- **Revert**: Rollback to a previously saved state before import.

If a duplicate `ComputerName` is detected during import, admins can:

- Review changes side-by-side
- Accept updates field-by-field
- Resolve conflicts by choosing which version to keep

The app creates a staging area for potential conflicts and displays them on a dedicated conflict resolution page. Admins can:

- Keep the existing database version
- Accept the staged import version
- Apply selected changes per row

All unresolved conflicts remain in the staging area until an admin reviews them.

---

## 🔐 Notes

- Devices marked as **Complete** are locked and cannot be edited.
- Admin import does not overwrite existing devices unless the chosen strategy allows it.
- Bulk actions prompt for confirmation on destructive changes (delete/reset).
- Conflict resolution must be completed before data is finalized.

---

## 🗄 To Do / Next Steps

- Add admin login system
- Year-based submission scoping (archiving)

---

## 📬 Support

Questions or bugs? Open an issue or contact your project administrator.
