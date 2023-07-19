import datetime
from _decimal import Decimal
from datetime import date
from typing import Optional

from database.models import Rate
from loguru import logger
from Exceptions import RateDoNotEstablished


@staticmethod
class PriceCalculator:
    """Отвечает за расчет цен в данном приложении"""
    async def calculate_insurance_cost(self, base_cost: str, cargo_type: str, delivery_date: Optional[datetime.date] = None) -> Decimal:
        """Calculate insurance cost
        :param delivery_date: Optional parameter - date of delivery. If not specified - today
        :param base_cost: base cost of cargo
        :param cargo_type: type of cargo. (Ex. Glass, Other)
        :return insurance_cost: Decimal. insurance cost in same currency. We use Decimal because of precision.
        :raises RateDoNotEstablished: if we have no rate for today
        """
        logger.info(f"Calculating insurance cost for cargo with {base_cost} and {cargo_type}")
        delivery_date = delivery_date or date.today()
        rate_value = await Rate.filter(date=delivery_date, cargo_type=cargo_type).first()
        if rate_value:
            rate = rate_value.rate
            logger.info(f"Rate for {delivery_date} and {cargo_type} is {rate}")
            return rate * Decimal(base_cost)
        else:
            logger.warning(f"Rate for {delivery_date} and {cargo_type} is not established")
            raise RateDoNotEstablished

