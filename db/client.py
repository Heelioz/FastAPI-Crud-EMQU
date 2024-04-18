from pymongo import MongoClient

#Conexion local
#db_client = MongoClient()

#Conexion Remota
db_client= MongoClient("mongodb+srv://EMQU:test@cluster0.jyg0ozp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test