from app.db_client import get_db_client
from app import auth
import time
from app import schema
import random
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from config import config
from app.logs import logger

client = get_db_client()
db = client.get_database("golab_test" if config.TESTING else "golab")

instances = db.get_collection("instances")
users = db.get_collection("users")
temp_users = db.get_collection("temp_users")

backend_db = client.get_database("backend_test" if config.TESTING else "backend")
requests = backend_db.get_collection("requests")

config_golab_db = client.get_database("config-golab")
qr_parameters_col = config_golab_db.get_collection("qr-parameters")

new_user = {
    "name": "name",
    "email": "email",
    "golab": {"password": "password"},
    "tokens": 0,
    "history": [],
    "total_requests": 0,
}


async def get_request_data(request_id: str):
    return await requests.find_one({"_id": ObjectId(request_id)})


async def add_request(request_id, user_id):
    response = await users.update_one(
        {"_id": ObjectId(user_id)}, {"$push": {"history": request_id}}
    )


async def get_qr_presets_db():
    response = await qr_parameters_col.find({}).to_list(length=1000)
    logger.debug(len(response))
    return response


async def reset_create_user(email: str, name: str):
    """Creates a reset user"""
    response = await temp_users.insert_one(
        {
            "email": email,
            "name": name,
        }
    )
    return str(response.inserted_id)


async def reset_verify_otp(_id: str, otp: int) -> bool:
    user = await temp_users.find_one({"_id": ObjectId(str(_id))})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid otp id")
    if user.get("otp") == otp and user["expire_after"] > int(time.time()):
        await temp_users.update_one(
            {"_id": ObjectId(str(_id))}, {"$set": {"verified": True}}
        )
        return True
    else:
        return False


async def reset_new_password(_id: str, password: str) -> None:
    user = await temp_users.find_one({"_id": ObjectId(str(_id))})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid otp id")
    if not user.get("verified"):
        raise HTTPException(status_code=400, detail="Otp not verified")
    await temp_users.delete_one({"_id": ObjectId(str(_id))})
    await users.update_one(
        {"email": user.get("email")},
        {"$set": {"golab": {"password": auth.get_password_hash(password)}}},
    )


async def create_user(name: str, email: str, password: str) -> str:
    """
    Create a temp user and send email verification and stores the otp in database
    :param name:
    :param email:
    :param password:
    :return str::
    i-0bc6849dda3f17ffd64e467b68028c88b0ee6bdc0
    """
    user = await users.find_one({"email": email})
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print("CREATING_USER : ", name, email, password)
    response = await temp_users.insert_one(
        {"name": name, "email": email, "password": auth.get_password_hash(password)}
    )
    print("CREATED_USER : ", name, email, password)
    return str(response.inserted_id)


def create_random_otp():
    return random.randint(100000, 999999)


async def create_otp(_id: str) -> None:
    """
    Store otp in database
    :param _id:
    :param otp:
    :return None:
    """
    print("CREATE_OTP : ", _id)
    user = await temp_users.find_one({"_id": ObjectId(str(_id))})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid otp_id")
    if user.get("expire_after") and user.get("expire_after") > int(time.time()):
        otp = user.get("otp") if user.get("otp") else create_random_otp()
    else:
        otp = create_random_otp()
    await temp_users.update_one(
        {"_id": ObjectId(str(_id))},
        {"$set": {"otp": otp, "expire_after": int(time.time()) + 600}},
    )
    print("CREATED_OTP : ", _id, otp)
    return otp


async def get_password(email: str) -> str:
    """
    Get password from database
    :param email:
    :return str:
    """
    user = await users.find_one({"email": email})
    print(user)
    if user:
        return user["golab"]["password"]


async def get_user_by_email(email: str) -> schema.UserFromDb | None:
    """
    Get user by email
    :param email:
    :return schema.UserFromDb | None:
    """
    user = await users.find_one({"email": email})
    if user:
        return schema.UserFromDb(
            _id=str(user["_id"]), email=user["email"], name=user["name"]
        )


async def get_user_by_id(_id: str) -> schema.UserFromDb | None:
    """
    Get user by id
    :param _id:
    :return schema.UserFromDb | None:
    """
    user = await users.find_one({"_id": ObjectId(str(_id))})
    if user:
        return schema.UserFromDb(**user)


async def verify_otp(_id: str, otp: int) -> bool:
    """
    Verify otp and create a user in database
    :param _id:
    :param otp:
    :return bool:
    """
    user = await temp_users.find_one({"_id": ObjectId(str(_id))})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid otp id")
    if user.get("otp") == otp and user["expire_after"] > int(time.time()):
        await users.insert_one(
            {
                **new_user,
                "name": user["name"],
                "email": user["email"],
                "golab": {"password": user["password"]},
            }
        )
        await temp_users.delete_one({"_id": ObjectId(str(_id))})
        return True
    else:
        return False


async def get_temp_user(_id):
    """
    Get temp user
    :return schema.UserFromDb | None:
    """
    user = await temp_users.find_one({"_id": ObjectId(str(_id))})
    if user:
        return schema.UserFromDb(**user)
