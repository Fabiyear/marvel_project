import sys
from api_marvel import ApiMarvel
from db_marvel import DbMarvel
from app import load_status

api_marvel = ApiMarvel()
db_marvel = DbMarvel()

type_ch = ["characters", "name"]
type_co = ["comics", "title"]

#test connection API MARVEL and get value total items
try:
    total_ch = api_marvel.check_status_api(type_ch[0])
    total_co = api_marvel.check_status_api(type_co[0])
except:
    api_marvel.api_indicate_error()
    raise
#check status characters table
status_table_ch = db_marvel.status_table(type_ch[0], total_ch)

#check comics table if exists
status_table_co = db_marvel.status_table(type_co[0], total_co)

#running process to load characters
load_status(status_table_ch, type_ch, total_ch)

#running process to load comics
load_status(status_table_co, type_co, total_co)