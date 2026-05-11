import time
import threading

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.value = 0

def lock_based_transaction(tx_id, res1, res2):
    print(f"Tx {tx_id}: Attempting to lock {res1.name}")
    res1.lock.acquire()
    print(f"Tx {tx_id}: Locked {res1.name}")
    time.sleep(1) # Simulate work and force interleaving
    
    print(f"Tx {tx_id}: Attempting to lock {res2.name}")
    if res2.lock.acquire(timeout=2): # Timeout prevents infinite deadlock for demo
        print(f"Tx {tx_id}: Locked {res2.name}")
        res1.value += 10
        res2.value -= 10
        print(f"Tx {tx_id}: Successfully updated resources.")
        res2.lock.release()
    else:
        print(f"Tx {tx_id}: DEADLOCK DETECTED! Aborting transaction to resolve.")
    
    res1.lock.release()
    print(f"Tx {tx_id}: Released locks.")

class TimestampOrdering:
    def __init__(self):
        self.read_ts = 0
        self.write_ts = 0
        self.value = 100

    def write(self, tx_id, tx_ts):
        if tx_ts < self.read_ts or tx_ts < self.write_ts:
            print(f"Tx {tx_id} (TS:{tx_ts}): Aborted (Timestamp ordering violated)")
        else:
            print(f"Tx {tx_id} (TS:{tx_ts}): Successfully wrote value")
            self.write_ts = tx_ts

    def read(self, tx_id, tx_ts):
        if tx_ts < self.write_ts:
            print(f"Tx {tx_id} (TS:{tx_ts}): Aborted (Read too late)")
        else:
            print(f"Tx {tx_id} (TS:{tx_ts}): Successfully read value")
            self.read_ts = max(self.read_ts, tx_ts)

if __name__ == "__main__":
    print("=== SIMULATING LOCK-BASED PROTOCOL (With Deadlock Handling) ===")
    rA = Resource("A")
    rB = Resource("B")
    
    # Force deadlock: Tx1 locks A then B, Tx2 locks B then A
    t1 = threading.Thread(target=lock_based_transaction, args=(1, rA, rB))
    t2 = threading.Thread(target=lock_based_transaction, args=(2, rB, rA))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("\n=== SIMULATING TIMESTAMP ORDERING ===")
    ts_resource = TimestampOrdering()
    
    # Tx1 (Older) and Tx2 (Newer)
    ts_resource.read(tx_id=1, tx_ts=10)
    ts_resource.write(tx_id=2, tx_ts=20)
    
    # Tx1 tries to write after Tx2 has already written (Late Write)
    ts_resource.write(tx_id=1, tx_ts=10)
