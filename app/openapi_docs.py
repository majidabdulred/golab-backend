import os

from app import schema
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()


get_me_demo_response = {
    "_id": "64e467b68028c88b0ee6bdd0",
    "name": "First Second",
    "email": "email@gmail.com",
    "instances": {
        "i-0fb45fb3b178dead7": {
            "state": "running",
            "gradio_url": "https://3c390543259a6961cb.gradio.live"
        }
    }
}



CODE_401 = {"description": "This is description",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
            }
get_me_demo_response_examples = \
    [get_me_demo_response.copy(),
     {**get_me_demo_response, "instances": {"state": "creating", "gradio_url": ""}},
     {**get_me_demo_response, "instances": {"state": "starting", "gradio_url": ""}}, ]

create_txt2img_demo_response_examples = {
    401:CODE_401,
    200:{"request_id":"64e467b68028c88b0ee6bdd0"},
    400:{"error_type":"notokenbalance"}
}
class GetMeResponse(BaseModel):
    _id: str
    name: str
    email: str
    instances: dict
    # Add example

    model_config = {
        "json_schema_extra": {
            "examples": get_me_demo_response_examples
        }
    }


response_get_me = \
    {200: {"description": "This is description",
           "model": GetMeResponse},
     401: CODE_401}


class CreateSessionResponse(BaseModel):
    success: bool
    instance_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"success": True, "instance_id": "i-0fb45fb3b178dead7"}
            ]
        }
    }


response_create_session = \
    {200: {"description": "This is description",
           "model": CreateSessionResponse},
     401: CODE_401,
     403: {"content": {"application/json:": {"examples": [{
         "detail": "You have reached maximum active sessions"
     },
         {"detail": "No available slots"}]}}}}

response_ping = \
    {200: {"content": {"application/json": {"example": {"success": True}}}},
     401: CODE_401,
     403: {"content": {"application/json:": {"example": {"detail":"User does not have access to this instance"}}}},
     400: {"content": {"application/json:": {"example": {"detail":"Instance not running"}}}}}

response_reset_send_otp = \
    {200:{"content": {"application/json": {"example": {"otp_id": "64e467b68028c88b0ee6bdd0"}}}},
    404: {"content": {"application/json:": {"example": {"detail": "User not found"}}}}}

response_reset_verify_otp = \
    {200:{"content": {"application/json": {"example": {"verified": True,"otp_id":"64e467b68028c88b0ee6bdd0"}}}},
        400: {"content": {"application/json:": {"example": {"detail": "Invalid otp id"}}}},
     }

response_reset_new_password = \
    {200:{"content": {"application/json": {"example": {"success": True}}}},
        400: {"content": {"application/json:": {"examples": [{"detail": "Invalid otp id"},{"detail": "Otp not verified"}]}}},
     }