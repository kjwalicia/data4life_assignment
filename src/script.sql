DROP TABLE IF EXISTS stg_raw;
CREATE TABLE IF NOT EXISTS stg_raw (
    doctor_id INTEGER NOT NULL,
    doctor_name TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    patient_age TEXT NOT NULL,
    patient_gender TEXT NOT NULL,
    appointment_id TEXT,
    appointment_datetime TEXT
);

DROP TABLE IF EXISTS doctors;
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    doctor_id TEXT NOT NULL UNIQUE,
    doctor_name TEXT NOT NULL
    --CHECK (doctor_id GLOB 'D[0-9]+')
);

DROP TABLE IF EXISTS patients;
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    patient_id TEXT NOT NULL UNIQUE,
    patient_name TEXT NOT NULL,
    patient_age INTEGER NOT NULL,
    patient_gender TEXT NOT NULL
    --CHECK (patient_id GLOB 'P[0-9]+'),
    --CHECK (patient_gender GLOB '^[MF]'),
    --CHECK (patient_age >= 0 AND patient_age <= 200)
);

DROP TABLE IF EXISTS appointments;
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    appointment_id TEXT NOT NULL UNIQUE,
    patient_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_datetime TEXT NOT NULL,
    appointment_status TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
    --CHECK (appointment_id GLOB 'A[0-9]+')
);

INSERT INTO stg_raw (doctor_id, doctor_name, patient_id, patient_name, patient_age, patient_gender, appointment_id, appointment_datetime) VALUES
    ('D1', 'D1Name', 'P1', 'P1Name', 12, 'M', 'A1', '08032018 09:00:00'),
    ('D1', 'D1Name', 'P1', 'P1Name', 12, 'M', 'A2', '08042018 10:00:00'),
    ('D1', 'D1Name', 'P2', 'P2Name', 22, 'F', 'A3', '08032018 10:00:00'),
    ('D1', 'D1Name', 'P1', 'P1Name', 12, 'M', 'A4', '08042018 11:00:00'),
    ('D2', 'D2Name', 'P1', 'P1Name', 12, 'M', 'A5', '18032018 08:00:00'),
    ('D2', 'D2Name', 'P1', 'P1Name', 12, 'M', 'A6', '18042018 09:00:00'),
    ('D2', 'D2Name', 'P3', 'P3Name', 32, 'M', 'A7', '18032018 09:00:00'),
    ('D2', 'D2Name', 'P3', 'P3Name', 32, 'M', 'A8', '18042018 10:00:00');


INSERT INTO doctors (doctor_id, doctor_name)
SELECT DISTINCT doctor_id, doctor_name
FROM stg_raw
ORDER BY doctor_id ASC;

INSERT INTO patients (patient_id, patient_name, patient_age, patient_gender)
SELECT DISTINCT patient_id, patient_name, patient_age, patient_gender
FROM stg_raw
ORDER BY patient_id ASC;

INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_datetime, appointment_status)
SELECT
    appointment_id,
	patient_id,
	doctor_id,
    -- datetime format should be YYYY-MM-DD HH:MM:SS.SSS
    substr(appointment_datetime,5,4) || '-' || substr(appointment_datetime,3,2) || '-' || substr(appointment_datetime,1,2),
    -- datetime format should be YYYY-MM-DD HH:MM:SS.SSS
    substr(appointment_datetime,5,4) || '-' || substr(appointment_datetime,3,2) || '-' || substr(appointment_datetime,1,2) || ' ' || substr(appointment_datetime,10,2) || ':00:00',
    'Confirmed'
FROM stg_raw
ORDER BY appointment_id;