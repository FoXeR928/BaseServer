import fastapi

app= fastapi.FastAPI()

@app.get('/info')
def root():
    return{'message':'Привет'}