# Company Management Dashboard

A full-stack application for managing company information, including web scraping, API backend, and interactive frontend.

# Features

- **Web Scraping**: Automatically collects company data (EBITDA, CIF) from public sources
- **RESTful API**: FastAPI backend with CRUD operations for company management
- **Interactive Dashboard**: Frontend interface to view, add, search, and delete companies
- **Database**: PostgreSQL storage for company information
- **Automated Setup**: Docker and Poetry for easy deployment

## Technologies

**Backend**:
- Python 3.12
- FastAPI (REST API)
- PostgreSQL (Database)
- Psycopg2 (Database adapter)
- Pydantic (Data validation)
- Selenium (Web scraping)

**Frontend**:
- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap 5 (Styling)

**DevOps**:
- Docker (Containerization)
- Poetry (Dependency management)
- pytest (Testing)

## Project Structure
```bash
.
├── api/
│ ├── crud.py
│ ├── main.py
│ └── schemas.py
├── db/
│ ├── connection.py
│ ├── creation.py
│ └── load_companies.py
│ └── tests/
├── scrap_job/
│ ├── scrap.py
│ └── companies.csv
│ └── tests/
├── static/
│ ├── index.html
│ ├── script.js
│ └── style.css
├── Dockerfile
├── entry_point.sh
├── pyproject.toml
└── poetry.lock
```
## Installation

### Prerequisites
- Docker
- Python 3.12
- Poetry

### Docker Setup

**1. Clone the repository:**
   ```bash
   git clone https://github.com/Bootcamp-IA-P4/scrap-job.git
   ``` 

   ```bash
   cd scrap-job
   ``` 

**2. Set up environment variables:**
   ```bash
   nano  ~/.bashrc
   ``` 

   ```bash
   source ~/.bashrc
   ``` 

**3. Install Poetry**
```bash
pip install poetry
``` 


**4. Run with Docker**
```bash
sudo docker run -e DB_USER=postgres -e DB_HOST=localhost -e DB_PORT=5432 -e DB_NAME=Companies -e DB_PASSWORD=yourpassword -p 3000:8000 -p 5432:5432 --name scrap --rm scrap
```

### Local Setup
**1. Clone the repository:**
   ```bash
   git clone https://github.com/Bootcamp-IA-P4/scrap-job.git
   ``` 

   ```bash
   cd scrap-job
   ```

**2. Setup .env**
```bash
mkdir .env
```

```bash
DB_NAME=Companies
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

**3. Install Poetry**
```bash
pip install poetry
``` 

**4. Run Scrap**
```bash
python scrap_job/scrap.py
``` 

**4. Run Create Database**
```bash
python db/creation.py
```

**5. Run table creation**
```bash
python db/load_companies.py
```

**6. Start the FastAPI application**
```bash
uvicorn api.main:app --reload
```

### Testing
**1. Run tests with**
```bash
pytest
```

## Next Steps
1. Automate nightly scraping
2. Local LLM Integration
3. Confidential Data Analysis
