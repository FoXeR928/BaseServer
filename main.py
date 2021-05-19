import fastapi

app= fastapi.FastAPI()

@app.get('/info')
async def root():
    return{'message':'Привет'}