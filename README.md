# Advanced Database Management Systems (ADBMS) - Open-Ended Lab (OEL)

This repository contains the complete implementation for the ADBMS Open-Ended Lab. The project focuses on bridging the gap between theoretical database concepts and practical engineering by simulating real-world scenarios for a scaling e-commerce platform.

## 🚀 Project Overview
We simulated a database infrastructure upgrade, tackling challenges related to distributed systems, high availability, performance optimization, concurrency, and business intelligence.

## 🛠️ Prerequisites
To run all the simulations and scripts in this repository, you will need:

### 1. Software
- **Python 3.8+**
- **Docker & Docker Compose** (for MongoDB Replication)
- **MongoDB** (running locally on port 27017 for indexing/optimization tasks)

### 2. Python Libraries
Install the required dependencies via pip:
```bash
pip install pymongo pandas scikit-learn mlxtend matplotlib
```

---

## 📂 Task Breakdown & Implementation

### Task 1: CAP Theorem Simulation
- **File:** `task1_cap_theorem.py`
- **Objective:** Demonstrate the trade-offs between Consistency, Availability, and Partition Tolerance.
- **Implementation:** A Python-based distributed system emulator that simulates network partitions and compares **Strong Consistency** vs. **Eventual Consistency** behaviors.

### Task 2: MongoDB Replication (High Availability)
- **File:** `task2_replication_setup.sh`
- **Objective:** Implement a 3-node MongoDB Replica Set to ensure zero downtime.
- **Implementation:** A shell script that generates a `docker-compose.yml` and provides step-by-step instructions for initialization and failover testing.

### Task 3: Indexing Techniques
- **File:** `task3_4_mongo_queries.py`
- **Objective:** Compare query performance using different indexing strategies.
- **Implementation:** Measures execution time and document scans for **Collection Scans**, **B-Tree Indexes**, and **Hashed Indexes** on a dataset of 10,000 users.

### Task 4: Query Optimization
- **File:** `task3_4_mongo_queries.py`
- **Objective:** Optimize complex joins and aggregations.
- **Implementation:** Demonstrates a `$lookup` aggregation between users and orders, optimized using **Compound Indexes** on the `status` and `user_id` fields.

### Task 5: Concurrency Control
- **File:** `task5_concurrency.py`
- **Objective:** Prevent data corruption in multi-transactional environments.
- **Implementation:** Simulates:
  - **Lock-Based Protocol (2PL):** With deadlock detection and resolution.
  - **Timestamp Ordering:** Preventing "late writes" by older transactions.

### Task 6: Data Warehousing & Mining
- **File:** `task6_data_mining.py`
- **Objective:** Extract business value from raw data.
- **Implementation:**
  - **Classification:** Uses a Decision Tree (`scikit-learn`) to predict customer purchases.
  - **Association Rules:** Uses the Apriori algorithm (`mlxtend`) to find frequent itemsets (e.g., "Customers who buy mice also buy keyboards").

---

## 📊 Performance Outcomes
The project includes a visualization script `generate_graphs.py` which produces:
- **`task3_indexing_graph.png`**: Visual comparison of indexing speeds.
- **`task4_optimization_graph.png`**: Impact of compound indexing on aggregation performance.

---

## 📈 Key Learnings
1. **CAP Trade-offs:** Understood that no distributed system can achieve both 100% consistency and 100% availability during a network failure.
2. **Indexing Power:** Observed that proper indexing can reduce query times from milliseconds to sub-milliseconds, even on small datasets.
3. **Concurrency is Hard:** Learned how circular wait conditions cause deadlocks and how timeout mechanisms can resolve them.
4. **Predictive Power:** Demonstrated how simple machine learning models can turn transaction logs into actionable marketing insights.

---

## 📝 Final Report
A comprehensive report template is available in `Final_Report_Template.md`, which contains detailed explanations and placeholders for execution screenshots.
