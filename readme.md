
# Extract MySQL
Extrae datos de una base de datos MySQL/MariaDB

##  (Opcional) Build (para generar un ejecutable)
Se genera un archivo ejecutable (para el sistema operativo donde se ejecute el comando) en el directorio "dist":
```
c:\> pyinstaller --onefile extract_mysql.py
```

## Configuración
Se usan 2 archivos de configuración. Sus nombres por default (si no se especifica lo contrario) 
son **db_config.json** y **extract_config.json**
* db_config.json: contiene la configuración de la base de datos, en formato json

Ejemplo:
```
{
    "db_host": "localhost",
    "db_port": "3306",
    "db_db": "myDB",
    "db_user": "data_user",
    "db_pass": "password"
}
```
* extract_config.json: contiene la configuración de la extracción, en un formato de array json.
  * tabla: Si se define el campo "fields", es el nombre de la tabla. Si no, puede ser un nombre identificador.
  * fields (opcional): Array conteniendo los campos a exportar. Si no existe este parámetro, se toman todos los campos (de la misma manera que si se usa el valor "[*]") 
  * query (opcional): Query a ejecutar para generar los datos de la extracción. 
  * file (opcional): Nombre del archivo csv a generar. Si no existe este parámetro, usa el nombre de la tabla.


Ejemplo:
* La tabla "ventas" se exporta completa a un archivo llamado ventas.csv
* De la tabla productos se exportan solo los 3 campos explicitados y se genera un archivo llamado productos_completo.csv
* De la tabla usuarios se exportan todos los campos a un archivo llamado usuarios.csv
* Se genera un archivo llamado listado_de_descuentos.csv que tiene el resultado del query
```
[
{
    "tabla": "ventas"
}, {
    "tabla": "productos",
    "fields": ["id", "nombre", "categoria"],
    "file": "productos_completo.csv"
}, {
    "tabla": "usuarios",
    "fields": ["*"],
    "file": "usuarios.csv"
}, {
    "tabla": "descuentos",
    "query": "select dd.* from discount_data dd join discount_day dy on (dd.id_discount = dy.id_discount) where discount_date > '2022-01-01'",
    "file": "listado_de_descuentos.csv"
}
]
```

## Ejecución
```
c:\export_test> python extract_mysql.py     
Tabla prueba_query_json_plano: 100%|██████████████████| 12/12 [00:06<00:00,  1.91it/s]
c:\export_test> dir *.csv


    Directorio: C:\export_test


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         12/8/2022     17:36          37648 productos_completo.csv
-a----         12/8/2022     17:36         354604 ventas.csv
-a----         12/8/2022     17:36          18859 usuarios.csv
-a----         12/8/2022     17:36          14606 listado_de_descuentos.csv
```