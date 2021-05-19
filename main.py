import fastapi

app= fastapi.FastAPI()


@app.get('/')
async def root():
    if fastapi.Request.client:
        return{'message':'Привет'}
    else:
        return{'dskf;'}