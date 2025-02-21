from fastapi import FastAPI
from PG import PG


app = FastAPI()
pg = PG()


@app.get('/')
async def check():
    return {'status': 'OK'}


@app.post('/massage')
async def message():
    pass

