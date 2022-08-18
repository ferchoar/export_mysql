
# Extract MySQL
Extrae datos de una base de datos MySQL/MariaDB

## Requerimientos
* Python 3.10

NOTA: Probado en versiones anteriores de python (3.6 en adelante), pero hay que cambiar las versiones de los requerimientos

## Instalación (desde git)
Clonar el repositorio
```
$ git clone git@github.com:ferchoar/export_mysql.git
```

Recomendamos usar virtualenv
```
$ cd export_mysql
$ python3 -m venv ./venv
$ . venv/bin/activate
(venv) $
```
Instalar dependencias
```
(venv) $ pip install -r requirements.txt
Collecting mysql-connector-python==8.0.30 (from -r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/94/42/5f1c4974d346ff015af67a5b1b1818487caaee60659aefd7263af3e2e52a/mysql_connector_python-8.0.30-py2.py3-none-any.whl
Collecting protobuf==3.19.4 (from -r requirements.txt (line 2))
  Using cached https://files.pythonhosted.org/packages/c6/1c/f18d97fc479b4fb6f72bbb0e41188575362e3bbd31014cf294ef0fdec8bf/protobuf-3.19.4-py2.py3-none-any.whl
(...)
Collecting typing-extensions>=3.6.4; python_version < "3.8" (from importlib-metadata; python_version < "3.8"->click~=8.0.4->-r requirements.txt (line 5))
  Using cached https://files.pythonhosted.org/packages/45/6b/44f7f8f1e110027cf88956b59f2fad776cca7e1704396d043f89effd3a0e/typing_extensions-4.1.1-py3-none-any.whl
Installing collected packages: protobuf, mysql-connector-python, pytz, numpy, six, python-dateutil, pandas, zipp, importlib-resources, tqdm, typing-extensions, importlib-metadata, click
Successfully installed click-8.0.4 importlib-metadata-4.8.3 importlib-resources-5.4.0 mysql-connector-python-8.0.30 numpy-1.19.5 pandas-1.1.5 protobuf-3.19.4 python-dateutil-2.8.2 pytz-2022.2.1 six-1.16.0 tqdm-4.64.0 typing-extensions-4.1.1 zipp-3.6.0
(venv) $ 
```
Test
```
(venv) $ python extract_mysql.py --help
Usage: extract_mysql.py [OPTIONS]

Options:
  -d, --db_config_filename TEXT   Configuración de base de datos
  -e, --extract_config_filename TEXT
                                  Configuración de extracción
  --help                          Show this message and exit.
(venv) $

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


##  (Opcional) Build para generar un ejecutable
Se genera un archivo ejecutable (para el sistema operativo donde se ejecute el comando) en el directorio "dist":
```
c:\export_test> pyinstaller --onefile extract_mysql.py
1217 INFO: PyInstaller: 5.3
1217 INFO: Python: 3.10.0
1249 INFO: Platform: Windows-10-10.0.19044-SP0
(...)
80216 INFO: Updating resource type 24 name 1 language 0
80223 INFO: Appending PKG archive to EXE
80314 INFO: Fixing EXE headers
81361 INFO: Building EXE from EXE-00.toc completed successfully.
c:\export_test> dir *.exe


    Directorio: C:\export_test


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         17/8/2022     10:38       32452114 extract_mysql.exe


c:\export_test> 
```
Si se distribuye el ejecutable no se necesita el entorno python para ejecutar.
