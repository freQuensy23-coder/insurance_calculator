from tortoise.models import Model
from tortoise import fields


class Rate(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    cargo_type = fields.CharField(max_length=50)
    rate = fields.DecimalField(decimal_places=3, max_digits=3)

    class Meta:
        table = "rates"
