from _decimal import Decimal

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise

from Exceptions import RateDoNotEstablished
from PriceCalculator import PriceCalculator
from database.models import Rate
from pydantic_models.rate import Rate as Rate_pydantic

app = FastAPI()
calculator = PriceCalculator()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/calculate_cost")
async def calculate_cost(cargo_type: str, cost: str):
    try:
        return {"cost": await calculator.calculate_insurance_cost(cost, cargo_type)}
    except RateDoNotEstablished as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.post('/set_rates')
async def set_rates(rates: list[Rate_pydantic]):
    for rate in rates:
        rate_decimal = Decimal(rate.rate)
        await Rate.get_or_create(date=rate.date, cargo_type=rate.cargo_type, rate=rate_decimal)
    return {'status': 'ok'}



register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['database.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
