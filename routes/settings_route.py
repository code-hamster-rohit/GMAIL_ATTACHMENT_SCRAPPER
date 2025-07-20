from fastapi import APIRouter, HTTPException
from models.model import SettingsModel
import json, os

router = APIRouter()

@router.post("/save")
async def settings(settings: SettingsModel):
    try:
        if not os.path.exists("database"):
            os.makedirs("database")
        with open("database/settings.json", "w") as file:
            json.dump(settings.model_dump(), file, indent=4)
        file.close()
        return {"message": "Settings saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving settings: {str(e)}")

@router.get("/load")
async def get_settings():
    try:
        with open("database/settings.json", "r") as file:
            settings = json.load(file)
        file.close()
        return settings
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Settings not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding settings file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving settings: {str(e)}")