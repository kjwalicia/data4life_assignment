from fastapi import Depends, FastAPI, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
import crud, models, schemas, os
from database import SessionLocal, engine, setup_database
from datetime import datetime

''' run command: uvicorn main:app --reload'''

if not os.path.exists('data4life.db'):
    setup_database()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/appointments/", response_model=list[schemas.Appointment])
def Q2_get_doctor_appointments(doctor_id, 
                            appointment_day:int,
                            appointment_month:int,
                            appointment_year:int,
                            db:Session=Depends(get_db)):
    
    '''Q2. Get all appointments for the given doctor & date'''
    db_doctor = crud.get_doctor_by_id(doctor_id, db)
    
    # if doctor does not exist
    if db_doctor is None:
        raise HTTPException(
            status_code=400, detail=f"This doctor does not exist!")
    
    # if date is invalid
    try:
        appointment_date = datetime(year=int(appointment_year),
                                    month=int(appointment_month), 
                                    day=int(appointment_day), 
                                    hour=0, 
                                    minute=0, 
                                    second=0, 
                                    microsecond=0)
    except ValueError:
        raise HTTPException(
                status_code=400, detail=f"Datetime is invalid!")
    else:
        dt_string = appointment_date.strftime('%Y-%m-%d')
    
    return crud.get_doctor_appointments_by_date(
        db_doctor.doctor_id, dt_string, db)



@app.post("/appointments/", response_model=schemas.Appointment)
def Q3_fix_appointment(patient_id:str,
                    doctor_id:str, 
                    appointment_day:int,
                    appointment_month:int, 
                    appointment_year:int,
                    appointment_hour:int, 
                    db: Session = Depends(get_db)):
    
    '''Q3. Fix appointment by patient, doctor and date & time'''

    # if patient does not exist
    db_patient = crud.get_patient_by_id(patient_id, db)
    if db_patient is None:
        raise HTTPException(
            status_code=400, detail=f"This patient does not exist!")

    # if doctor does not exist
    db_doctor = crud.get_doctor_by_id(doctor_id, db)
    if db_doctor is None:
        raise HTTPException(
            status_code=400, detail=f"This doctor does not exist!")

    # if datetime is invalid
    try:
        appointment_datetime = datetime(year=int(appointment_year),
                 month=int(appointment_month), 
                 day=int(appointment_day), 
                 hour=int(appointment_hour), 
                 minute=0, 
                 second=0, 
                 microsecond=0)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Datetime is invalid!")
    else:
        dt_string = appointment_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    # if timing is out of bounds i.e. timing is not between 9 to 3
    if int(appointment_hour) < 8 or int(appointment_hour) > 15:
        raise HTTPException(
            status_code=400, detail=f"Timing is out of working hours!")
    
    db_appointment = crud.check_appointment_availability(doctor_id, dt_string, db)
    
    if db_appointment:
        raise HTTPException(
            status_code=400, detail=f"This timeslot is not available for this doctor!")

    # create appointment
    return crud.create_appointment(patient_id, doctor_id, dt_string, db)



@app.put("/appointments/", response_model=schemas.Appointment)
def Q4_cancel_appointment(patient_id:str,
                       doctor_id:str,
                       appointment_day:int,
                       appointment_month:int, 
                       appointment_year:int,
                       appointment_hour:int,
                       db:Session=Depends(get_db)):
    
    '''Q4: Cancel appointment by patient, doctor and date & time'''
    
    # if patient does not exist
    db_patient = crud.get_patient_by_id(patient_id, db)
    if db_patient is None:
        raise HTTPException(
            status_code=400, detail=f"This patient does not exist!")

    # if doctor does not exist
    db_doctor = crud.get_doctor_by_id(doctor_id, db)
    if db_doctor is None:
        raise HTTPException(
            status_code=400, detail=f"This doctor does not exist!")

    # if date is false
    try:
        appointment_datetime = datetime(year=int(appointment_year),
                 month=int(appointment_month), 
                 day=int(appointment_day), 
                 hour=int(appointment_hour), 
                 minute=0, 
                 second=0, 
                 microsecond=0)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Datetime is invalid!")
    else:
        dt_string = appointment_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    # if timing is out of bounds i.e. timing is not between 9 to 3
    if int(appointment_hour) < 8 or int(appointment_hour) > 15:
        raise HTTPException(
            status_code=400, detail=f"Timing is out of working hours!")
    
    db_appointment = crud.check_appointment_availability(doctor_id, dt_string, db)
    
    # if there is no confirmed appointment
    if not db_appointment:
        raise HTTPException(
            status_code=400, detail=f"No appointment to cancel!")
    
    return crud.cancel_appointment(db_appointment.appointment_id, db)



@app.get("/")
def home():
    return {'Navigate To': 'http://127.0.0.1:8000/docs'}



@app.get("/patients", response_model=list[schemas.Patient])
def get_all_patients(db:Session=Depends(get_db)):
    return crud.get_all_patients(db)



@app.get("/doctors", response_model=list[schemas.Doctor])
def get_all_doctors(db:Session=Depends(get_db)):
    return crud.get_all_doctors(db)



@app.get("/appointments", response_model=list[schemas.Appointment])
def get_all_appointments(db:Session=Depends(get_db)):
    return crud.get_all_appointments(db)



@app.get("/doctors/doctor={doctor_name}", response_model=schemas.Doctor)
def get_doctor_by_name(doctor_name,
                       db:Session=Depends(get_db)):
    
    db_doctor = crud.get_doctor_by_name(doctor_name, db)
    
    if db_doctor is None:
        raise HTTPException(
            status_code=400, detail=f"Doctor named {doctor_name} does not exist!")
    return db_doctor



@app.get("/patients/patient={patient_name}", response_model=schemas.Patient)
def get_patient_by_name(patient_name,
                        db:Session=Depends(get_db)):
    
    db_patient = crud.get_patient_by_name(patient_name, db)
    
    if db_patient is None:
        raise HTTPException(
            status_code=400, detail=f"Patient named {patient_name} does not exist!")
    return db_patient
