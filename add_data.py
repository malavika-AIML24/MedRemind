from backend.database import SessionLocal
from backend import models

def inject_more_data():
    db = SessionLocal()
    
    # 1. New Unique Doctors (Batch 2)
    new_doctors = [
        models.User(username="dr_khan", role="doctor"),
        models.User(username="dr_taylor", role="doctor")
    ]
    
    # 2. New Unique Staff (Batch 2)
    new_staff = [
        models.User(username="nurse_emily", role="staff"),
        models.User(username="ward_boy_sam", role="staff")
    ]
    
    # 3. New Patients (Patients don't have a UNIQUE constraint on names, but let's add new ones)
    new_patients = [
        models.Patient(full_name="Ravi Varma", age=50),
        models.Patient(full_name="Diana Prince", age=35),
        models.Patient(full_name="Tony Stark", age=48)
    ]

    try:
        db.add_all(new_doctors + new_staff + new_patients)
        db.commit()
        print("✅ Success! New batch of medical staff and patients added.")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    inject_more_data()