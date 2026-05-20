# Project Progress

## 2026-05-20

- Refactored `upload_file` in `service/service_stock.py` to validate inbound Excel rows with a Pydantic DTO.
- Added barcode normalization before mapping rows to output:
  - trims whitespace
  - removes Excel float suffix (`.0`)
  - removes spaces and hyphens
  - keeps digits only
- Added required-column guard for `Artículo`, `Código de barras`, and `Tags`.
- Updated behavior to skip invalid rows (for example, empty barcode) instead of failing the full import.
- Extended tests in `tests/services/test_service_stock.py` to cover:
  - missing required column
  - barcode normalization format
  - null checks with proper scalar assertion
  - skipping rows with empty barcode
- Noted test environment dependency gap: `pytest` and `openpyxl` are required in the active virtual environment to execute the test suite.
