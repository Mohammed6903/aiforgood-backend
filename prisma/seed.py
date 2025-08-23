import bcrypt
from prisma import Prisma
import asyncio

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

async def main():
    db = Prisma()
    await db.connect()

    try:
        # Helper: create a location and return its id
        async def create_location(name, lng, lat):
            loc_result = await db.query_raw(
                '''INSERT INTO "Location" (name, coords) VALUES ($1, ST_GeomFromText($2, 4326)) RETURNING id''',
                name, f'POINT({lng} {lat})'
            )
            return loc_result[0]['id']

        # Predefine some nearby locations (NYC area + Hyderabad)
        base_locs = [
            ("Central Hospital", -74.0060, 40.7128),
            ("East Clinic", -74.0050, 40.7130),
            ("West Center", -74.0070, 40.7125),
            ("North Point", -74.0065, 40.7135),
            ("South Health", -74.0062, 40.7120),
            ("Fairfield by Mariott", 17.42424, 78.34750)
        ]
        location_ids = []
        for name, lng, lat in base_locs:
            loc_id = await create_location(name, lng, lat)
            location_ids.append(loc_id)
            print(f"Created location: {name} (id={loc_id})")

        # ------------------ Donors (20 unique) ------------------
        blood_types = ["A+", "O-", "B+", "AB+", "O+", "A-", "B-", "AB-"]
        donors = []
        # Add 5 donors specifically at Fairfield by Mariott (last location in base_locs)
        fairfield_idx = len(location_ids) - 1
        for i in range(1, 6):
            user = await db.user.create(
                data={
                    'name': f"Donor Fairfield {i}",
                    'email': f"donor_fairfield{i}@example.com",
                    'phone': f"91000000{i:03d}",
                    'city': "Hyderabad",
                    'state': "Telangana",
                    'country': "India",
                    'role': "DONOR",
                    'password': hash_password("donor123"),
                }
            )
            donor_rec = await db.donor.create(
                data={
                    'user_id': user.id,
                    'blood_type': blood_types[i % len(blood_types)],
                    'location_id': location_ids[fairfield_idx],
                }
            )
            donors.append(donor_rec)
            print(f"Created donor: {user.name} at Fairfield by Mariott")

        # Add the rest of the donors as before
        for i in range(6, 21):
            loc_idx = (i - 1) // 3 % len(location_ids)
            user = await db.user.create(
                data={
                    'name': f"Donor User {i}",
                    'email': f"donor{i}@example.com",
                    'phone': f"90000000{i:03d}",
                    'city': f"City{i}",
                    'state': f"State{i}",
                    'country': "CountryA",
                    'role': "DONOR",
                    'password': hash_password("donor123"),
                }
            )
            donor_rec = await db.donor.create(
                data={
                    'user_id': user.id,
                    'blood_type': blood_types[i % len(blood_types)],
                    'location_id': location_ids[loc_idx],
                }
            )
            donors.append(donor_rec)
            print(f"Created donor: {user.name} at location {loc_idx+1}")

        # ------------------ Patients (20 unique, no location) ------------------
        blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        for i in range(1, 21):
            user = await db.user.create(
                data={
                    'name': f"Patient User {i}",
                    'email': f"patient{i}@example.com",
                    'phone': f"80000000{i:03d}",
                    'city': f"PatientCity{i}",
                    'state': f"PatientState{i}",
                    'country': "CountryB",
                    'role': "PATIENT",
                    'password': hash_password("patient123"),
                }
            )
            patient_rec = await db.patient.create(
                data={
                    'user_id': user.id,
                    'blood_group': blood_groups[i % len(blood_groups)],
                    'age': 20 + i,
                    'gender': "M" if i % 2 == 0 else "F",
                }
            )
            print(f"Created patient: {user.name}")

        # ------------------ Volunteers (20 unique, no location) ------------------
        activities_list = [
            ["Blood Drive"],
            ["Awareness Campaign"],
            ["Donor Support"],
            ["Emergency Help"],
            ["Coordination"],
        ]
        for i in range(1, 21):
            user = await db.user.create(
                data={
                    'name': f"Volunteer User {i}",
                    'email': f"volunteer{i}@example.com",
                    'phone': f"70000000{i:03d}",
                    'city': f"VolunteerCity{i}",
                    'state': f"VolunteerState{i}",
                    'country': "CountryC",
                    'role': "VOLUNTEER",
                    'password': hash_password("volunteer123"),
                }
            )
            volunteer_rec = await db.volunteer.create(
                data={
                    'user_id': user.id,
                    'activities': activities_list[i % len(activities_list)],
                    'assigned_region': f"Region-{i}",
                }
            )
            print(f"Created volunteer: {user.name}")

        print("✅ Seeding complete with donors linked to locations; patients and volunteers without location.")

    except Exception as e:
        print(f"Error during seeding: {e}")
        raise
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
