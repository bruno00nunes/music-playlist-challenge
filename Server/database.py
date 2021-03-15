from config import config
import psycopg2

dbParams = config('postgresql')


# ===================
#  Database Functions
# ===================


def fetch_from_table(table, field_value=None, field_name="ID"):
    """SELECT FROM A TABLE
    Parameters
    ----------
    table : str
        Name of the table to fetch from
    field_value : str
        Value that will filter
    field_name : str
        Name of column to filter by
    """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**dbParams)

        # create a cursor
        cur = conn.cursor()

        condition = f'where "{field_name}" = {field_value}' if (field_value is not None) else ''

        query = f'SELECT * FROM public."{table}" {condition}'

        # execute a statement
        cur.execute(query)
        results = extract_from_cursor(cur)

        cur.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []
    finally:
        if conn is not None:
            conn.close()


def insert_into_table(table, inserted):
    """DYNAMIC INSERT INTO A TABLE
    Parameters
    ----------
    table : str
        Name of the table to insert into
    inserted : dict
        A dictionary consisted of Column names as keys, and Column Value as values
    """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**dbParams)

        # create a cursor
        cur = conn.cursor()

        field_names = '"' + '", "'.join(inserted.keys()) + '"'
        field_values = tuple(inserted.values())

        # This is really weird, need this workaround because psycopg2 doesn't allow to add the values
        # Directly into the query, must pass them as a tuple in the parameters of cursor.execute()
        value_placeholders = ""
        x = len(field_values)
        for n in range(x):
            value_placeholders += "%s"
            if n < x-1:
                value_placeholders += ", "

        query = f'INSERT INTO public."{table}"({field_names}) VALUES({value_placeholders}) RETURNING "ID";'

        # execute a statement
        cur.execute(query, field_values)
        inserted_id = cur.fetchone()[0]

        inserted = fetch_from_table(table, inserted_id, "ID")

        conn.commit()
        cur.close()
        return inserted
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []
    finally:
        if conn is not None:
            conn.close()


def execute_query(query, values=None):
    """EXECUTE A QUERY (USED ON UPDATES AND DELETES)
    Parameters
    ----------
    query : str
        Query to be executed
    values : tuple
        A tuple consisted of values to be used on the query
    """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**dbParams)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        if values is None:
            cur.execute(query)
        else:
            cur.execute(query, values)
            conn.commit()

        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()


def fetch_from_query(query):
    """SELECT FROM A QUERY (USED IF MULTIPLE FILTERS ARE NEEDED)
    Parameters
    ----------
    query : str
        Query to be executed
    """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**dbParams)

        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        results = extract_from_cursor(cur)

        cur.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []
    finally:
        if conn is not None:
            conn.close()


def extract_from_cursor(cur):
    """EXTRACT VALUES FROM A CURSOR INTO A DICTIONARY (Column, Value)
    Parameters
    ----------
    cur : cursor
        Cursor to extract the dictionary from
    """
    results = []
    column_names = [desc[0] for desc in cur.description]

    for fetched_item in cur.fetchall():
        item = {}
        count = 0

        for value in fetched_item:
            item[column_names[count]] = value
            count += 1

        results.append(item)
    return results
