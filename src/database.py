from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

# this creates the SQLite engine
engine = create_engine('sqlite:///data4life.db', connect_args={"check_same_thread":False}, echo=True)

Base = declarative_base()

# This is how we have sessions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=False)



def setup_database():

    conn = sqlite3.connect('data4life.db')
    c = conn.cursor()
    
    with open('script.sql') as f:
        sql_script = f.read()
    
    c.executescript(sql_script)
    
    # for checking
    print('##### Loading Dummy Data #####')
    stg_raw = c.execute('''SELECT * FROM stg_raw''')
    for row in stg_raw:
        print(row)

    print('##### Loading Doctors Data #####')
    doctors = c.execute('''SELECT * FROM doctors''')
    for row in doctors:
        print(row)
     
    print('##### Loading Patients Data #####')
    patients = c.execute('''SELECT * FROM patients''')
    for row in patients:
        print(row)
        
    print('##### Loading Appointments Data #####')
    appointments = c.execute('''SELECT * FROM appointments''')
    for row in appointments:
        print(row)
    
    conn.close()
