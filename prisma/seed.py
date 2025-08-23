import os
import bcrypt
from prisma import Prisma
import asyncio
from datetime import datetime

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

async def main():
    db = Prisma()
    await db.connect()

    try:
        # Create a location using raw SQL for PostGIS
        location_result = await db.query_raw("""
            INSERT INTO "Location" (name, coords)
            VALUES ($1, ST_GeomFromText($2, 4326))
            RETURNING id, name
        """, 'Central Hospital', 'POINT(-74.0060 40.7128)')
        
        location_id = location_result[0]['id']
        print(f"Created location with PostGIS: {location_id}")

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
        print(f"Created donor user: {donor.id}")

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
        print(f"Created patient user: {patient.id}")

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
        print(f"Created volunteer user: {volunteer.id}")

        # Create related records for each role
        donor_rec = await db.donor.create(
            data={
                'user_id': donor.id,
                'blood_type': 'A+',
                'location_id': location_id,
            }
        )
        print(f"Created donor record: {donor_rec.id}")

        patient_rec = await db.patient.create(
            data={
                'user_id': patient.id,
                'blood_group': 'B+',
                'age': 30,
                'gender': 'M',
            }
        )
        print(f"Created patient record: {patient_rec.id}")

        volunteer_rec = await db.volunteer.create(
            data={
                'user_id': volunteer.id,
                'activities': ['Blood Drive'],
                'assigned_region': 'North Zone',
            }
        )
        print(f"Created volunteer record: {volunteer_rec.id}")

        # Create a donation
        donation = await db.donation.create(
            data={
                'donor_id': donor_rec.id,
                'quantity': 1,
                'date': datetime.fromisoformat('2025-08-01T10:00:00+00:00'),
                'blood_type': 'A+',
                'notes': 'First donation',
                'city': 'CityA',
                'district': 'District1',
                'state': 'StateA',
                'location_id': location_id,
            }
        )
        print(f"Created donation: {donation.id}")

        # Create a blood request
        blood_request = await db.bloodrequest.create(
            data={
                'requester_id': patient.id,
                'blood_type': 'A+',
                'urgency': 'Urgent',
                'status': 'Pending',
                'location_id': location_id,
                'matched_donor': donor_rec.id,
            }
        )
        print(f"Created blood request: {blood_request.id}")

        # Create a badge for donor
        badge = await db.badge.create(
            data={
                'name': 'First Donation',
                'description': 'Awarded for first blood donation',
                'user_id': donor.id,
            }
        )
        print(f"Created badge: {badge.id}")

        # Create leaderboard entry
        leaderboard = await db.leaderboardentry.create(
            data={
                'user_id': donor.id,
                'rank': 1,
                'score': 100.0,
            }
        )
        print(f"Created leaderboard entry: {leaderboard.id}")

        # Create engagement
        engagement = await db.engagement.create(
            data={
                'user_id': donor.id,
                'engagement_score': 75.5,
                'activity_log': ['Donated blood', 'Received badge'],
            }
        )
        print(f"Created engagement: {engagement.id}")

        print("Seeding complete with PostGIS support!")

        # Example: Query nearby locations using PostGIS
        nearby = await db.query_raw("""
            SELECT id, name, ST_AsText(coords) as coords_text,
                   ST_Distance(coords, ST_GeomFromText('POINT(-74.0050 40.7120)', 4326)) as distance
            FROM "Location"
            WHERE ST_DWithin(coords, ST_GeomFromText('POINT(-74.0050 40.7120)', 4326), 0.01)
            ORDER BY distance
        """)
        print(f"Found {len(nearby)} nearby locations")

    except Exception as e:
        print(f"Error during seeding: {e}")
        raise
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())