from io import BytesIO
from pathlib import Path
from unittest import TestCase

import pandas as pd

from service import service_stock
import pytest

class Test(TestCase):
    BASE_DIR = Path(__file__).resolve().parents[1]
    #this is the ideal path file with add the required rows, heads and its values
    path_file = BASE_DIR / "mockFiles" / "2025_12_24_11_38_01_tovars_MAQUILA - BOTURINI.xls"

    def test_upload_file(self):

        stock = service_stock.upload_file(self.path_file.read_bytes())
        assert (stock[0]["Artículo"] == "BASE MDF KIT MEZCALERO")
        assert (stock[0]["Código de barras"] == "483914272323")
        assert (stock[0]["Tags"] == "BASES MDF")


    def test_upload_file_raises_key_error_when_missing_column(self):
        path_file = self.BASE_DIR / "mockFiles" / "código_de_barras_missing_column.xls"
        with pytest.raises(KeyError) as exc:
            service_stock.upload_file(path_file.read_bytes())

        assert "Missing Código de barras columns" in str(exc.value)


    def test_upload_file_parse_barcode_to_string_when_read_excel_file(self):

        stock = service_stock.upload_file(self.path_file.read_bytes())

        assert (isinstance(stock[0]["Código de barras"], str))
        assert (stock[0]["Código de barras"] != "")

    def test_upload_file_remove_row_when_read_excel_file(self):

        stock = service_stock.upload_file(self.path_file.read_bytes())
        df = pd.DataFrame(stock)
        assert not df.isnull().any().any()

    def test_upload_file_normalizes_barcode_format(self):
        df = pd.DataFrame(
            [
                {
                    "Artículo": "ITEM 1",
                    "Código de barras": "00123-45 6",
                    "Tags": "TAG",
                }
            ]
        )

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        stock = service_stock.upload_file(buffer.getvalue())

        assert stock[0]["Código de barras"] == "00123456"

    def test_upload_file_skips_rows_with_empty_barcode(self):
        df = pd.DataFrame(
            [
                {
                    "Artículo": "VALID ITEM",
                    "Código de barras": "123456",
                    "Tags": "TAG",
                },
                {
                    "Artículo": "INVALID ITEM",
                    "Código de barras": None,
                    "Tags": "TAG",
                },
            ]
        )

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        stock = service_stock.upload_file(buffer.getvalue())

        assert len(stock) == 1
        assert stock[0]["Artículo"] == "VALID ITEM"
