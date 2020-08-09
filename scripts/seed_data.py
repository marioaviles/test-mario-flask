import psycopg2
import os 

DB_USER = os.environ['DB_USER']
DB_PSW=os.environ['DB_PSW']
DB_HOST=os.environ['DB_HOST']
DB_NAME=os.environ['DB_NAME']

db_conn = psycopg2.connect(host=DB_HOST, port="5432" , dbname=DB_NAME, user=DB_USER, password=DB_PSW)
db_cursor = db_conn.cursor()

def create_database():
	db_cursor.execute("""
create table tb_restaurants (
id TEXT PRIMARY KEY, -- Unique Identifier of Restaurant
            rating INTEGER, -- Number between 0 and 4
            name TEXT, -- Name of the restaurant
            site TEXT, -- Url of the restaurant
            email TEXT,
            phone TEXT,
            street TEXT,
            city TEXT,
            state TEXT,
            lat FLOAT, -- Latitude
            lng FLOAT) -- Longitude
		""")
	db_conn.commit()

def seed_database():
	cdw = os.getcwd()
	db_cursor.execute("""
     COPY tb_restaurants FROM '{0}/restaurantes.csv' CSV HEADER DELIMITER ',';
		""".format(cdw))
	db_conn.commit()

def install_plugins():
      cdw = os.getcwd()
      db_cursor.execute("""
     CREATE EXTENSION postgis;
            """)
      db_conn.commit()

def init_geom_data():
  db_cursor.execute("""
  SELECT AddGeometryColumn('tb_restaurants', 'geom', 4326, 'POINT', 2);  
  UPDATE tb_restaurants SET geom = ST_SetSRID(ST_MakePoint(lng , lat ), 4326);  
  CREATE INDEX idx_restaruants_geoms ON tb_restaurants USING gist(geom); 
  """)
  db_conn.commit()

create_database()
print("create_database")
seed_database()
print("seed_database")
install_plugins()
print("install_plugins")
init_geom_data()
print("init_geom_data")
db_cursor.close()
