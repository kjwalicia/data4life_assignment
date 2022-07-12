from ast import Str
from datetime import datetime
from typing import List, Union, Optional
from pydantic import BaseModel
import typing



# Create Models
class DoctorAppointment(BaseModel):
    doctor_id: str
    appointment_day: int
    appointment_month: int
    appointment_year: int


class CreateAppointment(BaseModel):
    doctor_id: str
    patient_id: str
    appointment_day: int
    appointment_month: int
    appointment_year: int
    appointment_hour: int
        

class CreateDoctor(BaseModel):
    doctor_name: str
        

class CreatePatient(BaseModel):
    patient_name: str
    patient_age: int
    patient_gender: str


# Response Models
class Appointment(BaseModel):
    appointment_id: str
    doctor_id: str
    patient_id: str
    appointment_date: str
    appointment_datetime: str
    appointment_status: str

    class Config:
        orm_mode = True
        

class Doctor(CreateDoctor):
    doctor_id: str
    
    class Config:
        orm_mode = True
        

class Patient(CreatePatient):
    patient_id: str
    
    class Config:
        orm_mode = True