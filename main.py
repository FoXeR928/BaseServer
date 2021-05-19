import uvicorn

ports=open('port.txt', 'r')

if __name__=='__main__':
    uvicorn.run(
        'app:app',
        host='localhost',
        port=80,
        reload=True)