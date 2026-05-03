from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

# Data Models for API
class LogEntry(BaseModel):
    patient_id: int
    medicine_name: str
    status: str

class VitalEntry(BaseModel):
    patient_id: int
    blood_pressure: str
    heart_rate: int

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/")
def root(): return {"status": "MedRemind API Active"}

# --- MEDICATION ROUTES ---
@app.post("/log-medication")
def create_log(entry: LogEntry, db: Session = Depends(get_db)):
    new_log = models.MedicationLog(patient_id=entry.patient_id, medicine_name=entry.medicine_name, status=entry.status)
    db.add(new_log); db.commit(); return {"message": "Success"}

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(models.MedicationLog).all()

@app.get("/adherence/{patient_id}")
def get_adherence(patient_id: int, db: Session = Depends(get_db)):
    logs = db.query(models.MedicationLog).filter(models.MedicationLog.patient_id == patient_id).all()
    if not logs: return {"rate": 0}
    taken = len([l for l in logs if l.status == "Taken"])
    return {"rate": round((taken / len(logs)) * 100, 1)}

# --- VITALS ROUTES ---
@app.post("/log-vitals")
def create_vital(entry: VitalEntry, db: Session = Depends(get_db)):
    new_vital = models.VitalRecord(patient_id=entry.patient_id, blood_pressure=entry.blood_pressure, heart_rate=entry.heart_rate)
    db.add(new_vital); db.commit(); return {"message": "Vitals Saved"}

@app.get("/patient-monitor")
def get_monitor(db: Session = Depends(get_db)):
    return db.query(models.VitalRecord).all()

@app.get("/vitals-trend/{patient_id}")
def get_vitals_trend(patient_id: int, db: Session = Depends(get_db)):
    vitals = db.query(models.VitalRecord).filter(models.VitalRecord.patient_id == patient_id).all()
    # Return as a list of dictionaries for the chart
    return [{"timestamp": v.timestamp, "heart_rate": v.heart_rate} for v in vitals]

@app.get("/users/{role}")
def get_users_by_role(role: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role == role).all()

@app.get("/patients")
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()

@app.get("/users/{role}")
def get_users_by_role(role: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role == role).all()

@app.get("/patients")
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()

@app.get("/users/{role}")
def get_users_by_role(role: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role == role).all()

@app.get("/patients")
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()