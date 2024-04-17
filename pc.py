from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# http://127.0.0.1:8000 url local

# Comando para levantar el server  uvicorn app:app --reload

#Entidad PC

class PC(BaseModel):
    id: int
    name: str
    ip: str
    ping: bool
    count: int

#Entidad User

class User(BaseModel):
    mail: str
    password: str

PC_list = [PC(id= 1, name ="HeliozPC", ip = "192.168.4.5", ping = True, count = 5),
           PC(id= 2, name ="SOFIPC", ip = "192.168.4.6", ping = True, count = 5),
           PC(id= 3, name ="HELLO", ip = "192.168.4.10", ping = True, count = 5)]

users_list = [User( mail ="marcosjduque2@gmail.com", password = "12345")]


@app.get('/pc/all')
async def get_all_pc():
    return PC_list

   
#Query
@app.get("/pc/")
async def get_pc(name: str):
    return search_pc(name)


#Busqueda de pc por nombre
def search_pc(name :str):
    
    pcs = filter(lambda pc: pc.name == name, PC_list)
    try:
        return list(pcs)[0]
    except:
        return "ERROR: PC no existente"

#Insercion nueva PC

@app.post("/pc/")
async def create_pc(pc: PC):
    if type(search_pc(pc.name))== PC:
        return {"ERROR":"PC ya registrada"} #Valida que el objeto que devuelve la busqueda por nombre del objeto a registrarse no devuelva una pc registrada
    
    PC_list.append(pc)
    return pc

@app.put("/pc/")
async def update_pc(pc: PC):
    
    if type(search_pc(pc.name)) == PC: 

        for index, saved_pc in enumerate(PC_list):
            if saved_pc.name == pc.name:
                PC_list[index] = pc
                found = True

    else:
        return {"error":"Pc no actualizado"}
    
    return {"error":"Pc actualizado"}, pc
    
@app.delete("/pc/")
async def update_pc(name: str):
    
    if type(search_pc(name)) == PC: 
 
        for index, saved_pc in enumerate(PC_list):
            if saved_pc.name == name:
                del PC_list[index]
                found = True

    else:
        return {"error":"Pc no eliminada"}
    
    return {"error":"Pc eliminada"}


   
    
     

    



    
         

