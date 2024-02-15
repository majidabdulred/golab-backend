from pydantic import BaseModel,Field,EmailStr

from enum import Enum
from typing import List,Optional,AnyStr
import random
from bson import ObjectId

class CreateQRRequest(BaseModel):
    url: str
    # prompt: str
    preset: str
class SendQR1Request(BaseModel):
    user_id: str
    url : str
    prompt: str
class Parameters(BaseModel):
    prompt: str
    seed: Optional[int]=None
    batch_size: Optional[int]=None
    cfg_scale: Optional[int]=None
    steps : Optional[int]=None
    width : Optional[int]=None
    height : Optional[int]=None
    negative_prompt : Optional[str]=None


class Sendtxt2Img(BaseModel):
    user_id : str
    parameters : Parameters
# class Sendtxt2ImgOld(BaseModel):
#     request_type: str = "custom"
#     user_id: str
#     prompt: str
#     batch_size: Optional[int] = 4
#     width: Optional[int] = 512
#     height: Optional[int] = 512
#     negative_prompt: Optional[str] = ""
#
#     # seed: Optional[int] = int(random.random() * 1000000)
#     # sampler_name: Optional[str] = "Euler a"
#     # steps: Optional[int] = 25
#     # cfg_scale: Optional[int] = 7
#     #
#     # tiling: Optional[bool] = True
#     #
#     # restore_faces: Optional[bool] = True
#     class Config:
#         validate_assignment = True


class ASPECT_RATIO(str, Enum):
    sixteen_nine = "16:9"
    four_three = "4:3"
    three_four = "3:4"
    one_one = "1:1"
    two_three = "2:3"
    three_two = "3:2"
    nine_sixteen = "9:16"


class CreateTxt2ImgRequest(BaseModel):
    prompt: AnyStr
    negative_prompt: AnyStr
    num: int
    aspect_ratio: ASPECT_RATIO


class CREATE_AVATAR(BaseModel):
    images: List
    selected_type: str


class BaseFile(BaseModel):
    id: str
    url: str


class REQUEST_TYPE(str, Enum):
    avatar = "avatar"
    txt2img = "txt2img"
    qr = "qr"
    upscale = "upscale"


class REQUESTDATA(BaseModel):
    request_id: str = Field(alias="_id")
    type: REQUEST_TYPE


class HistoryRequests(BaseModel):
    offset: int
    limit: int
    data: List[REQUESTDATA]


class NewUser(BaseModel):
    name: str
    email: str
    profile_pic: BaseFile
    tokens: int
    history: List


class UserFromDb(BaseModel):
    name:Optional[str]="NaN"
    id: str = Field(alias="_id")
    email: str


class Email(BaseModel):
    email: EmailStr


class NewPassword(BaseModel):
    password: str
    otp_id: str = Field(..., max_length=24, min_length=24)


class otp_id(BaseModel):
    otp_id: str = Field(..., max_length=24, min_length=24)


class TempUser(BaseModel):
    name: str
    email: str
    password: str