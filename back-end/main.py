from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class PredictRequest(BaseModel):
    video_file_name: str
    query: str

@app.post("/predict")
async def get_prediction(request: PredictRequest):
    result = predict(request.video_file_name, request.query)
    print(type(result))
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)