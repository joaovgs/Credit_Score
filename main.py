from enum import Enum
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Carregar o conjunto de dados
try:
    dataset = pd.read_csv('Car_Insurance_Claim.csv')
except FileNotFoundError:
    raise RuntimeError("Arquivo CSV não encontrado.")

class DrivingExperience(str, Enum):
    opcaoDE0 = ""
    opcaoDE1 = "0-9y"
    opcaoDE2 = "10-19y"
    opcaoDE3 = "20-29y"
    opcaoDE4 = "30y+"

class Gender(str, Enum):
    gender_default = ""
    male = "male"
    female = "female"

class Age(str, Enum):
    opcaoIdade0 = ""
    opcaoIdade1 = "16-25"
    opcaoIdade2 = "26-39"
    opcaoIdade3 = "40-64"
    opcaoIdade4 = "65+"

class Education(str, Enum):
    education_default = ""
    none = "none"
    university = "university"
    high_school = "high school"

class Income(str, Enum):
    income_default = ""
    poverty = "poverty"
    working_class = "working class"
    middle_class = "middle class"
    upper_class = "upper class"

class VehicleType(str, Enum):
    vehicletype_default = ""
    sedan = "sedan"
    sports_car = "sports car"

class VehicleYear(str, Enum):
    vehicle_year_default = ""
    after = "after 2015"
    before = "before 2015"


class PersonData(BaseModel):
    age: Age
    gender: Gender
    driving_experience: DrivingExperience
    education: Education
    income: Income
    vehicle_year: VehicleYear
    vehicle_type: VehicleType
    annual_mileage: float

@app.post("/credit_score")
async def calculate_credit_score(
    age: Age = Form(...),
    gender: Gender = Form(...),
    driving_experience: DrivingExperience = Form(...),
    education: Education = Form(...),
    income: Income = Form(...),
    vehicle_year: VehicleYear = Form(...),
    vehicle_type: VehicleType = Form(...),
    annual_mileage: float = Form(...),
):
    # Criar um objeto PersonData com os dados fornecidos
    data = PersonData(
        age=age,
        gender=gender,
        driving_experience=driving_experience,
        education=education,
        income=income,
        vehicle_year=vehicle_year,
        vehicle_type=vehicle_type,
        annual_mileage=annual_mileage
    )

    # Filtrar o conjunto de dados com base nos dados fornecidos na solicitação
    filtered_data = dataset
    for field, value in data.dict().items():
        filtered_data = filtered_data[filtered_data[field.upper()] == value]

    # Verificar se há pelo menos um registro correspondente
    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Nenhum registro correspondente encontrado")

    # Calcular o CREDIT_SCORE com base nos dados filtrados
    credit_score = filtered_data['CREDIT_SCORE'].mean()

    # Retornar o CREDIT_SCORE
    return {"credit_score": credit_score}