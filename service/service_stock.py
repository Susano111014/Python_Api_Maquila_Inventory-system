from io import BytesIO
import re
from typing import Any

import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator

REQUIRED_COLUMNS = ["Artículo", "Código de barras", "Tags"]


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


def upload_file(content: bytes) -> list[dict[str, Any]]:
    df = pd.read_excel(BytesIO(content))

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        if not missing == "Tags":
            raise KeyError(f"Missing {', '.join(missing)} columns")

    df = df[REQUIRED_COLUMNS]

    validated_rows: list[dict[str, Any]] = []
    for row in df.itertuples(index=False, name=None):
        row_map = dict(zip(REQUIRED_COLUMNS, row))
        payload = {
            "articulo": row_map.get("Artículo"),
            "codigo_barras": row_map.get("Código de barras"),
            "tags": row_map.get("Tags"),
        }

        try:
            dto = StockRowDTO.model_validate(payload)
        except ValidationError:
            continue

        validated_rows.append(
            {
                "Artículo": dto.articulo,
                "Código de barras": dto.codigo_barras,
                "Tags": dto.tags,
            }
        )

    return validated_rows
