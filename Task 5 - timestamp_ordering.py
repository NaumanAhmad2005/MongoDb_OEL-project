import time

product_name = "Laptop"
inventory_count = 10
last_update_time = 0 

def purchase_attempt(user_name, arrival_time, qty):
    global inventory_count, last_update_time
    
    print(f"\n[{user_name}] arrived at {arrival_time:.2f} to buy {qty} items.")
    
    # If the user's arrival time is OLDER than the last update, they are too slow!
    if arrival_time < last_update_time:
        print(f"!!! REJECTED: {user_name}, your data is outdated. Restarting transaction.")
    else:
        # Success
        inventory_count -= qty
        last_update_time = arrival_time 
        print(f"+++ SUCCESS: {user_name} bought items. Stock left: {inventory_count}")


# 1. User 1 arrives early
purchase_attempt("User_1", 10.05, 1)

# 2. User 2 arrives even later
purchase_attempt("User_2", 10.10, 2)

# 3. User 3 tries to use 'Old Data' (Time 10.02 is earlier than the last update 10.10)
purchase_attempt("User_3", 10.02, 1)