import os
from . import crud, schemas
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/companies/", response_model=list[schemas.Company])
def read_companies():
    companies = crud.get_companies()
    if companies:
        return [
            schemas.Company(
                company_name=c[0],
                ebitda_source=c[1],
                cif_source=c[2],
                cif=c[3],
                ebitda_2023=c[4]
            )
            for c in companies
        ]
    return []


@app.get("/companies/{cif}", response_model=schemas.Company)
def read_company(cif: str):
    company = crud.get_company_by_cif(cif)
    if company:
        return schemas.Company(
            company_name=company[0],
            ebitda_source=company[1],
            cif_source=company[2],
            cif=company[3],
            ebitda_2023=company[4]
        )
    raise HTTPException(status_code=404, detail="Company not found")


@app.delete("/companies/{cif}")
def delete_company(cif: str):
    if crud.delete_company_by_cif(cif):
        return {"message": f"Company with CIF {cif} deleted successfully"}
    raise HTTPException(status_code=404, detail="Company not found")


@app.put("/companies/{cif}", response_model=schemas.Company)
def update_company(cif: str, company: schemas.Company):
    if crud.update_company_by_cif(
        cif=cif,
        company_name=company.company_name,
        ebitda_source=company.ebitda_source,
        cif_source=company.cif_source,
        ebitda_2023=company.ebitda_2023
    ):
        return company
    raise HTTPException(status_code=404, detail="Company not found")


@app.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.Company):
    print("Received payload:", company.dict())
    try:
        if crud.create_company(
            company_name=company.company_name,
            ebitda_source=company.ebitda_source,
            cif_source=company.cif_source,
            cif=company.cif,
            ebitda_2023=company.ebitda_2023
        ):
            return company
        else:
            raise HTTPException(status_code=400, detail="Company could not be created")
    except Exception as error:
        print(f"Error in create_company endpoint: {error}")
        raise HTTPException(status_code=400, detail=str(error))