import json
import logging
from api_marvel import ApiMarvel
from db_marvel import DbMarvel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

api_marvel = ApiMarvel()
db_marvel = DbMarvel()

limit = 100

def load_status(load_parameters, type, total):
    if load_parameters == "OK":

        logging.info(f"complete table {type[0]}")

    elif load_parameters[0] == "NOK":
        # load table
        write_table(type[0], total, type[1], limit, load_parameters)

    elif load_parameters[0] == "START":
        # create table characters
        db_marvel.create_table(type[0])
        # load table
        write_table(type[0], total, type[1], limit, load_parameters)
    else:
        logging.error("please check your code status_table_ch")


def write_table(type, total, object_mrv, limit, load_parameters):

    id_seq = load_parameters[1]
    offset = load_parameters[2]
    index = load_parameters[3]

    for x in range(total):
      response = api_marvel.get_data(offset, limit, type)
      data = json.loads(response.text)
      index = index

      if offset + index + 1 <= total:
        for i in data['data']['results']:
          id_marvel = (data['data']['results'][index]['id'])
          name = (data['data']['results'][index][object_mrv])
          db_marvel.insert_table(id_seq, name, id_marvel, type, offset, index)
          logging.info(f"id_seq: {id_seq}"
                       f" name: {data['data']['results'][index][object_mrv]}"
                       f" id_marvel: {data['data']['results'][index]['id']}"
                       f" type: {type} "
                       f" offset: {offset}"
                       f" index: {index}")
          if index == 99:
              index = 0
              offset = offset + 100
          else:
              index = index + 1
          id_seq = id_seq + 1
      else:
        logging.info(f"finish process to {type}, total rows {id_seq - 1} in table.")
        db_marvel.insert_table_obt(type)
        break