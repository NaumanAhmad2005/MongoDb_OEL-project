# Advanced Database Management Systems (ADBMS) - Open-Ended Lab (OEL)
**Submitted By:** [Your Name/ID]  
**Course:** Advanced Database Management Systems (ADBMS)  

---

## 1. Introduction
Modern database systems must handle vast amounts of data while maintaining high availability, consistency, and efficient query performance. In this Open-Ended Lab, we simulate a database infrastructure upgrade for a growing e-commerce company. We tackled these requirements by exploring the CAP theorem tradeoffs, implementing MongoDB Replication for High Availability, applying Indexing techniques (B-Tree and Hash) for query optimization, handling Concurrency Control, and extracting business value using Data Mining (Classification and Association Rules).

---

## 2. Task-by-Task Implementation

### Task 1: CAP Theorem Simulation
**Concept:** The CAP theorem proves that a distributed database can only provide Consistency, Availability, or Partition Tolerance—never all three simultaneously.
**Implementation:** A Python simulation was created mimicking 3 distributed nodes. 
*   **Strong Consistency** was achieved by waiting for all nodes to acknowledge the write. 
*   **Eventual Consistency** was achieved by writing to the Primary node immediately and syncing in the background. 
*   When a **Network Partition** was triggered, the system chose Availability over Consistency in the Eventual scenario, and failed writes in the Strong Consistency scenario.
*(Insert Screenshot of `task1_cap_theorem.py` execution here)*

### Task 2: MongoDB Replication
**Concept:** Replication ensures High Availability. If the primary database goes offline, a secondary node automatically takes over.
**Implementation:** A Docker-Compose configuration was used to launch a 3-node MongoDB Replica Set (`rs0`). We initialized the cluster and tested failover by deliberately shutting down the `mongo1` container. The remaining nodes automatically held an election and promoted a secondary node to Primary.
*(Insert Screenshot of MongoDB Replica Set `rs.status()` and failover here)*

### Task 3: Indexing Techniques
**Concept:** Indexing reduces the number of documents a database must scan to find data.
**Implementation:** Using PyMongo, we generated 10,000 dummy users. We then tested exact match queries. 
*   A **B-Tree Index** was created on the `age` field.
*   A **Hashed Index** was created on the `user_id` field.
Execution times were measured using `.explain("executionStats")`. The results show a massive drop in execution time and `totalDocsExamined` when using indexes compared to a collection scan.
*(Insert `task3_indexing_graph.png` here)*
*(Insert Screenshot of PyMongo terminal output here)*

### Task 4: Query Optimization
**Concept:** Complex queries (like joins and aggregations) can bottleneck a system. Restructuring and compound indexes optimize these paths.
**Implementation:** An aggregation pipeline was built to `$lookup` (join) the 20,000 orders collection with the 10,000 users collection, `$unwind` the array, and `$group` total sales by country. We then optimized this by applying a compound index on the `status` and `user_id` fields.
*(Insert `task4_optimization_graph.png` here)*

### Task 5: Concurrency Control
**Concept:** Concurrency control prevents data corruption when multiple transactions access the same data simultaneously.
**Implementation:** A Python script was developed to simulate:
1.  **Lock-Based Protocol (2PL):** Showcased thread locking and intentionally triggered a deadlock (Tx1 locks A waiting for B; Tx2 locks B waiting for A), which the system detected and resolved by aborting the transaction.
2.  **Timestamp Ordering:** Demonstrated transaction rejection when an older transaction attempted to write after a newer transaction had already updated the value.
*(Insert Screenshot of `task5_concurrency.py` execution here)*

### Task 6: Data Warehousing & Mining
**Concept:** Transforming raw data into structured schemas to predict trends and discover shopping patterns.
**Implementation:** A Star Schema was conceptually implemented via a Pandas DataFrame (Sales Fact Table). 
*   **Classification:** A Decision Tree model was trained using `scikit-learn` to predict laptop purchases based on age/income, achieving ~66% accuracy.
*   **Association Rules:** The Apriori algorithm (`mlxtend`) mined frequent itemsets, discovering rules such as "Customers who buy keyboards always buy laptops (100% confidence)".
*(Insert Screenshot of `task6_data_mining.py` execution here)*

---

## 3. Challenges Faced & Solutions
1.  **Simulating Distributed Network Partitions locally:** Testing the CAP theorem required simulating node failures. *Solution:* Built a lightweight Python class network emulator that artificially drops connections to specific node IDs.
2.  **Deadlock resolution:** Standard Python threads will hang forever during a deadlock. *Solution:* Implemented a timeout mechanism on the lock acquisition. If a lock isn't acquired within 2 seconds, the transaction aborts itself and rolls back to resolve the deadlock.
3.  **MongoDB Environment Setup:** Configuring local replica sets is complex without multiple servers. *Solution:* Used Docker and Docker-Compose to containerize three MongoDB instances and map them to a virtual replica set network.

---

## 4. Conclusion
This lab successfully bridged the gap between theoretical ADBMS concepts and practical engineering. Implementing replication, tuning queries via indexes, handling transactional deadlocks, and extracting business intelligence through machine learning provided a holistic view of modern data infrastructure management. These optimizations are critical for ensuring our e-commerce platform can scale efficiently without data loss or downtime.
