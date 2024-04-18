from fastapi import APIRouter
from db.models.pc_model import PC
from db.client import db_client
from db.schemas.pc_schema import pc_schema, pcs_schema

router= APIRouter( prefix= "/pc", tags=["PC"]) 

# http://127.0.0.1:8000 url local

# Comando para levantar el server  uvicorn app:app --reload

#Entidad PC



@router.get('/all', response_model=list[PC])
async def get_all_pc():
    return pcs_schema(db_client.local.pcs.find())
  

#Busqueda de pc por ip
@router.get('/')
def search_pc(field: str, key: str):
    try:
       pc = db_client.local.pcs.find_one({field: key})
       return PC(**pc_schema(pc))
    except:
        return "ERROR: PC no existente"

#Insercion nueva PC

@router.post("/")
async def create_pc(pc: PC):
   
    if type(search_pc("ip", pc.ip)) == PC:
        return "ERROR: PC ya registrada"

    pc_dict=dict(pc)

    del pc_dict["id"]

    id = db_client.local.pcs.insert_one(pc_dict).inserted_id
    new_pc = pc_schema(db_client.local.pcs.find_one({"_id": id}))

    return PC(**new_pc)

@router.put("/")
async def update_pc(pc: PC):
    

    pc_dict = dict(pc)
    del pc_dict["id"]
    
    try:
        db_client.local.pcs.find_one_and_replace({"ip": pc.ip}, pc_dict)
    
    except:
        return {"Error" : "No se ha actualizado la PC"}
    
    return search_pc("ip", pc.ip)


   
@router.delete("/")
async def delete_pc(field: str, key: str):
    
    found = db_client.local.pcs.find_one_and_delete({field: key})
    
    if not found:
        return {"error": "No se ha eliminado la PC"}
    
    return {"Message" : "PC eliminada"}
    



   
    
     

    



    
         

