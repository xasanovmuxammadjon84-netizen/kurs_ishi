from django.db import connection
from contextlib import closing

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row)) for row in cursor.fetchall()
    ]

def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns,row))

def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT market_order.id, market_customer.first_name,market_customer.last_name, market_order.address, market_order.payment_type,market_order.status,market_order.created_at from market_order 
                            INNER JOIN market_customer on market_customer.id=market_order.customer_id 
                            where market_order.customer_id =%s""",[id])
        order = dictfetchall(cursor)
        return order

def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT food_orderproduct.count,food_orderproduct.price,
        food_orderproduct.created_at,food_product.title from food_orderproduct 
         INNER JOIN food_product ON food_orderproduct.product_id=food_product.id  where order_id=%s""",[id])
        orderproduct = dictfetchall(cursor)
        return orderproduct

def get_table():
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" 
        SELECT food_orderproduct.product_id, 
COUNT(food_orderproduct.product_id),food_product.title 
FROM food_orderproduct 
INNER JOIN food_product ON food_product.id=food_orderproduct.product_id 
GROUP BY food_orderproduct.product_id ,food_product.title 
order by count desc limit 10

        """)
        table = dictfetchall(cursor)
        return table