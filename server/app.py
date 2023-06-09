from datetime import datetime

from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory='templates')

WILL_COME = False
COME_TIME = None
LAST_UPDATE = None


@app.get('/admin', response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse('admin.html', {'request': request})

@app.post('/admin')
async def admin_form(willCome: str = Form(None), comeTime: str = Form(None)):
    global KNOWN, WILL_COME, COME_TIME, LAST_UPDATE
    WILL_COME = willCome or False
    COME_TIME = comeTime or None
    LAST_UPDATE = datetime.now()
    return RedirectResponse('/admin', status_code=status.HTTP_302_FOUND)

@app.get('/getcome')
async def getcome():
    if LAST_UPDATE is None or (datetime.now() - LAST_UPDATE).days > 1:
        return 'unknown'
    return {
        'will_come': WILL_COME,
        'come_time': COME_TIME,
    }
