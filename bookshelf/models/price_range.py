from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class PriceRange(BaseModel):
    min_price: Decimal = Field(ge=0)
    max_price: Decimal = Field(ge=0)

    @model_validator(mode="after")
    def _check(self) -> "PriceRange":
        if self.min_price > self.max_price:
            raise ValueError("min_price must be <= max_price")

        return self