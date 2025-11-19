import mysql.connector

# GUARDAR
def guardar_receta(con, datos):
    IdReceta      = datos.get("IdReceta")
    Nombre        = datos.get("Nombre")
    Descripcion   = datos.get("Descripcion")
    Ingredientes  = datos.get("Ingredientes")
    Utensilios    = datos.get("Utensilios")
    Instrucciones = datos.get("Instrucciones")
    Nutrientes    = datos.get("Nutrientes")
    Categorias    = datos.get("Categorias")
    Imagen        = datos.get("Imagen")

    cursor = con.cursor()

    try:
        if IdReceta:  
            sql = """
            UPDATE Recetas
            SET Nombre        = %s,
                Descripcion   = %s,
                Ingredientes  = %s,
                Utensilios    = %s,
                Instrucciones = %s,
                Nutrientes    = %s,
                Categorias    = %s,
                Imagen        = %s
            WHERE IdReceta    = %s
            """
            val = (
                Nombre, Descripcion, Ingredientes, Utensilios, Instrucciones, Nutrientes, Categorias, Imagen, IdReceta
            )
        else:        # INSERT
            sql = """
            INSERT INTO Recetas (
                IdReceta, Nombre, Descripcion, Ingredientes, Utensilios, Instrucciones, Nutrientes, Categorias, Imagen
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """
            val = (
                IdReceta, Nombre, Descripcion, Ingredientes, Utensilios, Instrucciones, Nutrientes, Categorias, Imagen
            )

        cursor.execute(sql, val)
        con.commit()
    finally:
        cursor.close()


def eliminar_receta(con, id_receta: int):

    cursor = con.cursor()
    try:
        sql = "DELETE FROM Recetas WHERE IdReceta = %s"
        val = (id_receta,)
        cursor.execute(sql, val)
        con.commit()
    finally:
        cursor.close()

# BUSCAR
def buscar_recetas(con, busqueda: str):
    busqueda = f"%{busqueda}%"
    cursor = con.cursor(dictionary=True)

    sql = """
    SELECT  IdReceta, Nombre, Descripcion, Ingredientes, Utensilios, Instrucciones, Nutrientes, Categorias
    FROM Recetas
    WHERE Nombre      LIKE %s
       OR Ingredientes LIKE %s
       OR Nutrientes   LIKE %s
       OR Categorias   LIKE %s
    ORDER BY IdReceta DESC
    LIMIT 10 OFFSET 0
    """
    val = (busqueda, busqueda, busqueda, busqueda)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()
    finally:
        cursor.close()

    return registros

# CATEGORIA
def buscar_por_categoria(con, categoria: str):

    cursor = con.cursor(dictionary=True)

    sql = """
    SELECT Nombre
    FROM Recetas
    WHERE Categorias = %s
    ORDER BY Nombre ASC
    LIMIT 10 OFFSET 0
    """
    val = (categoria,)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()
    finally:
        cursor.close()

    return registros

