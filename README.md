# FastAPI-Crud-EMQU

Este código de Python define un conjunto de rutas API para gestionar información de computadoras (PC) en una base de datos. Utiliza el framework FastAPI para crear una API RESTful y se conecta a una base de datos MongoDB a través de un cliente personalizado (db_client).

Recursos utilizados

FastAPI: Un framework web para desarrollar APIs RESTful en Python de forma rápida y eficiente.
MongoDB: Una base de datos NoSQL que almacena datos en colecciones de documentos JSON.
Entidad PC: Un modelo que representa la estructura de los datos de las computadoras, incluyendo campos como id, ip, etc. (Se asume que está definido en db.models.pc_model).
Esquemas PC: Se utilizan para serializar y deserializar datos de PC a/desde el formato JSON (https://github.com/tiangolo/full-stack-fastapi-template).
pc_schema: Representa un único objeto PC.
pcs_schema: Representa una lista de objetos PC.

Funciones del código

Importaciones:

Se importan las librerías necesarias: APIRouter de FastAPI, PC del modelo de PC, db_client del cliente de la base de datos y los esquemas pc_schema y pcs_schema.
Rutas API:

Se crea un enrutador router con el prefijo /pc y la etiqueta "PC" para agrupar las rutas relacionadas con las computadoras.

Obtener todos los PC (/all):

La función get_all_pc responde a solicitudes GET a la ruta /pc/all.
Recupera todos los documentos PC de la colección pcs en la base de datos de forma asíncrona.
Aplica el esquema pcs_schema para convertir los documentos de MongoDB a objetos PC y devuelve la lista resultante.
Buscar PC por campo (/):

La función search_pc responde a solicitudes GET a la ruta /pc.
Toma dos parámetros: field (campo de búsqueda, como ip) y key (valor del campo para buscar).
Busca un documento PC en la base de datos que coincida con el campo y valor especificados.
Si se encuentra un PC, lo convierte a un objeto PC usando PC(**pc_schema(pc)) y lo devuelve.
Si no se encuentra, devuelve un mensaje de error.
Crear una nueva PC (/):

La función create_pc responde a solicitudes POST a la ruta /pc.
Toma un objeto PC como argumento.
Comprueba si ya existe una PC con la misma dirección IP llamando a search_pc (se podría optimizar con una consulta única a la base de datos).
Si ya existe, devuelve un mensaje de error.
De lo contrario, convierte el objeto PC a un diccionario y elimina la clave id (asumiendo que la base de datos genera IDs automáticamente).
Inserta el documento PC en la base de datos y recupera el ID generado.
Busca la PC recién creada por ID y la devuelve como un objeto PC.

Actualizar una PC (/):

La función update_pc responde a solicitudes PUT a la ruta /pc.
Toma un objeto PC como argumento.
Convierte el objeto PC a un diccionario y elimina la clave id.
Intenta reemplazar un documento existente en la base de datos que coincida con la dirección IP (ip) proporcionada en el objeto PC.
Si la actualización falla (por ejemplo, si la PC no existe), devuelve un mensaje de error.
De lo contrario, devuelve un mensaje de éxito y llama a search_pc para obtener la PC actualizada.
Eliminar una PC (/):

La función delete_pc responde a solicitudes DELETE a la ruta /pc.
Toma dos parámetros: field (campo de búsqueda, como ip) y key (valor del campo para buscar).
Busca un documento PC en la base de datos que coincida con el campo y valor especificados.
Si no se encuentra la PC, devuelve un mensaje de error.
Si se encuentra la PC, verifica que el campo count no tenga un valor mayor a cero, si este campo esta 
en un valor mayor significa que el equipo fue sometido a una prueba de ping y no puede ser eliminado.

En el archivo jwt_bd  se encuentra un codigo para la autenticación de usuarios en un sistema basado en FastAPI y MongoDB. Utiliza JWT para la seguridad y almacena las contraseñas de forma segura mediante hash y un token de seguridad jwt 

Dependencias de seguridad:

Se define una instancia de OAuth2PasswordBearer para manejar la autenticación basada en tokens.
Se crea un objeto CryptContext para el hash seguro de contraseñas.
Funciones de búsqueda de usuarios:

search_user: Busca un usuario en la base de datos por su correo electrónico y devuelve su información pública como un objeto User si lo encuentra.
search_user_db: Busca un usuario en la base de datos por su correo electrónico y devuelve su información completa como un objeto UserDB si lo encuentra (incluye la contraseña hasheada).
Función de autenticación (auth_user):

Verifica la validez del token de acceso proporcionado en la solicitud.
Decodifica el token y extrae el correo electrónico del usuario.
Busca el usuario en la base de datos por su correo electrónico y lo devuelve como un objeto User si es válido.
Función para obtener el usuario actual (current_user):

Se asegura de que el usuario obtenido de la función auth_user esté activo (no deshabilitado).
Devuelve el usuario actual como un objeto User.
Ruta para obtener información del usuario actual (/me):

Utiliza la dependencia current_user para obtener el usuario autenticado.
Devuelve la información pública del usuario actual como un objeto User.
Ruta para iniciar sesión (/login):

Recibe el nombre de usuario y contraseña del formulario de inicio de sesión.
Busca el usuario en la base de datos por su correo electrónico.
Verifica si la contraseña introducida coincide con la contraseña hasheada almacenada para el usuario.
Si la autenticación es correcta, genera un token de acceso JWT con el correo electrónico del usuario y la fecha de expiración.
Devuelve el token de acceso y su tipo (bearer).
Ruta para registrarse (/signup):
Recibe los datos del nuevo usuario en formato JSON.
Verifica si ya existe un usuario con el mismo correo electrónico.
Crea un nuevo objeto UserDB con los datos del usuario.
Hashea la contraseña del usuario de forma segura y la almacena en el objeto UserDB.
Inserta el nuevo usuario en la colección de usuarios de la base de datos.
Devuelve un mensaje de confirmación del registro exitoso.