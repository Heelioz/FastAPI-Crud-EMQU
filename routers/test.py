from fastapi import APIRouter
from db.models.pc_model import PC
from db.client import db_client
from db.schemas.pc_schema import pc_schema, pcs_schema


router= APIRouter( prefix= "/test", tags=["TEST"]) 

@router.put("/ping")
async def increment_pc_count(ip: str):
    
    found_pc = db_client.pcs.find_one({"ip": ip})

    if not found_pc:
        return {"error": "PC no encontrada con la IP proporcionada."}

    else:
        found_pc["count"] += 1
        db_client.pcs.find_one_and_replace({"ip": ip}, found_pc)

    if found_pc.get("ping", 0) == False:
        return {"Message": "Ping realizado, no hubo respuesta de  " + ip}

    return {"Message": "Ping realizado respuesta exitos de  " + ip}