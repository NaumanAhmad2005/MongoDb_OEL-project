import pyodbc
import threading
import time

conn_str = r"DRIVER={SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=Ecommerce_Optimization;Trusted_Connection=yes"

def user_a():
    try:
        conn = pyodbc.connect(conn_str, autocommit=False)
        cursor = conn.cursor()
        print("User A: Locking Product 1...")
        cursor.execute("UPDATE Products SET Price = Price + 1 WHERE ProductID = 1")
        time.sleep(3) 
        print("User A: Trying to lock Product 2...")
        cursor.execute("UPDATE Products SET Price = Price + 1 WHERE ProductID = 2")
        conn.commit()
    except Exception as e:
        print(f"\n[USER A ERROR]: {e}") 

def user_b():
    try:
        conn = pyodbc.connect(conn_str, autocommit=False)
        cursor = conn.cursor()
        print("User B: Locking Product 2...")
        cursor.execute("UPDATE Products SET Price = Price + 1 WHERE ProductID = 2")
        time.sleep(3)
        print("User B: Trying to lock Product 1...")
        cursor.execute("UPDATE Products SET Price = Price + 1 WHERE ProductID = 1")
        conn.commit()
    except Exception as e:
        print(f"\n[USER B ERROR]: {e}")


t1 = threading.Thread(target=user_a)
t2 = threading.Thread(target=user_b)
t1.start(); t2.start()
t1.join(); t2.join()