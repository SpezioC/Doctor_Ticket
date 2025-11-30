# Doctor Ticket – Smart Ticket Classification System

## Overview
Doctor Ticket is a small showcase project designed to simulate the workflow of an automated ticket-processing system.
It performs three main tasks:
- acquiring maintenance tickets from an API (mock or real)
- cleaning and analyzing ticket text
- storing and managing structured tickets inside a database
This project is not meant to be a production system, but a clear demonstration of text classification, scoring rules, and basic database integration.

## Features
- text normalization and small typo-correction
- automatic keyword detection
- ticket scoring based on predefined dictionaries
- priority assignment
- database insertion and retrieval
- simple ticket management through SQL queries
- mock API for local testing

## How It Works
1. Connect to a mock API (or a real server).
2. Fetch raw ticket descriptions.
3. Normalize the text and correct minor misspellings.
4. Extract known problems and compute a score.
5. Assign a priority level.
6. Store the ticket in an SQLite database.
7. Allow database queries for ticket management.

## 🗂 Project Structure
```
Doctor_Ticket/
│
├── core/               # main ticket and DB logic
│   ├── ticket.py
│   └── sqldb.py
│
├── definition/         # dictionaries and scoring rules
│   ├── models.py
│   └── scores_rules.py
│
├── connection_to/      # server/database connectors
│   ├── to_db.py
│   └── to_web.py
│
├── mock_api/           # fake API for local testing
│   ├── mock_apy.py
│   └── tickets_data.json
│
├── tests/              # unittest test suite
│
└── main.py             # entry point
```

## 🔧 Installation
- Python 3.10+
- SQLite (bundled with Python)
- Optional: a real API endpoint if not using the mock API

Instal the project:
```
git clone <your-repo-url>
cd Doctor_Ticket
```

## Usage
```python main.py```
This will:
- fetch tickets from the mock API (or from the real server if configured)
- process and clean the text
- compute score and priority
- insert the results into the database
Processed tickets can then be inspected directly inside the SQLite database.

## 🧪 Tests
python -m unittest discover -s tests -t .

## 📝 Notes
Planned improvements:
- more robust problem classification
- better handling of technicians' decisions
- stronger negative-sentiment analysis
- data visualization for ticket statistics
- optional web dashboard

## 📄 License
Released under the MIT License.