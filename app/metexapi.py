from aiohttp import request
from app import schema
from config import config
from app.logs import logger


# async def create_txt2img(data:schema.Sendtxt2Img):
#     data = data.dict(exclude_none=True)
#     async with request("POST", f"{BASE_METEX_API_URL}/v3/golab/create-custom", json=data) as response:
#         if response.status == 422:
#             logger.error(f"SENDTXT2IMG VALIDATION ERROR : {await response.json()}")
#             raise ValueError
#         if response.status != 200:
#             logger.error(f"¸ SENDTXT2IMG ERROR :  {await response.text()}")
#             raise ValueError
#         res_json = await response.json()
#         res_json.info(f"SENDTXT2IMG : SESSION : {res_json.get('id')}")
#         return res_json
async def create_txt2img(data: schema.Sendtxt2Img):
    URL = config.BASE_METEX_API_URL + "/v3/user/create-txt2img"

    data = data.dict(exclude_none=True)

    async with request(method="POST", url=URL, json=data) as res:
        if res.status == 422:
            logger.error(f"CREATE_CUSTOM_REQUEST VALIDATION ERROR : {await res.json()}")
            raise ValueError
        if res.status != 200:
            logger.error(f"CREATE_CUSTOM_REQUEST ERROR : {URL} : {await res.text()}")
            raise ValueError
        res_json = await res.json()
        logger.info(f"POST CUSTOM REQUEST : SESSION : {res_json.get('session_id')}")
        return res_json


async def post_qr_request(data):
    URL = config.BASE_METEX_API_URL + "/v3/user/create-qr1"

    data = data.dict(exclude_none=True)

    async with request(method="POST", url=URL, json=data) as res:
        if res.status == 422:
            logger.error(f"CREATE_QR_REQUEST VALIDATION ERROR : {await res.json()}")
            raise ValueError
        if res.status != 200:
            logger.error(f"CREATE_QR_REQUEST ERROR : {URL} : {await res.text()}")
            raise ValueError
        res_json = await res.json()
        logger.info(f"POST QR REQUEST : SESSION : {res_json.get('session_id')}")
        return res_json
