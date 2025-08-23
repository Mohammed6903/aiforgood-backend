from prisma import Prisma

prisma: Prisma = Prisma()

async def get_db() -> Prisma:
    if not prisma.is_connected():
        await prisma.connect()
    return prisma