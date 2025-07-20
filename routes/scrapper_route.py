from fastapi import APIRouter, HTTPException
from utils.access_token import GetAccessToken
from models.model import EmailIdsModel, AttachmentIdsModel
import json, requests
import base64, os

router = APIRouter()

@router.get("/list")
async def list_emails():
    try:
        with open("database/settings.json", "r") as file:
            settings = json.load(file)
        file.close()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Settings not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding settings file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving settings: {str(e)}")

    response = requests.get(
        f"https://gmail.googleapis.com/gmail/v1/users/{settings['user_email']}/messages?maxResults=500&q=from:acintapatna@gmail.com%20after:{settings['date_from']}%20before:{settings['date_to']}%20{settings['search_query']}",
        headers={
            "Authorization": f"Bearer {GetAccessToken().return_token().token}",
            "Accept": "application/json"
        }
    )

    email_ids_list = []
    if response.status_code == 200:
        try:
            for email in response.json().get('messages'):
                email_ids_list.append(email['id'])
            return {"email_ids": email_ids_list}
        except KeyError:
            raise HTTPException(status_code=500, detail="Error parsing email IDs from response")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@router.post("/get_body")
async def get_email_body(ids: EmailIdsModel):
    with open("database/settings.json", "r") as file:
        settings = json.load(file)
    file.close()
    attachments = {}
    for id in ids.email_ids:

        response = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/{settings['user_email']}/messages/{id}",
            headers={
                "Authorization": f"Bearer {GetAccessToken().return_token().token}",
                "Accept": "application/json"
            }
        )
        temp_attachments, temp_attachments_filenames = [], []
        if response.status_code == 200:
            try:
                for part in response.json()['payload']['parts']:
                    if 'attachmentId' in part['body']:
                        temp_attachments.append(part['body']['attachmentId'])
                        temp_attachments_filenames.append(part['filename'])
                attachments[id] = [temp_attachments, temp_attachments_filenames]
            except KeyError:
                raise HTTPException(status_code=500, detail="Error parsing email body from response")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return attachments

@router.post("/get_attachments")
async def get_email_attachments(ids: AttachmentIdsModel):
    with open("database/settings.json", "r") as file:
        settings = json.load(file)
    file.close()
    for email_id in ids.email_ids:
        for attachment_id in ids.attachment_ids[email_id][0]:
            response = requests.get(
                f"https://gmail.googleapis.com/gmail/v1/users/{settings['user_email']}/messages/{email_id}/attachments/{attachment_id}",
                headers={
                    "Authorization": f"Bearer {GetAccessToken().return_token().token}",
                    "Accept": "application/json"
                }
            )

            if response.status_code == 200:
                if not os.path.exists("attachments"):
                    os.makedirs("attachments")
                try:
                    attachment_data = response.json()['data']
                    filename = ids.attachment_ids[email_id][1][ids.attachment_ids[email_id][0].index(attachment_id)]
                    with open(f"attachments/{filename}", "wb") as file:
                        file.write(base64.urlsafe_b64decode(attachment_data.encode('UTF-8')))
                    file.close()
                except KeyError:
                    raise HTTPException(status_code=500, detail="Error parsing attachment data from response")
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    return  {"message": "Attachments downloaded successfully"}