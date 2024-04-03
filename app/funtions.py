import asyncio
import random

from app import util
from app.send_mail import send_mail
from app import db, schema, auth
from fastapi import HTTPException, Body, Depends, UploadFile, File, Form
from app import metexapi


async def get_users_request(user: schema.UserFromDb = Depends(auth.get_current_user)):
    userdata = db.get_user_by_id()
    """Create a avatar"""


async def create_temp_user(user: schema.TempUser) -> dict:
    """Create a temp user and send email verification and stores the otp in database"""
    if not (user.email.endswith("@metex.co") or user.email.endswith("@immu.ai")):
        raise HTTPException(
            status_code=403, detail="Email must be of metex.co or immu.ai."
        )
    response = await db.create_user(
        user.name, user.email, user.password
    )  # Create a temp user
    otp = await db.create_otp(response)
    await send_mail(user.email, user.name, otp)
    return {"otp_id": str(response)}


async def verify_otp(
    otp_id: str = Body(..., max_length=24, min_length=24), otp: int = Body(...)
):
    """Verify otp and create a user in database"""
    response = await db.verify_otp(otp_id, otp)
    return {"verified": response}


async def resend_otp(otp_id: schema.otp_id):
    """Resend otp has body otp_id"""
    otp = await db.create_otp(otp_id.otp_id)
    user = await db.temp_users.find_one({"_id": db.ObjectId(str(otp_id.otp_id))})
    await send_mail(user.get("email"), user.get("name"), otp)
    return {"otp_id": otp_id.otp_id}


async def reset_send_otp(email: schema.Email):
    """Send otp to email"""
    user = await db.get_user_by_email(email.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    otp_id = await db.reset_create_user(email.email, user.name)
    otp = await db.create_otp(otp_id)
    await send_mail(email.email, user.name, otp)
    return {"otp_id": str(otp_id)}


async def reset_verify_otp(
    otp_id: str = Body(..., max_length=24, min_length=24), otp: int = Body(...)
):
    """Verify otp and create a user in database"""
    response = await db.reset_verify_otp(otp_id, otp)
    return {"verified": response}


async def reset_new_password(data: schema.NewPassword):
    """Reset password"""
    await db.reset_new_password(data.otp_id, data.password)
    return {"success": True}

async def create_img2img(
    image: UploadFile = File(...),
    url: str = Form(...),
    prompt: str = Form(...),
    user: schema.UserFromDb = Depends(auth.get_current_user)
) -> dict:
    payload = schema.Sendimg2img(
        user_id=user.id,
        prompt= prompt,
        url=url,
        image=image,
    )
    response = await metexapi.create_img2img(payload)
    await db.add_request(response.get("id"), "user.id")

    return {
        "request_id": response.get('session_id'),
        "image_data": response.get('image_data'),
    }


async def create_txt2img(
    data: schema.CreateTxt2ImgRequest,
    user: schema.UserFromDb = Depends(auth.get_current_user),
) -> dict:
    """Create a avatar"""
    height, width = util.set_height_and_width(data.aspect_ratio)
    payload = schema.Sendtxt2Img(
        user_id=user.id,
        parameters=schema.Parameters(
            prompt=data.prompt,
            batch_size=data.num,
            width=width,
            height=height,
            negative_prompt=data.negative_prompt,
        ),
    )
    response = await metexapi.create_txt2img(payload)
    await db.add_request(response.get("id"), user.id)

    return {
        "request_id": response.get("session_id"),
        "image_data": response.get("image_data"),
    }


async def create_qr(
    data: schema.CreateQRRequest,
    user: schema.UserFromDb = Depends(auth.get_current_user),
) -> dict:
    """Create a avatar"""
    payload = schema.SendQR1Request(user_id=user.id, url=data.url, prompt=data.preset)
    response = await metexapi.post_qr_request(payload)
    await db.add_request(response.get("id"), user.id)
    return {
        "request_id": response.get("session_id"),
        "image_data": response.get("image_data"),
    }


async def get_qr_preset():
    all_presets = await db.get_qr_presets_db()
    presets = [
        {
            "text": i.get("name"),
            "name": str(i.get("_id")),
            "image": {"id": i.get("image").split("/")[-1], "url": i.get("image")},
        }
        for i in all_presets
    ]
    return {"num": len(all_presets), "presets": presets}


async def get_request_status(id: str, RECURSTION=0):
    response = await db.get_request_data(id)
    status = response.get("status")
    if status == "complete":
        payload = {
            "status": "COMPLETE",
            "request_id": id,
            "type": response.get("request_type"),
            "isfavorite": False,
            "version": 1,
            "request_data": {"prompt": response.get("parameters").get("prompt")},
            "output": {
                "images": [
                    {"id": i.split("/")[-1], "url": i}
                    for i in response.get("output").get("images")
                ]
            },
        }
        return payload
    elif status == "processing" or status == "available":
        if RECURSTION > 5:
            return {"status": "PROCESSING"}
        await asyncio.sleep(5)
        return await get_request_status(id, RECURSTION + 1)


#         return {"status": "COMPLETE",
#
#                 "request_id": id,
#                 "type": "txt2img",
#                 "isfavorite": False,
#                 "version": 1,
#                 "request_data": {
#                     "prompt": "Lorem ipsum"
#                 },
#                 "output": {
#                     "images": [{"id": "32e2d23d23e23e",
#                                 "url": ""} for i in range(4)]
#                 }}
