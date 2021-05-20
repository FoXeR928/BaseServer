import uvicorn

open=open('port.txt', 'r')
port=(next(open))
ip=(next(open))

if __name__=='__main__':
    uvicorn.run(
        'app:app',
        host=ip,
        port=int(port),
        reload=True)