from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.connection import get_db, engine
from database.models import Base ,User, Spin, Payment
from api.roulette import spin_wheel
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

class SpinRequest(BaseModel):
    user_id: int
    payment_id: str

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/spin")
async def do_spin(data: SpinRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Payment).where(
            Payment.telegram_charge_id == data.payment_id,
            Payment.user_id == data.user_id,
            Payment.status == "completed"
        )
    )
    payment = result.scalar_one_or_none()
    
    if not payment:
        raise HTTPException(400, "Платёж не найден")
    
    payment.status = "used"
    
    spin_result = spin_wheel()
    
    await db.execute(
        update(User)
        .where(User.id == data.user_id)
        .values(
            stars_balance=User.stars_balance + spin_result["prize_stars"],
            total_won=User.total_won + spin_result["prize_stars"],
        )
    )
    
    spin = Spin(
        user_id=data.user_id,
        prize_stars=spin_result["prize_stars"],
        segment_index=spin_result["segment_index"],
        telegram_payment_id=data.payment_id,
    )
    db.add(spin)
    await db.commit()
    
    return spin_result

@app.post("/payment/success")
async def payment_success(
    charge_id: str, user_id: int, amount: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        db.add(User(id=user_id))
    
    payment = Payment(
        user_id=user_id,
        telegram_charge_id=charge_id,
        amount=amount,
        status="completed"
    )
    db.add(payment)
    await db.commit()
    return {"ok": True}