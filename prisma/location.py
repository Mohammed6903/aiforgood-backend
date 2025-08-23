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
        """, 'Fairfield by mariott', 'POINT(17.424238904940754 78.34649335509613)')
        
        location_id = location_result[0]['id']
        print(f"Created location with PostGIS: {location_id}")
    except Exception as e:
        print(f"Error during seeding: {e}")
        raise
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())