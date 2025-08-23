from app.db.session import get_db, Prisma
from fastapi import Depends
from app.schemas.donor import Donor
from app.schemas.blood_request import BloodRequest
from app.schemas.location import Location
from typing import List, Optional, Dict
import datetime
from datetime import timedelta

async def get_user(user_id: int, db: Prisma =Depends(get_db)):
    return await db.user.find_unique(where={"id": user_id})

async def create_user(data: dict, db: Prisma = Depends(get_db)):
    donor = Donor(**data)
    return await db.user.create(data=donor.model_dump())

async def get_user_by_email(email: str, db: Prisma = Depends(get_db)):
    return await db.user.find_unique(where={"email": email})

async def get_nearby_donors(
    lat: float, 
    lng: float, 
    radius: float = 5.0,
    blood_type: Optional[str] = None,
    max_results: int = 50,
    available_only: bool = True,
    db: Prisma = Depends(get_db)
) -> List[Dict]:
    """
    Find nearby blood donors using PostGIS geography functions and Prisma raw query.
    """
    base_query = """
    SELECT 
        d.id as donor_id,
        u.id as user_id,
        u.name,
        u.email,
        u.phone,
        u.city,
        u.state,
        u.country,
        d.blood_type,
        d.last_donation_date,
        d.total_donations,
        ST_Y(l.coords::geometry) as lat,
        ST_X(l.coords::geometry) as lng,
        l.name as location_name,
        -- Distance in meters (no rounding needed)
        ST_Distance(
            l.coords::geography,
            ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
        ) AS distance_meters,
        -- Distance in km with proper type casting for ROUND
        ROUND(
            (ST_Distance(
                l.coords::geography,
                ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
            ) / 1000.0)::NUMERIC, 2
        ) AS distance_km
    FROM "Donor" d
    JOIN "Location" l ON d.location_id = l.id
    JOIN "User" u ON d.user_id = u.id
    WHERE ST_DWithin(
        l.coords::geography,
        ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
        $3 * 1000  -- Convert km to meters
    )
    """

    conditions = []
    params = [lng, lat, radius]
    param_count = 3

    if blood_type:
        param_count += 1
        conditions.append(f"AND d.blood_type = ${param_count}")
        params.append(blood_type)

    if available_only:
        cutoff_date = datetime.datetime.now() - timedelta(days=56)
        param_count += 1
        conditions.append(f"AND (d.last_donation_date IS NULL OR d.last_donation_date <= TO_TIMESTAMP(${param_count}, 'YYYY-MM-DD HH24:MI:SS'))")
        params.append(cutoff_date.strftime('%Y-%m-%d %H:%M:%S'))

    # Add conditions to the base query
    if conditions:
        query = base_query + " " + " ".join(conditions)
    else:
        query = base_query

    # Add ORDER BY and LIMIT
    param_count += 1
    query += f"""
    ORDER BY distance_meters ASC
    LIMIT ${param_count}
    """
    params.append(max_results)

    def _is_donor_available(last_donation_date):
        if last_donation_date is None:
            return True
        days_since = (datetime.datetime.now() - last_donation_date).days
        return days_since >= 56

    def _days_since_last_donation(last_donation_date):
        if last_donation_date is None:
            return None
        return (datetime.datetime.now() - last_donation_date).days

    try:
        rows = await db.query_raw(query, *params)
        donors = []
        for row in rows:
            donor_data = {
                'donor_id': row['donor_id'],
                'user_id': row['user_id'],
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone'],
                'city': row['city'],
                'state': row['state'],
                'country': row['country'],
                'blood_type': row['blood_type'],
                'last_donation_date': row['last_donation_date'].isoformat() if row['last_donation_date'] else None,
                'total_donations': row['total_donations'],
                'location_name': row['location_name'],
                'distance_meters': float(row['distance_meters']),
                'distance_km': float(row['distance_km']),
                'is_available': _is_donor_available(row['last_donation_date']),
                'days_since_last_donation': _days_since_last_donation(row['last_donation_date']),
                'lat': float(row['lat']),
                'lng': float(row['lng'])
            }
            donors.append(donor_data)
        return donors
    except Exception as e:
        print(f"Error finding nearby donors: {e}")
        raise

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

async def get_faq(db: Prisma = Depends(get_db)):
    return await db.faq.find_many()