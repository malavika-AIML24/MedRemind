from backend.database import SessionLocal, engine
from backend import models

# Initialize database
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

def seed_hospital():
    # Clear existing to avoid duplicates (optional)
    db.query(models.User).delete()
    db.query(models.Patient).delete()

    # 1. Doctors
    doctors = [
        models.User(username="dr_sharma", role="doctor"),
        models.User(username="dr_peters", role="doctor"),
        models.User(username="dr_aditi", role="doctor")
    ]
    # 2. Staff/Nurses
    staff = [
        models.User(username="nurse_claire", role="staff"),
        models.User(username="nurse_rahul", role="staff"),
        models.User(username="admin_vicky", role="staff")
    ]
    # 3. Patients
    patients = [
        models.Patient(full_name="Arjun Mehta", age=45),
        models.Patient(full_name="Sarah Connor", age=32),
        models.Patient(full_name="Liam Neeson", age=67),
        models.Patient(full_name="Priyanka Chopra", age=29),
        models.Patient(full_name="Bruce Wayne", age=40)
    ]

    db.add_all(doctors + staff + patients)
    db.commit()
    print("🏥 Hospital Database Seeded Successfully!")

if __name__ == "__main__":
    seed_hospital()