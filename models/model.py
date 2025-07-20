from pydantic import BaseModel

class SettingsModel(BaseModel):
    user_email: str
    search_email: str
    date_from: str
    date_to: str
    search_query: str

class EmailIdsModel(BaseModel):
    email_ids: list[str]

class AttachmentIdsModel(BaseModel):
    email_ids: list[str]
    attachment_ids: dict[str, list[list[str]]]