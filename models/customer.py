from pydantic import BaseModel, EmailStr

class Customer(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    institution: str
    course: str
    year: str
    projectType: str
    timeline: str
    projectDescription: str
