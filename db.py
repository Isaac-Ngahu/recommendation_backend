import psycopg2


connection = psycopg2.connect(database="postgres", user="postgres", password="12976", host="localhost", port=5432)
cursor = connection.cursor()
#email,phone_number,role user table
#user_id,search,search_count
# for seller recommendations give a collection of top searches(use barcode api), and top items to sell based on top categories(use amazon data)
def get_top_searches():
    try:
        sql = "SELECT search,search_count FROM search WHERE search_count>1 ORDER BY created_at DESC LIMIT 3"
        cursor.execute(sql)
        searches = cursor.fetchall()
        if len(searches) ==0:
            return []
        else:
            return searches
    except psycopg2.IntegrityError as e:
        connection.rollback()
        print("Constraint violation:", e)
    except psycopg2.OperationalError as e:
        print("Database connection problem:", e)

def get_top_categories():
       try:
        sql = "SELECT id,search_category,category_count FROM category WHERE category_count>2 ORDER BY created_at DESC LIMIT 3"
        cursor.execute(sql)
        categories = cursor.fetchall()
        if len(categories) ==0:
            return []
        else:
            return categories
       except psycopg2.IntegrityError as e:
            connection.rollback()
            print("Constraint violation:", e)
       except psycopg2.OperationalError as e:
           print("Database connection problem:", e)  
def get_buyer_searches(user_id):
    try:
        sql = "SELECT search FROM search WHERE user_id=%s ORDER BY created_at DESC LIMIT 3"
        value = (user_id,)
        cursor.execute(sql, value)
        results = cursor.fetchall()
        search_results = [result[0] for result in results]
        return search_results
    except psycopg2.IntegrityError as e:
        connection.rollback()
        print("Constraint violation:", e)
    except psycopg2.OperationalError as e:
        print("Database connection problem:", e)

def insert_search_data(user_id,search,category):
    try:
        sql = "SELECT id,search,search_count FROM search WHERE search=%s"
        value = (search,)
        category_sql = "SELECT id,search_category,category_count FROM category WHERE search_category=%s"
        category_value = (category,)
        cursor.execute(category_sql,category_value)
        category_result = cursor.fetchone()
        cursor.execute(sql,value)
        search_result = cursor.fetchone()
        if search_result is None and category_result is None:
            sql = "INSERT INTO search (search,search_count,user_id) VALUES(%s,%s,%s) RETURNING id"
            values = (search,1,user_id)
            cursor.execute(sql,values)
            search_id = cursor.fetchone()[0]
            sql2 = "INSERT INTO category(search_category,category_count) VALUES(%s,%s) RETURNING id"
            values2 = (category,1)
            cursor.execute(sql2,values2)
            category_id = cursor.fetchone()[0]
            sql3 = "INSERT INTO search_category(search_id,category_id) VALUES(%s,%s)"
            values3 = (search_id,category_id)
            cursor.execute(sql3,values3)
            connection.commit()
            return "inserted"
        elif search_result is None and category_result is not None:
            sql = "INSERT INTO search (search,search_count,user_id) VALUES(%s,%s,%s) RETURNING id"
            values = (search,1,user_id)
            sql2 = "UPDATE category SET category_count=%s WHERE id=%s" 
            new_category_count = category_result[2] + 1
            value = (new_category_count,category_result[0])
            cursor.execute(sql2,value)
            connection.commit()
            return "inserted"
        elif search_result is not None and category_result is not None:
            sql = "UPDATE search SET search_count=%s WHERE id=%s"
            new_search_count = search_result[2] + 1
            values = (new_search_count,search_result[0])
            cursor.execute(sql,values)
            sql2 = "UPDATE category SET category_count=%s WHERE id=%s"
            new_category_count = category_result[2] + 1
            value = (new_category_count,category_result[0])
            cursor.execute(sql2,value)
            connection.commit()
            return "inserted"
    except psycopg2.IntegrityError as e:
        connection.rollback()
        print("Constraint violation:", e)
    except psycopg2.OperationalError as e:
        print("Database connection problem:", e)
    # except psycopg2.DatabaseError as e:
    #     connection.rollback()
    #     print("General database error:", e)
    
        