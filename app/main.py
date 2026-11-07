"""Aplicação FastAPI - uvicorn app.main:app --reload."""
from fastapi import FastAPI
from app.api.rotas import router

app = FastAPI(title="FinBot API", description="Chat educacional de investimentos — FATEC / PLN")
app.include_router(router)
