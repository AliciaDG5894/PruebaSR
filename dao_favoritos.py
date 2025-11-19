import mysql.connector
from datetime import datetime

def obtener_favoritos(con, id_usuario):
    """
    Devuelve los favoritos de un usuario, junto con datos de la receta.
    """
    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT 
        f.IdFavorito,
        f.Id_Usuario,
        f.IdReceta,
        f.Comentario,
        f.Calificacion,
        f.Fecha,
        r.Nombre,
        r.Descripcion,
        r.Categorias,
        r.Imagen
    FROM Favoritos f
    INNER JOIN Recetas r ON f.IdReceta = r.IdReceta
    WHERE f.Id_Usuario = %s
    ORDER BY f.Fecha DESC
    """
    val = (id_usuario,)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()
    finally:
        cursor.close()

    return registros


def guardar_favorito(con, id_usuario, id_receta, comentario=None, calificacion=None):

    cursor = con.cursor(dictionary=True)

    try:
        sql_buscar = """
        SELECT IdFavorito
        FROM Favoritos
        WHERE Id_Usuario = %s
          AND IdReceta   = %s
        """
        val_buscar = (id_usuario, id_receta)
        cursor.execute(sql_buscar, val_buscar)
        row = cursor.fetchone()

        ahora = datetime.now()

        if row:
            sql_update = """
            UPDATE Favoritos
            SET Comentario  = %s,
                Calificacion = %s,
                Fecha        = %s
            WHERE IdFavorito = %s
            """
            val_update = (comentario, calificacion, ahora, row["IdFavorito"])
            cursor.execute(sql_update, val_update)
        else:
            # No existe → INSERT
            sql_insert = """
            INSERT INTO Favoritos (Id_Usuario, IdReceta, Comentario, Calificacion, Fecha)
            VALUES (%s, %s, %s, %s, %s)
            """
            val_insert = (id_usuario, id_receta, comentario, calificacion, ahora)
            cursor.execute(sql_insert, val_insert)

        con.commit()
    finally:
        cursor.close()


def eliminar_favorito(con, id_favorito, id_usuario):

    cursor = con.cursor()

    try:
        sql = """
        DELETE FROM Favoritos
        WHERE IdFavorito = %s
          AND Id_Usuario = %s
        """
        val = (id_favorito, id_usuario)
        cursor.execute(sql, val)
        con.commit()
    finally:
        cursor.close()
