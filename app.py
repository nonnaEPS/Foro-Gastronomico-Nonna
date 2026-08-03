from flask import Flask, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from modules.usuario import crear_usuario


# para subir archivos
import os
#from werkzeug.utils import secure_filename


app = Flask(__name__)

import os

app.config["MYSQL_HOST"] = os.environ.get("DB_HOST")
app.config["MYSQL_USER"] = os.environ.get("DB_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("DB_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DB_NAME")
app.config["MYSQL_PORT"] = int(os.environ.get("DB_PORT"))

mysql = MySQL(app)

CORS(app)






@app.route("/subir_receta", methods=["POST"])
@cross_origin()
def subir_receta():
    usuario_idusuario = request.json["usuario_idusuario"]
    nombre = request.json["nombre"]
    imagenes = request.json["imagenes"]
    tiempo = request.json["tiempo"]
    ingredientes = request.json["ingredientes"]
    receta = request.json["receta"]
    likes = request.json["likes"]
    dislikes = request.json["dislikes"]
    cantidadComentarios = request.json["cantidadComentarios"] 
    

    cursor = mysql.connection.cursor()

    sql = "INSERT INTO publicacion(usuario_idusuario, nombre, imagenes, tiempo, ingredientes, receta, likes, dislikes, cantidadComentarios) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (usuario_idusuario, nombre, imagenes, tiempo, ingredientes, receta, likes, dislikes, cantidadComentarios))


    mysql.connection.commit()

    cursor.close()
    response = make_response()

    response = jsonify({"resultado":"Agregada nueva receta"})
    return response



@app.route("/iniciar_sesion", methods=["POST"])
@cross_origin()
def iniciar_sesion():
    email = request.json["email"]
    clave = request.json["clave"]
    #consulta SQL
    sql = "SELECT idusuario, email, nombre FROM usuario WHERE email=%s AND clave=%s"

    #crear el cursor
    cursor = mysql.connect.cursor()#mysql.connect.cursor()
    cursor.execute(sql, (email, clave))

    resultado = cursor.fetchall()

    #cerrar la conexión
    cursor.close()
    response = make_response()
    
    

@app.route("/traer_recetas", methods=["GET"])
@cross_origin()
def traer_recetas():
    #consulta SQL
    sql = "SELECT idpublicacion, nombre, imagenes,  ingredientes, receta FROM publicacion"

    #crear el cursor
    cursor = mysql.connection.cursor()#mysql.connect.cursor()
    cursor.execute(sql)

    resultado = cursor.fetchall()

    #cerrar la conexión
    cursor.close()
    response = make_response()

    if resultado == None:
        response = jsonify({"mensaje":None})
        return response
    else:
        recetas = []

        for i in resultado:

            p = {"idpublicacion":i[0], "nombre":i[1], "imagenes":i[2], "ingredientes":i[3], "receta":i[4]}
            recetas.append(p)

        return jsonify(recetas)
    


@app.route("/traer_usuarios", methods=["GET"])
@cross_origin()
def traer_usuarios():
    #consulta SQL
    sql = "SELECT idusuario, nombre, email FROM usuario"

    #crear el cursor
    cursor = mysql.connection.cursor()#mysql.connect.cursor()
    cursor.execute(sql)

    resultado = cursor.fetchall()

    #cerrar la conexión
    cursor.close()
    response = make_response()

    if resultado == None:
        response = jsonify({"mensaje":None})
        return response
    else:
        usuarios = []

        for i in resultado:

            p = {"idusuario":i[0], "nombre":i[1], "email":i[2]}
            usuarios.append(p)

        return jsonify(usuarios)
    
    

@cross_origin
@app.route("/eliminar_usuario/<id>", methods=["DELETE"])
def eliminar_usuario(id):

    sql = "DELETE FROM usuario WHERE idusuario=%s"

    #crear el cursor
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (id,))

    mysql.connection.commit()

    #cerrar la conexión
    cursor.close()
    response = make_response()


    response = jsonify({"resultado":"Usuario eliminado"})
    return response



@cross_origin
@app.route("/actualizar_usuario/<id>", methods=["PUT"])
def actualizar_usuario(id):
    nombre = request.json["nombre"]

    sql = "UPDATE usuario SET nombre=%s WHERE idusuario=%s"

    #crear el cursor
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (nombre, id))
    mysql.connection.commit()


    #cerrar la conexión
    cursor.close()
    response = make_response()

    response = jsonify({"resultado":"Usuario no activo"})
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)