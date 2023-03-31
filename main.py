from typing import List
from pydantic import BaseModel
from commands.gen_struct_out import process_data
from fastapi import FastAPI, HTTPException, Request, Response


app = FastAPI()


class Point(BaseModel):
    x: float
    y: float

class Bbox(BaseModel):
    bottomLeft: Point
    bottomRight: Point
    topLeft: Point
    topRight: Point

class DetectedText(BaseModel):
    text: str
    bbox: Bbox

class CropRegion(BaseModel):
    x: float
    y: float
    width: float
    height: float

class OCRData(BaseModel):
    cropRegion: CropRegion
    detectedTextList: List[DetectedText]


@app.get("/")
def read_root():
    return Response("The EyeDocScanner API is running.")

@app.post("/")
def handle_post_request(data: List[OCRData], request: Request):
    ctype = request.headers['content-type']
    
    # refuse to receive non-json content
    if ctype != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    # generate structured output
    processed_data, success = process_data(data)
    
    if success:
        # process the data and return a response
        return processed_data
    else:
        raise HTTPException(status_code=480, detail="Unable to process data")
