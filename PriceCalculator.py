from _decimal import Decimal
from datetime import date
from database.models import Rate
from loguru import logger
from Exceptions import RateDoNotEstablished


@staticmethod
class PriceCalculator:
    """Отвечает за расчет цен в данном приложении"""
    async def calculate_insurance_cost(self, base_cost: str, cargo_type: str) -> Decimal:
        """Calculate insurance cost
        :param base_cost: base cost of cargo
        :param cargo_type: type of cargo. (Ex. Glass, Other)
        :return insurance_cost: Decimal. insurance cost in same currency. We use Decimal because of precision.
        :raises RateDoNotEstablished: if we have no rate for today
        """
        logger.info(f"Calculating insurance cost for cargo with {base_cost} and {cargo_type}")
        today = date.today()
        # Get current rate from database with cargo_type. Select only one
        rate_value = await Rate.filter(date=today, cargo_type=cargo_type).first()
        if rate_value:
            rate = rate_value.rate
            return rate * Decimal(base_cost)
        else:
            raise RateDoNotEstablished
        # If we have no rate for today, we get last rate


