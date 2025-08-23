# Placeholder for database session setup
from prisma import Prisma

prisma = Prisma()

async def get_db():
    if not prisma.is_connected():
        await prisma.connect()
    return prisma