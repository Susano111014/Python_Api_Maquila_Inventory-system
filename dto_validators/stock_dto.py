import re
from typing import Any

import pandas as pd
from pydantic import BaseModel, field_validator


class StockRowDTO(BaseModel):
    articulo: str
    codigo_barras: str
    tags: str | None = None

    @field_validator("codigo_barras", mode="before")
    @classmethod
    def normalize_barcode(cls, value: Any) -> str:
        if pd.isna(value):
            raise ValueError("codigo_barras is empty")

        barcode = str(value).strip()
        if re.fullmatch(r"\d+\.0", barcode):
            barcode = barcode[:-2]

        barcode = barcode.replace(" ", "").replace("-", "")
        barcode = re.sub(r"\D", "", barcode)

        if not barcode:
            raise ValueError("codigo_barras is empty after normalization")

        return barcode
