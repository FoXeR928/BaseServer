import fastapi
from fastapi import responses
from fastapi.responses import HTMLResponse

app= fastapi.FastAPI()

@app.get('/info')
def root():
    return{'message':'Привет'}

@app.get('/html', response_class=HTMLResponse)
def html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <header>
            <a href="http://localhost/info">dfgdfgd</a>
            <a href="http://localhost/info">fwerwer</a>
            <a href="http://localhost/info">werwer</a>
            <a href="http://localhost/info">ewrwerwer</a>
        </header>
        <main>
            <p>fdgjdfgjdflgjdfgldjfgoeritueoritueroitejgdkfgdfm,bndorituergl,fgjerotue</p>
        </main>
        <footer>
            <a href="http://localhost/info">werwerw</a>
            <a href="http://localhost/info">werwerw</a>
            <a href="http://localhost/info">werwer</a>
            <a href="http://localhost/info">werwerwr</a>
        </footer>
    </body>
    </html>
    """