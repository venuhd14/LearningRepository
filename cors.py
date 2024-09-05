from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware this list all the origins,methods,headers,use "*" for all methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)
#allowing specific origin
app.add_middleware(
    CORSMiidlewrae,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET, POST"],
    allow_headers=["Content_type, Authorizationn"],    
)

#allowing multiple origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://newdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)