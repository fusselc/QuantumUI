# INSTALL.md

## Prerequisites
- Python 3.11 or higher
- Node.js 20 or higher
- Git

---

## Local Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/QuantumUI.git
cd QuantumUI
```

### 2. Configure Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 3. Configure Frontend
In a new terminal:
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
Navigate to `http://localhost:5173`.

---

## Running Tests
```bash
# Run backend test suite
pytest

# Run frontend build & test
cd frontend
npm run build
npm run test
```
