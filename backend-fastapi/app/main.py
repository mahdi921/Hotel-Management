from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Hotel Management API",
    description="High-performance Public API for Local Smart Hotel Management system",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Hotel Management API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

from .routers import rooms, bookings, invoices
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(invoices.router)
