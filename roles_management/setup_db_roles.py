import psycopg2
from psycopg2.extensions import AsIs
from psycopg2 import sql
import os

superuser = [os.environ['POSTGRES_SUPER_USER'],os.environ['POSTGRES_SUPER_PASSWORD']]
research_db = [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_PORT'],os.environ['POSTGRES_RESEARCH_DB'],os.environ['POSTGRES_RESEARCH_USER'],os.environ['POSTGRES_RESEARCH_PASSWORD']]
main_db = [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_PORT'],os.environ['POSTGRES_DB'],os.environ['POSTGRES_USER'],os.environ['POSTGRES_PASSWORD']]
auth_db= [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_PORT'],os.environ['POSTGRES_AUTH_DB'],os.environ['POSTGRES_AUTH_USER'],os.environ['POSTGRES_AUTH_PASSWORD']]

generic_role_name = "readwrite_"

def db_con(dbargs):
    conn = None
    try:
        conn = psycopg2.connect(
            host=dbargs[0],
            port=dbargs[1],
            database=dbargs[2],
            user=dbargs[3],
            password=dbargs[4]
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit(1)
    return None

def revoke_public_permissions(database):
    sql_statement = """
        REVOKE CREATE ON SCHEMA public FROM PUBLIC;
        REVOKE ALL ON DATABASE {database_name} FROM PUBLIC;
    """
    args = database[:-2] + superuser
    conn = db_con(args)
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL(
                sql_statement
            ).format(
                database_name = sql.Identifier(
                    database[2]
                )
            )
        )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cur.close()
    conn.close()

def create_db_roles(database):
    drop_sql_statement = """
        DROP OWNED BY {role_name};
        DROP ROLE if exists {role_name};
    """
    sql_statement = """
        CREATE role {role_name};
        GRANT CONNECT ON DATABASE {database_name} TO {role_name};
        GRANT USAGE, CREATE ON SCHEMA public TO {role_name};
        GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {role_name};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {role_name};
        GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {role_name};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO {role_name};
    """
    args = database[:-2] + superuser
    conn = db_con(args)
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL(
                drop_sql_statement
            ).format(
                role_name = sql.Identifier(
                    generic_role_name + database[2]
                )
            )
        )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        cur.execute("ROLLBACK")
        conn.commit()
    try:
        cur.execute(
            sql.SQL(
                sql_statement
            ).format(
                database_name = sql.Identifier(
                    database[2]
                ),
                role_name = sql.Identifier(
                    generic_role_name + database[2]
                )
            )
        )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cur.close()
    conn.close()

def create_and_grant_permission_to_user(database):
    sql_statement = """
        DROP USER if exists {user};
        CREATE USER {user} WITH PASSWORD '{password}';
        GRANT {role_name} TO {user};
    """
    args = database[:-2] + superuser
    conn = db_con(args)
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL(
                sql_statement
            ).format(
                role_name = sql.Identifier(
                    generic_role_name + database[2]
                ),
                user = sql.Identifier(
                    database[3]
                ),
                password = sql.Placeholder()
            ),
            (AsIs(database[4]),)
        )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cur.close()
    conn.close()

def main():
    # Remove permissions from public schema
    revoke_public_permissions(research_db)
    revoke_public_permissions(main_db)
    revoke_public_permissions(auth_db)
    # Create readwrite roles and link to public schema only
    create_db_roles(research_db)
    create_db_roles(main_db)
    create_db_roles(auth_db)
    # Create users and grant them readwrite roles
    create_and_grant_permission_to_user(research_db)
    create_and_grant_permission_to_user(main_db)
    create_and_grant_permission_to_user(auth_db)
    #done

if __name__ == '__main__':
    main()