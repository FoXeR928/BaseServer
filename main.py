import uvicorn

with open('port.txt', 'r') as ports:
    for x in ports:
        port=x

if __name__=='__main__':
    uvicorn.run(
        'app:app',
        host='localhost',
        port=int(port),
        reload=True)