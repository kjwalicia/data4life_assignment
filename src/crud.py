from sqlalchemy.orm import Session
import models, schemas


# Patients
def get_all_patients(db:Session):
    return db.query(models.Patient).order_by(models.Patient.id.asc()).all()

def get_patient_by_id(patient_id:str, db:Session):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()

def get_patient_by_name(patient_name:str, db:Session):
    return db.query(models.Patient).filter(models.Patient.patient_name == patient_name).first()


# Doctors
def get_all_doctors(db:Session):
    return db.query(models.Doctor).order_by(models.Doctor.id.asc()).all()

def get_doctor_appointments_by_date(doctor_id:str, 
                            appointment_date:str, 
                            db:Session):
    
    return db.query(models.Appointment
        ).filter(models.Appointment.doctor_id == doctor_id,
                 models.Appointment.appointment_date == appointment_date,
        ).order_by(models.Appointment.appointment_datetime.asc()).all()

def get_doctor_by_id(doctor_id:str, db:Session):
    return db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()

def get_doctor_by_name(doctor_name:str, db:Session):
    return db.query(models.Doctor).filter(models.Doctor.doctor_name == doctor_name).first()


# Appointments
def get_all_appointments(db:Session):
    return db.query(models.Appointment).order_by(models.Appointment.id.asc()).all()

def check_appointment_availability(doctor_id:str, appointment_datetime:str, db:Session):
    return db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_datetime == appointment_datetime,
        models.Appointment.appointment_status == 'Confirmed').first()

def create_appointment(patient_id:str, doctor_id:str, appointment_datetime:str, db:Session):
    no_of_appointments = len(db.query(models.Appointment).all())

    new_appointment = models.Appointment(
        appointment_id = 'A'+str(no_of_appointments+1),
        patient_id = patient_id,
        doctor_id = doctor_id,
        appointment_date = appointment_datetime.split(' ')[0],
        appointment_datetime = appointment_datetime,
        appointment_status = 'Confirmed')

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

def get_appointment_by_id(appointment_id:str, db:Session):
    return db.query(models.Appointment).filter(
        models.Appointment.appointment_id == appointment_id).first()

def cancel_appointment(appointment_id_to_cancel:str, db:Session):
    appointment_to_cancel = db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id_to_cancel).first()
    appointment_to_cancel.appointment_status = 'Cancelled'
    db.commit()
    db.refresh(appointment_to_cancel)
    return appointment_to_cancel
    