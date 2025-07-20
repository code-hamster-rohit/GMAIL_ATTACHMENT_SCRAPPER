# Gmail Scraper API

A FastAPI-based microservice for scraping attachments from Gmail accounts. This project allows you to configure search settings, list emails, fetch email bodies, and download attachments programmatically using the Gmail API.

---

## Features

- Save and load Gmail search settings
- List emails matching search criteria
- Retrieve email body and attachment metadata
- Download attachments from selected emails
- CORS enabled for easy frontend integration

---

## Getting Started

### Prerequisites

- Python 3.10+
- Gmail API credentials (`credentials.json` in `client_secret/`)
- Required Python packages (see `requirements.txt`)

### Installation

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd EMAIL_SCRAPPER
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Add Gmail API credentials**

   - Download your `credentials.json` from Google Cloud Console and place it in `client_secret/`.

4. **Run the API server**
   ```sh
   python main.py
   ```
   The API will be available at `http://localhost:8000`.

---

## API Endpoints

### Settings

- `POST /email/settings/save`  
  Save Gmail search settings.  
  **Body:**
  ```json
  {
    "user_email": "your@gmail.com",
    "search_email": "from@gmail.com",
    "date_from": "YYYY/MM/DD",
    "date_to": "YYYY/MM/DD",
    "search_query": "optional search string"
  }
  ```
- `GET /email/settings/load`  
  Load the current search settings.

### Scrapper

- `GET /email/scrapper/list`  
  List email IDs matching the saved settings.
- `POST /email/scrapper/get_body`  
  Get attachment metadata for a list of email IDs.  
  **Body:**
  ```json
  { "email_ids": ["id1", "id2"] }
  ```
- `POST /email/scrapper/get_attachments`  
  Download attachments for given email and attachment IDs.  
  **Body:**
  ```json
  {
    "email_ids": ["id1"],
    "attachment_ids": { "id1": [["att_id1"], ["filename1"]] }
  }
  ```

---

## How to Modify or Extend

- **Change search logic:**
  - Edit `routes/scrapper_route.py` to adjust how emails are filtered or queried.
- **Add new endpoints:**
  - Create new route files in `routes/` and include them in `main.py`.
- **Change data models:**
  - Update or add Pydantic models in `models/model.py`.
- **Authentication/Token logic:**
  - See `utils/access_token.py` for OAuth and token refresh logic.
- **Frontend integration:**
  - CORS is enabled for all origins by default. Adjust in `main.py` as needed.

---

## File Structure

```
main.py                  # FastAPI app entry point
routes/                  # API route definitions
  scrapper_route.py      # Email scraping endpoints
  settings_route.py      # Settings endpoints
models/                  # Pydantic models
utils/                   # Utility functions (OAuth, etc.)
client_secret/           # Place your Gmail API credentials here
requirements.txt         # Python dependencies
```

---

## Collaboration

I am open to collaboration, suggestions, and improvements! Feel free to open issues or submit pull requests. For any queries or to discuss features, please reach out.

---

## License

This project is provided as-is for educational and personal use. Please ensure you comply with Gmail API terms and privacy policies when using this tool.
