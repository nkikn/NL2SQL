from    backend.db.database import SessionLocal
from backend.models.sqlalchemy import Customer

def insert_sample_data():
    db = SessionLocal()
    try:
        customers = [
            Customer(id=1, name="Marc-André ter Stegen", email="terstegen@example.com", age=23),
            Customer(id=3, name="Gerard Piqué", email="pique@example.com", age=28),
            Customer(id=4, name="Ivan Rakitić", email="rakitic@example.com", age=27),
            Customer(id=5, name="Sergio Busquets", email="busquets@example.com", age=27),
            Customer(id=6, name="Xavi", email="xavi@example.com", age=32),
            Customer(id=8, name="Andrés Iniesta", email="iniesta@example.com", age=31),
            Customer(id=9, name="Luis Suárez", email="suarez@example.com", age=28),
            Customer(id=10, name="Lionel Messi", email="messi@example.com", age=28),
            Customer(id=11, name="Neymar Jr.", email="neymar@example.com", age=23),
            Customer(id=13, name="Claudio Bravo", email="bravo@example.com", age=32),
            Customer(id=14, name="Javier Mascherano", email="mascherano@example.com", age=31),
            Customer(id=15, name="Marc Bartra", email="bartra@example.com", age=24),
            Customer(id=18, name="Jordi Alba", email="alba@example.com", age=26),
            Customer(id=19, name="Sandro Ramírez", email="sandro@example.com", age=20),
            Customer(id=20, name="Sergi Roberto", email="roberto@example.com", age=23),
            Customer(id=21, name="Adriano Correia", email="adriano@example.com", age=30),
            Customer(id=22, name="Dani Alves", email="dalves@example.com", age=32),
            Customer(id=23, name="Thomas Vermaelen", email="vermaelen@example.com", age=29),
            Customer(id=24, name="Douglas Pereira", email="douglas@example.com", age=25),
            Customer(id=25, name="Jordi Masip", email="masip@example.com", age=26),
        ]
        for cust_data in customers:
            existing = db.query(Customer).filter(Customer.id == cust_data.id).first()
            if not existing:
                db.add(cust_data)
        db.commit()
    finally:
        db.close()
