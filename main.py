from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import settings_route, scrapper_route
import uvicorn

app = FastAPI(
    title="GMAIL SCRAPPER API",
    description="API for scraping attachments from Gmail",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(settings_route.router, prefix="/email/settings", tags=["SETTINGS"])
app.include_router(scrapper_route.router, prefix="/email/scrapper", tags=["SCRAPPER"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)