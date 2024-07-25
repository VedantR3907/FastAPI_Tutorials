from fastapi import FastAPI, Request
import logging
import time

app = FastAPI()

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



'''
This middleware is called with each and every API, the response written is the response of API, Everything you write
above the response line will be performed before getting the response and everything you write after the response
will be executed after generating the response from the API
'''
# Define middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Process time: {process_time:.4f} seconds")
    
    return response

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Logging Middleware"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
