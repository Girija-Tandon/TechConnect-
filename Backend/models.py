from pydantic import BaseModel

class Resume(BaseModel):
    name: str
    text: str

class JobDescription(BaseModel):
    title: str
    description: str
