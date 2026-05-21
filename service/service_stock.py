from io import BytesIO
from typing import Any

import pandas as pd
from pydantic import ValidationError

from dto_validators.stock_dto import StockRowDTO

REQUIRED_COLUMNS = ["Artículo", "Código de barras"]
OPTIONAL_COLUMNS = ["Tags"]

def upload_file(content: bytes) -> list[dict[str, Any]]:
    df = pd.read_excel(BytesIO(content))

    required_missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    optional_missing = [col for col in OPTIONAL_COLUMNS if col not in df.columns]

    if required_missing:
        raise KeyError(f"Missing {', '.join(required_missing)} columns")

    for col in optional_missing:
        df[col] = None

    selected_columns = REQUIRED_COLUMNS + OPTIONAL_COLUMNS
    df = df[selected_columns]

    validated_rows: list[dict[str, Any]] = []
    for row in df.itertuples(index=False, name=None):
        row_map = dict(zip(selected_columns, row))
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
