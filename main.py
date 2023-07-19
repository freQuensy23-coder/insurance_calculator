import datetime
from _decimal import Decimal
from typing import Optional

import os

import uvicorn
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
import loguru

from Exceptions import RateDoNotEstablished
from PriceCalculator import PriceCalculator
from database.models import Rate
from pydantic_models.rate import Rate as Rate_pydantic

app = FastAPI()
calculator = PriceCalculator()
log = loguru.logger
log.add("file.log", format="{time} {level} {message}", level="INFO", rotation="1 MB", compression="zip")


@app.get("/calculate_cost")
async def calculate_cost(cargo_type: str, cost: str, date: Optional[str] = None):
    try:
        return {"cost": await calculator.calculate_insurance_cost(cost, cargo_type, delivery_date=date)}
    except RateDoNotEstablished as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.post('/set_rates')
async def set_rates(rates: list[Rate_pydantic]):
    log.info("Setting rates")

    warnings = []
    for rate in rates:
        rate_decimal = Decimal(rate.rate)
        log.debug(f"Rate {rate} with rate {rate_decimal}")
        await Rate.update_or_create(date=rate.date, cargo_type=rate.cargo_type, defaults={'rate': rate_decimal})

        if rate.date < datetime.date.today():
            warnings.append(f'Rate for [{rate}] is outdated')
            log.warning(f'Rate for [{rate}] is outdated')

    log.info("Rates set")
    return {'status': 'ok', 'warnings': warnings}


@app.get("/rates")
async def get_rates(day: datetime.date = None):
    log.info(f"Getting rates for {day}")
    day = day or datetime.date.today()
    rates = await Rate.filter(date=day).all()
    return {"status": "ok", "result": rates}


register_tortoise(
    app,
    db_url=f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    modules={'models': ['database.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
