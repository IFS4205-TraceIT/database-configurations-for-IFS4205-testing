import psycopg2
from faker import Faker
import random
import string
import uuid
import os
import sys

database_folder = os.getcwd() + '/database_sql/'
database_file = "traceit_mainsystem_createtable.sql"
basefolder = os.getcwd() + '/sampledata/'
relation_file = "generate_relations.sql"

db = [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_PORT'],os.environ['POSTGRES_DB'],os.environ['POSTGRES_USER'],os.environ['POSTGRES_PASSWORD'],os.environ['POSTGRES_SSL_CERT'],os.environ['POSTGRES_SSL_KEY'],os.environ['POSTGRES_SSL_ROOT_CERT']]

insert_user_sql = """
    INSERT INTO users values(%s,%s,%s,%s,%s,%s,%s,%s,%s);
"""

insert_vaccine_sql = """
    INSERT INTO vaccinationtypes(name,start_date) values(%s,%s);
"""

insert_building_sql = """
    INSERT INTO buildings(id, name,location) values(%s,%s,%s);
"""

def user_generate(conn, total):
    fake = Faker()
    cur = conn.cursor()
    for x in range(total):
        name = fake.name()
        dob = fake.date_of_birth(None,0,100)
        email = name.lower().replace(" ", "")+"@"+fake.domain_name()
        phone = fake.pyint(80000000,99999999)
        gender = random.choice(["Male","Female"])
        address = fake.street_address()
        postal_code = str(random.randint(1, 80)).rjust(2, "0") + str(random.randint(1, 9999)).rjust(4, "0")
        nric = ('T' if dob.year > 2000 else 'S')+str(dob)[2:4] + str(random.randint(1, 99999)).rjust(5, "0") + random.choice(string.ascii_letters).upper()
        id = str(uuid.uuid4())
        try:
            cur.execute(insert_user_sql,(id,nric,name,dob,email,phone,gender,address,postal_code))
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("ROLLBACK")
            conn.commit()
            print(error)
        conn.commit()
    cur.close()

def vaccine_generate(conn):
    cur = conn.cursor()
    list_of_vaccines = [
        ["Pfizer-BioNTech",'2020-12-21'],
        ["Moderna",'2021-02-17'],
        ["Sinovac",'2021-10-23'],
        ["Novavax",'2022-02-14']
    ]
    for each in list_of_vaccines:
        try:
            cur.execute(insert_vaccine_sql,(each[0],each[1]))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    conn.commit()
    cur.close()

def building_generate(conn):
    cur = conn.cursor()
    list_of_buildings = [
        ['Bugis Junction',188024],
        ['Far East Plaza',228213],
        ['ION Orchard',238801],
        ['Bedok Mall',467360],
        ['NEX',556083],
        ['JCube',609731],
        ['Rivervale Mall',545082],
        ['Paya Lebar Square',409051],
        ['Rochester Mall',138639],
        ['IMM',609601]
    ]
    for each in list_of_buildings:
        try:
            id = str(uuid.uuid4())
            cur.execute(insert_building_sql,(id,each[0],each[1]))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    conn.commit()
    cur.close()

def execute_sql(conn, filename):
    sql_file = open(filename)
    sql_as_string = sql_file.read()
    cursor = conn.cursor()
    cursor.execute(sql_as_string)
    conn.commit()

def db_con(dbargs):
    conn = None
    try:
        conn = psycopg2.connect(
            host=dbargs[0],
            database=dbargs[2],
            user=dbargs[3],
            password=dbargs[4],
            sslmode="verify-ca",
            sslcert=dbargs[5],
            sslkey=dbargs[6],
            sslrootcert=dbargs[7]
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None

def main():

    if(len(sys.argv) <= 1):
        print("ERROR: Please specify the total user to be generated.\n")
        exit(1)
    
    try:
        total_user = int(sys.argv[1])
        if total_user <= 0:
            print('ERROR: Please enter an integer > 0 for the total user to be generated\n')
            exit(1)
    except ValueError:
        print('ERROR: Please enter an integer for the total user to be generated\n')
        exit(1)


    conn = db_con(db)
    if(conn == None):
        exit(1)

    # Generate initial tables
    # execute_sql(conn, database_folder + database_file)
    print("Generating primaries...")
    # Generate data for primary tables
    user_generate(conn, total_user)
    vaccine_generate(conn)
    building_generate(conn)
    print("Generating relations...")
    # Generate secondary tables data
    execute_sql(conn, basefolder + relation_file)
    conn.close()
    

if __name__ == '__main__':
    main()
