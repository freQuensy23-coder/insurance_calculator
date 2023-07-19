import datetime
from _decimal import Decimal
from typing import Optional

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
        return {"cost": await calculator.calculate_insurance_cost(cost, cargo_type, date=date)}
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


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['database.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
