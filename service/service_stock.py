from io import BytesIO
import pandas as pd


def upload_file(content: bytes) -> dict:
    df = pd.read_excel(BytesIO(content))
    df = df.get(["Artículo", "Código de barras", "Tags"])
    stock_dict = df.to_dict("records")
    return stock_dict
