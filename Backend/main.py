from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ml_components import parse_resume, predict_missing_skills
from database import save_to_db

app = FastAPI()

class Resume(BaseModel):
    name: str
    text: str

class JobDescription(BaseModel):
    title: str
    description: str

@app.get("/")
def root():
    return {"message": "Welcome to AI-Driven Inclusive Assessment Tools for Skill Ecosystem!"}

@app.post("/parse_resume/")
def parse_resume_endpoint(resume: Resume):
    try:
        parsed_data = parse_resume(resume.text)
        save_to_db("resumes", {"name": resume.name, "parsed_data": parsed_data})
        return {"status": "success", "parsed_data": parsed_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_skills/")
def predict_skills_endpoint(data: dict):
    try:
        prediction = predict_missing_skills(data)
        return {"status": "success", "predicted_skills": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
