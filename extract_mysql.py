import csv
import mysql.connector
import pandas as pd
import json
import click
from tqdm import tqdm
from time import sleep
from typing import Dict


def conn_db(config):
    mydb = mysql.connector.connect(
        host=config["db_host"],
        port=config["db_port"],
        user=config["db_user"],
        database=config["db_db"],
        password=config["db_pass"]
    )
    return mydb


def get_data(db_conn, config):
    """
    Obtiene los datos (en función de la configuración) de la base de datos

    :param db_conn: Conexión a base de datos
    :param config: Configuración
    :type config: Dict
    :return: Diccionario de python con los datos extraidos de la base de datos
    :rtype: Dict
    """
    mycursor = db_conn.cursor(dictionary=True)

    if "fields" in config.keys():
        sentence = "select "+",".join(config["fields"]) + ' from '+config["tabla"]
    elif "query" in config.keys():
        # print('=>NotYet!')
        # exit(1)
        sentence = config["query"]
    else:
        sentence = "select * from "+config["tabla"]
        # print(f"=>No 'fields' or 'query' in config for table {config['tabla']}")
        # exit(1)

    mycursor.execute(sentence)
    # Opcion 1: Solo devuelve el nombre de las columnas si el cursor tiene está definido con "dictionary=True"
    myresult = mycursor.fetchall()

    # Opcion 2: Devuelve siempre los nombres de las columnas, pero es complejo de leer
    # columns = mycursor.description
    # myresult = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]

    # print(sentence)
    # print(myresult)
    # exit(1)
    mycursor.close()
    return myresult


def save_csv(dict_data: Dict, config: Dict):
    """
    Genera un archivo csv a partir del diccionario pasado por parámetro

    :param dict_data: diccionario de python con los datos
    :param config: configuración
    """
    df = pd.DataFrame.from_dict(dict_data)
    # print(df)
    # exit(1)
    # df.to_csv('lalala.csv', index=False)
    if "file" in config.keys():
        out_filename = config["file"]
    else:
        out_filename = config["tabla"]+'.csv'
    df.to_csv(path_or_buf=out_filename, index=False, header=True,
              encoding='utf-8', sep='|', mode='w+',
              quoting=csv.QUOTE_NONE, escapechar="\\"
              # quotechar='"', quoting=csv.QUOTE_NONNUMERIC
              )
    # print('NotYet!')


@click.command()
@click.option('-d', '--db_config_filename', type=str, default='db_config.json',
              help='Configuración de base de datos')
@click.option('-e', '--extract_config_filename', type=str, default='extract_config.json',
              help='Configuración de extracción')
def main(db_config_filename='db_config.json', extract_config_filename='extract_config.json'):

    # Chequeo que los archivos existan:
    files_to_check = [db_config_filename, extract_config_filename]
    for filename in files_to_check:
        try:
            file = open(filename)
            file.close()
        except FileNotFoundError:
            print(f"Archivo {filename} no encontrado.")
            exit(1)

    # todo: chequear en algún lado que sean archivos json reales... y eventualmente que no estén malformados!
    # Leo la configuración de extracción
    with open(extract_config_filename) as F:
        extract = json.load(F)

    # leo la configuración de base de datos
    with open(db_config_filename) as F:
        config_db = json.load(F)

    # Conecto con la DB
    conn = conn_db(config_db)
    # print(conn)

    pbar = tqdm(total=len(extract))
    # Por cada entrada en la configuración
    for tabla in extract:
        # print("Procesando tabla", tabla["tabla"])
        pbar.set_description(f'Tabla {tabla["tabla"]}')
        pbar.update(1)
        pbar.refresh()
        data = get_data(db_conn=conn, config=tabla)
        save_csv(dict_data=data, config=tabla)
        sleep(.5)
    pbar.close()


if __name__ == "__main__":
    main()
