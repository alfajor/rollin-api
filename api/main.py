from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, Security, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from models.entry import EntryList
from models.form import FormData
from auth import api_key_auth
from db.db import post_form

load_dotenv()
middleware_key = os.getenv('SESSION_MIDDLEWARE_KEY')

# TODO:
# determine data source to feed API - json file? spreadsheet? user supplied?
# API frontend 
    # assigning / revoking unique api keys to client 
    # user key management? periodic key expiration? 
    # prevent duplicate email entries
# rate limiting requests - user / key based? -- https://github.com/laurentS/slowapi
# remove POST capability on endpoint once data is set
# persisting & continually adding data

app = FastAPI()

# session middleware
app.add_middleware(SessionMiddleware, secret_key=str(middleware_key), max_age=3600, https_only=True)

# @app.middleware('http')
# async def set_state_key(request: Request, call_next):
#     # set variable to req state & access in http route
#     request.state.user_key = '' # some value to be passed
#     res = await call_next(request)
#     return res

# static dir
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates
templates = Jinja2Templates(directory="templates")

# frontend routes
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.jinja')

@app.post('/', response_class=RedirectResponse)
async def form_handler(request: Request, form_data: FormData = Form(...)): # handle as form fields, not json
    # post & pass key to template
    user_api_key = post_form(form_data)
    return templates.TemplateResponse(request=request, name='index.jinja', context={'user_key': user_api_key})
    # return RedirectResponse(url='/', status_code=303)
    
# endpoint routes
@app.get('/api/v1')
def status():
    return {'status': 'ok'}

data_set = []

@app.post('/api/v1/academies')
def post_entries(data: EntryList, api_key: str = Security(api_key_auth)):
    # access data obj in future requests
    data_set.append(data) 
    return data

@app.get('/api/v1/academies')
def get_entries(api_key: str = Security(api_key_auth)):
    return data_set