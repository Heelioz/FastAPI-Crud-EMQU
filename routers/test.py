from fastapi import APIRouter
from db.models.pc_model import PC
from db.client import db_client
from db.schemas.pc_schema import pc_schema, pcs_schema

router= APIRouter( prefix= "/test", tags=["TEST"]) 