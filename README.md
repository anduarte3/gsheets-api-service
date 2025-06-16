# Google Sheets ✈️ Flight API Service

This Python script fetches live flight data from the [AviationStack API](https://aviationstack.com/) and logs it into a Google Sheet using the `gspread` library.

## What it does

- Pulls flight info (date, status, airports, delays, etc.)
- Converts delay times into readable format (e.g. "2h 10m")
- Automatically appends data to a Google Sheet
- Keeps it clean with environment variables

## Setup

1. Clone the repo
2. Create a `.env` file (see `.env.example`) with:

AVIATION_API_KEY=your_api_key
GOOGLE_CREDENTIALS_PATH=path/to/your/credentials.json

3. Install dependencies:
   pip install -r requirements.txt

4. Run it:
   python gsheet_script.py

## Notes

- Requires a service account JSON from Google Sheets API.
- Uses `.env` to keep secrets out of the script.
- Rate-limited API – don’t hammer it.

## Optional ideas

- Convert to FastAPI for a backend service
- Add date filters or parameters
- Style the sheet formatting (colors, headers, etc.)

---
