import time
from pymongo import MongoClient

print("=== TASK 3 & 4: INDEXING & QUERY OPTIMIZATION ===")
print("Ensure MongoDB is running locally on port 27017")

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    db = client["ecommerce_db"]
    users = db["users"]
    orders = db["orders"]

    # --- Setup Data ---
    print("\n[Setup] Inserting dummy data...")
    users.delete_many({})
    orders.delete_many({})

    # Insert 10,000 users
    user_data = [{"user_id": i, "name": f"User_{i}", "age": 20 + (i % 40), "country": "USA" if i % 2 == 0 else "UK"} for i in range(10000)]
    users.insert_many(user_data)

    # Insert 20,000 orders
    order_data = [{"order_id": i, "user_id": i % 10000, "amount": 10 + (i % 100), "status": "shipped" if i % 3 == 0 else "pending"} for i in range(20000)]
    orders.insert_many(order_data)

    print("Data inserted: 10,000 users, 20,000 orders.")

    # --- Task 3: Indexing Techniques ---
    print("\n--- TASK 3: Indexing Performance Comparison ---")
    
    # Query without index (Collection Scan)
    print("1. Querying without index (Exact Match): db.users.find({age: 35})")
    start = time.time()
    res_no_idx = users.find({"age": 35}).explain()["executionStats"]
    print(f"Time taken (No Index): {res_no_idx['executionTimeMillis']} ms | Docs Examined: {res_no_idx['totalDocsExamined']}")

    # Create B-Tree Index
    print("\nCreating B-Tree Index on 'age'...")
    users.create_index([("age", 1)]) # 1 for ascending B-Tree

    # Query with B-Tree index
    print("2. Querying with B-Tree index (Exact Match):")
    res_btree = users.find({"age": 35}).explain()["executionStats"]
    print(f"Time taken (B-Tree): {res_btree['executionTimeMillis']} ms | Docs Examined: {res_btree['totalDocsExamined']}")

    # Create Hash Index
    print("\nCreating Hash Index on 'user_id'...")
    users.create_index([("user_id", "hashed")])

    # Query with Hash index
    print("3. Querying with Hash index (Exact Match): db.users.find({user_id: 5000})")
    res_hash = users.find({"user_id": 5000}).explain()["executionStats"]
    print(f"Time taken (Hash): {res_hash['executionTimeMillis']} ms | Docs Examined: {res_hash['totalDocsExamined']}")

    # --- Task 4: Query Optimization ---
    print("\n--- TASK 4: Query Optimization ---")
    
    pipeline = [
        {"$match": {"status": "shipped"}},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "user_id",
            "as": "user_info"
        }},
        {"$unwind": "$user_info"},
        {"$group": {
            "_id": "$user_info.country",
            "total_sales": {"$sum": "$amount"}
        }}
    ]

    print("\nExecuting complex aggregation (Join users & orders, filter, group)...")
    start_agg = time.time()
    agg_result = list(orders.aggregate(pipeline))
    end_agg = time.time()
    print(f"Aggregation Result: {agg_result}")
    print(f"Time taken: {(end_agg - start_agg) * 1000:.2f} ms")

    # Optimization: Add index on status and user_id in orders
    print("\nOptimizing... Creating indexes on orders.status and orders.user_id...")
    orders.create_index([("status", 1), ("user_id", 1)])

    start_agg_opt = time.time()
    agg_result_opt = list(orders.aggregate(pipeline))
    end_agg_opt = time.time()
    print(f"Time taken after optimization: {(end_agg_opt - start_agg_opt) * 1000:.2f} ms")

    # Cleanup
    users.drop()
    orders.drop()

except Exception as e:
    print(f"Could not connect to MongoDB or an error occurred: {e}")
