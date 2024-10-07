from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, Response, Security, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from models.entry import EntryList
from models.form import FormData
from auth import api_key_auth
from db.db import post_form, check_email_exists

load_dotenv()
middleware_key = os.getenv('SESSION_MIDDLEWARE_KEY')

# TODO:
# determine data source to feed API - currently json file. spreadsheet? user supplied?
# API frontend 
    # assigning / revoking unique api keys to client?
    # user key management - requesting new keys? periodic key expiration? 
    # monitoring user key access / requests
# remove POST capability on endpoint once data is set
# persisting & continually adding data

app = FastAPI()

# rate limiter 
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# session middleware
app.add_middleware(SessionMiddleware, secret_key=str(middleware_key), max_age=3600, https_only=True)

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates
templates = Jinja2Templates(directory="templates")

# frontend routes
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.jinja')

@app.post('/', response_class=HTMLResponse)
async def form_handler(request: Request, form_data: FormData = Form(...)): # handle as form fields, not json
    emailExists = check_email_exists(form_data.email)
    user_api_key = None
    message = None
    if emailExists:
        message = "Email record exists. Please enter another email."
        user_api_key = None
    else: 
        message = "Thanks! Your API key is: " 
        user_api_key = post_form(form_data)
    
    return templates.TemplateResponse(request=request, name='index.jinja', context={'user_key': user_api_key, 'message': message})
    
# endpoint routes
@app.get('/api/v1')
async def status():
    return {'status': 'ok'}

data_set = []

@app.post('/api/v1/academies')
@limiter.limit('10/minute')
async def post_entries(request: Request, data: EntryList, api_key: str = Security(api_key_auth)):
    # access data obj in future requests
    data_set.append(data) 
    return data

@app.get('/api/v1/academies')
@limiter.limit('10/minute')
async def get_entries(request: Request, response: Response, api_key: str = Security(api_key_auth)):
    return data_set

# TODO: searching / filtering / limiting etc within endpoint - query params