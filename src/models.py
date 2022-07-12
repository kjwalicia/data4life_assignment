from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
import enum


class GenderEnum(str, enum.Enum):
    M = 'M'
    F = 'F'


class StatusEnum(str, enum.Enum):
    Confirmed = 'Confirmed'
    Cancelled = 'Cancelled'


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(String, unique=True, nullable=False, index=True)
    patient_name = Column(String, unique=True, nullable=False, index=True)
    patient_age = Column(Integer, nullable=False)
    patient_gender = Column(Enum(GenderEnum), nullable=False)

    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, nullable=False)
    doctor_id = Column(String, unique=True, nullable=False, index=True)
    doctor_name = Column(String, unique=True, nullable=False, index=True)

    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True) 
    appointment_id = Column(String, unique=True, nullable=False)
    patient_id = Column(String, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.doctor_id"), nullable=False)
    appointment_date = Column(String, nullable = False)
    appointment_datetime = Column(String, nullable=False)
    appointment_status = Column(Enum(StatusEnum), default='Confirmed', nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
