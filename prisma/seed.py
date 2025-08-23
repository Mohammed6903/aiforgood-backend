import os
import bcrypt
from prisma import Prisma
import asyncio

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

async def main():
    db = Prisma()
    await db.connect()

    # Create users for all roles
    donor = await db.user.create(
        data={
            'name': 'Donor User',
            'email': 'donor@example.com',
            'phone': '1234567890',
            'city': 'CityA',
            'state': 'StateA',
            'country': 'CountryA',
            'role': 'DONOR',
            'password': hash_password("donor123"),
        }
    )
    patient = await db.user.create(
        data={
            'name': 'Patient User',
            'email': 'patient@example.com',
            'phone': '2345678901',
            'city': 'CityB',
            'state': 'StateB',
            'country': 'CountryB',
            'role': 'PATIENT',
            'password': hash_password("patient123"),
        }
    )
    volunteer = await db.user.create(
        data={
            'name': 'Volunteer User',
            'email': 'volunteer@example.com',
            'phone': '3456789012',
            'city': 'CityC',
            'state': 'StateC',
            'country': 'CountryC',
            'role': 'VOLUNTEER',
            'password': hash_password("volunteer123"),
        }
    )

    # Create related records for each role
    await db.donor.create(
        data={
            'user_id': donor.id,
            'blood_type': 'A+',
        }
    )
    await db.patient.create(
        data={
            'user_id': patient.id,
            'blood_group': 'B+',
            'age': 30,
            'gender': 'M',
        }
    )
    await db.volunteer.create(
        data={
            'user_id': volunteer.id,
            'activities': [],
        }
    )
    print("Seeding complete!")

    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
