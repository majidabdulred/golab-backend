from fastapi import Request, HTTPException
from app import custom_exceptions

async def exception_handler(request:Request,exc:Exception):
    if isinstance(exc, custom_exceptions.GradioUrlNotFound):
        print(exc.instance_id,"Gradio Url Not found")
