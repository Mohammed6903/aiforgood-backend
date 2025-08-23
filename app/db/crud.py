from app.db.session import get_db, Prisma
from fastapi import Depends
from app.schemas.donor import Donor
from app.schemas.blood_request import BloodRequest
from app.schemas.location import Location

async def get_user(user_id: int, db: Prisma =Depends(get_db)):
    return await db.user.find_unique(where={"id": user_id})

async def create_user(data: dict, db: Prisma = Depends(get_db)):
    donor = Donor(**data)
    return await db.user.create(data=donor.model_dump())

async def get_user_by_email(email: str, db: Prisma = Depends(get_db)):
    return await db.user.find_unique(where={"email": email})

async def get_nearby_donors(lng: float, lat: float, radius=10, db: Prisma = Depends(get_db)):
    donors = await db.query_raw('''
        SELECT d.id, u.name, u.email, u.phone,d.blood_type,
               ST_Distance(l.coords::geography,
                    ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography) AS distance
        FROM "Donor" d
        JOIN "Location" l ON d.location_id = l.id
        JOIN "User" u ON d.user_id = u.id
        WHERE ST_DWithin(
            l.coords::geography,
            ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
            $3 * 1000
        )
        ORDER BY distance ASC
    ''', lng, lat, radius)

    return donors

async def insert_location(data: dict, db: Prisma = Depends(get_db)):
    location = Location(**data)
    return await db.location.upsert(where={"id": location.id}, create=data, update=data)

async def create_blood_request(data: dict, db: Prisma = Depends(get_db)):
    blood_request = BloodRequest(**data)
    return await db.blood_request.create(data=blood_request.model_dump())

async def get_blood_request(request_id: int, db: Prisma = Depends(get_db)):
    return await db.blood_request.find_unique(where={"id": request_id})

async def get_blood_requests_by_user(user_id: int, db: Prisma = Depends(get_db)):
    return await db.blood_request.find_many(where={"requester_id": user_id})