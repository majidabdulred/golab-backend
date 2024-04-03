from dotenv import load_dotenv
from app.auth import auth
from fastapi import FastAPI, Depends
from app import funtions, util, aws
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.exception_handler import exception_handler
from app.logs import logger
from config import config

load_dotenv()
app = FastAPI(title="golab", version="0.0.1")

app.add_exception_handler(Exception, exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if config.TESTING:
    logger.info("Testing mode")
else:
    logger.info("Production mode")

logger.info("MAIN BACKEND URL : " + config.BASE_METEX_API_URL)


@app.get("/")
async def root():
    return {"message": "Good to go Chief!"}


@auth.post("/signup")
async def signup(response=Depends(funtions.create_temp_user)):
    return response


@auth.post("/reset/send_otp")  # , responses=openapi_docs.response_reset_send_otp)
async def reset_send_otp(response=Depends(funtions.reset_send_otp)):
    return response


@auth.post("/reset/verify_otp")  # , responses=openapi_docs.response_reset_verify_otp)
async def reset_verify_otp(response=Depends(funtions.reset_verify_otp)):
    return response


@auth.post(
    "/reset/new_password"
)  # , responses=openapi_docs.response_reset_new_password)
async def reset_new_password(response=Depends(funtions.reset_new_password)):
    return response


@auth.post("/verify_otp")
async def verify_otp(response=Depends(funtions.verify_otp)):
    return response


@auth.post("/resend_otp")
async def resend_otp(response=Depends(funtions.resend_otp)):
    return response


@app.post(
    "/img2img/generate"
)  # , responses=openapi_docs.create_img2img_demo_response_examples)
async def create_img2img_demo(response=Depends(funtions.create_img2img)):
    return response


@app.post(
    "/txt2img/generate"
)  # , responses=openapi_docs.create_txt2img_demo_response_examples)
async def create_txt2img_demo(response=Depends(funtions.create_txt2img)):
    return response


@app.post("/qr/generate")
async def create_qr(response=Depends(funtions.create_qr)):
    return response


@app.get("/qr/presets")
async def create_qr_preset(response=Depends(funtions.get_qr_preset)):
    return response


@app.get("/request")
async def get_request_status(id: str):
    return await funtions.get_request_status(id)


# @app.get("/request")
# async def get_request_status(id: str):
#     await asyncio.sleep(random.randint(1, 10))
#     m = random.choice([True, False])
#     print(m)
#     if m:
#         return {"status": "PROCESSING"}
#     else:
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


@app.get("/file")
async def get_file(url: str):
    image = await aws.download_file_by_uri(url)
    print(type(image))
    return {"id": url.split("/")[-1], "base64": image, "type": "png"}


app.include_router(auth)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
