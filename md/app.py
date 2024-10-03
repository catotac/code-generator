from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat_routes import chat_bp
from app.routers.code_routes import code_bp

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include your chat and code routers
app.include_router(chat_bp)
app.include_router(code_bp)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, debug=True)  # Set your custom host and port
