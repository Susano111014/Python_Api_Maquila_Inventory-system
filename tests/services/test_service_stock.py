from io import BytesIO
from pathlib import Path
from unittest import TestCase
import pandas as pd
from service import service_stock


class Test(TestCase):
    def test_upload_file(self):
        base_dir = Path(__file__).resolve().parents[1]
        path_file = base_dir / "mockFiles" / "2025_12_24_11_38_01_tovars_MAQUILA - BOTURINI.xls"

        stock = service_stock.upload_file(path_file.read_bytes())
        assert (stock[0]["Artículo"] == "BASE MDF KIT MEZCALERO")
        assert (stock[0]["Código de barras"] == 483914272323)
        assert (stock[0]["Tags"] == "BASES MDF")
