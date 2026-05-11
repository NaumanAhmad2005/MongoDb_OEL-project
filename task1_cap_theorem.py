import time
import threading
import random

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.is_online = True

    def write(self, key, value):
        if not self.is_online:
            return False
        self.data[key] = value
        return True

    def read(self, key):
        if not self.is_online:
            return None
        return self.data.get(key, None)

class DistributedSystem:
    def __init__(self):
        self.nodes = {1: Node(1), 2: Node(2), 3: Node(3)}
        self.network_partitioned = False

    def toggle_network_partition(self):
        self.network_partitioned = not self.network_partitioned
        print(f"\n--- Network Partition: {'ON' if self.network_partitioned else 'OFF'} ---")

    def strong_consistency_write(self, key, value):
        print(f"\n[Strong Consistency] Attempting to write {key}={value}")
        success_count = 0
        for node_id, node in self.nodes.items():
            if self.network_partitioned and node_id == 3:
                print(f"Node {node_id} is unreachable (Partition).")
                continue
            if node.write(key, value):
                print(f"Node {node_id} wrote successfully.")
                success_count += 1
        
        # Require all 3 nodes for strong consistency
        if success_count == len(self.nodes):
            print("SUCCESS: Data written to all nodes.")
        else:
            print("FAILURE: Could not achieve strong consistency (Availability sacrificed).")

    def eventual_consistency_write(self, key, value):
        print(f"\n[Eventual Consistency] Attempting to write {key}={value}")
        primary_node = self.nodes[1]
        
        if primary_node.write(key, value):
            print("SUCCESS: Data written to Primary Node 1 (Available).")
            
            # Background sync
            def sync_data():
                time.sleep(1)
                for node_id in [2, 3]:
                    if self.network_partitioned and node_id == 3:
                        print(f"Background Sync: Node {node_id} unreachable.")
                    else:
                        self.nodes[node_id].write(key, value)
                        print(f"Background Sync: Node {node_id} updated.")
            
            threading.Thread(target=sync_data).start()
        else:
            print("FAILURE: Primary node down.")

    def read_all(self, key):
        print(f"\nReading '{key}' from all nodes:")
        for node_id, node in self.nodes.items():
            val = node.read(key)
            status = "Unreachable" if self.network_partitioned and node_id == 3 else f"Value={val}"
            print(f"Node {node_id}: {status}")

if __name__ == "__main__":
    system = DistributedSystem()
    
    # 1. Normal Operation (No Partition)
    print("=== NORMAL OPERATION ===")
    system.strong_consistency_write("item1", "Apple")
    system.eventual_consistency_write("item2", "Banana")
    time.sleep(2) # Wait for eventual consistency sync
    system.read_all("item2")
    
    # 2. Network Partition Occurs
    system.toggle_network_partition()
    
    # 3. Partitioned Operation
    print("\n=== OPERATION DURING PARTITION ===")
    # Strong consistency fails (chooses Consistency over Availability)
    system.strong_consistency_write("item3", "Orange") 
    
    # Eventual consistency succeeds (chooses Availability over Consistency)
    system.eventual_consistency_write("item4", "Mango")
    time.sleep(2) # Wait for sync attempt
    system.read_all("item4")
