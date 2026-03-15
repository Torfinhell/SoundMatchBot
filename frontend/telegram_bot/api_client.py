import httpx
from config import BACKEND_URL

async def register(tg_id, username):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BACKEND_URL}/users/register", json={"telegram_id": str(tg_id), "username": username})
        return res.json()['user_id']

async def get_polls():
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{BACKEND_URL}/polls/active")).json()

async def submit_ans(poll_id, user_id, answers):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BACKEND_URL}/polls/{poll_id}/submit", json={"user_id": user_id, "answers": answers})

async def get_recs(user_id):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{BACKEND_URL}/recommendations/{user_id}")).json()

async def claim_admin(user_id, pwd):
    async with httpx.AsyncClient() as client:
        return (await client.post(f"{BACKEND_URL}/admin/claim", json={"user_id": user_id, "password": pwd})).json()