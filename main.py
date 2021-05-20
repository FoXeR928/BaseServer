import uvicorn
from __init__ import all

if __name__=='__main__':
    uvicorn.run(
        'app:app',
        host=all.ip,
        port=all.port,
        reload=True)