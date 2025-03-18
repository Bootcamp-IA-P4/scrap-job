import psycopg2
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from db.connection import connect_to_database
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

def get_db():
    conn = connect_to_database()
    try:
        yield conn
    finally:
        conn.close()

@app.get("/api/companies")
def get_companies(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    cursor.close()
    return companies

@app.get("/api/companies/{CIF}")
def get_company(CIF: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM companies WHERE CIF = %s", (CIF,))
    company = cursor.fetchone()
    cursor.close()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get("/")
def read_root():
    return {"message": "Welcome to the EBITDA Tracker API!"}