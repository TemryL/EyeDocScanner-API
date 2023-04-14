import json
from commands.gen_struct_out import process_data
from fastapi import FastAPI, HTTPException, Request, Response


app = FastAPI()


@app.get("/")
def read_root():
    return Response("The EyeDocScanner API is running.")

@app.post("/")
async def handle_post_request(request: Request):
    ctype = request.headers['content-type']
    
    # refuse to receive non-json content
    if ctype != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    # generate structured output
    data = await request.body()
    data = json.loads(data)
    processed_data, success = process_data(data)
    
    if success:
        # process the data and return a response
        return processed_data
    else:
        raise HTTPException(status_code=480, detail="Unable to process data")
