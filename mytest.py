import random
from filesys import File, FileSys, DISKMIN, DISKMAX, MINPRIME, DOUBLEHASH

def hashCode(s):
    """Replicates C++ unsigned int hash code logic."""
    val = 0
    thirty_three = 33
    for char in s:
        # Use bitwise AND to simulate 32-bit unsigned overflow
        val = (val * thirty_three + ord(char)) & 0xFFFFFFFF
    return val

def generate_colliding_key(base, modifier, table_size, hash_func):
    """Helper to find keys that hash to the same index."""
    key = base + str(modifier)
    base_hash = hash_func(base) % table_size
    while (hash_func(key) % table_size) != base_hash:
        modifier += 1
        key = base + str(modifier)
    return key, modifier

class TestRandom:
    def __init__(self, low, high, seed=10):
        self.rng = random.Random(seed)
        self.low = low
        self.high = high
    def getRandNum(self):
        return self.rng.randint(self.low, self.high)

def main():
    names_db = ["driver.cpp", "test.cpp", "test.h", "info.txt", "mydocument.docx", "tempsheet.xlsx"]
    rnd_id = TestRandom(DISKMIN, DISKMAX)
    rnd_name = TestRandom(0, 5)
    
    fs = FileSys(MINPRIME, hashCode, DOUBLEHASH)
    data_list = []

    # --- Test 1: Non-colliding keys ---
    print("Testing with non-colliding keys...")
    i = 0
    while i < 10:
        name = names_db[rnd_name.getRandNum()]
        block = rnd_id.getRandNum()
        data_obj = File(name, block, True)
        if any(f.getDiskBlock() == block for f in data_list): continue
        data_list.append(data_obj)
        fs.insert(data_obj)
        i += 1
    
    fs.dump()

    # --- Test 2: Forced Collisions ---
    print("\nTesting with colliding keys (same block, different names):")
    c1 = File("collision1.txt", DISKMIN, True)
    c2 = File("collision2.txt", DISKMIN, True)
    result = fs.insert(c1) and fs.insert(c2)
    print("Test 2 Result: SUCCESS" if result else "FAILED")

    # --- Test 3 & 4: Removal ---
    print("\nTesting removal logic...")
    rm_success = fs.remove(c1)
    try:
        fs.getFile(c1.getName(), c1.getDiskBlock())
        rm_success = False
    except RuntimeError:
        pass # Expected
    print("Removal Test: PASSED" if rm_success else "FAILED")

    # --- Test 5: Rehashing ---
    print("\nTEST 5: Rehashing Check...")
    # Insert more items until load factor triggers rehash
    for j in range(70):
        f = File(f"extra_{j}.txt", 200000 + j, True)
        fs.insert(f)
    
    if fs.m_current_cap > MINPRIME:
        print(f"PASSED: Rehash occurred. New capacity: {fs.m_current_cap}")
    else:
        print("FAILED: Rehash did not occur.")

    # --- Test 6: Mixed Operations ---
    print("\nTEST 6: Mixed Operations...")
    mixed_file = File("mixed.txt", 300000, True)
    fs.insert(mixed_file)
    fs.remove(mixed_file)
    try:
        fs.getFile("mixed.txt", 300000)
        print("Test 6 FAILED: File still exists.")
    except RuntimeError:
        print("Test 6 PASSED: Mixed operations verified.")

if __name__ == "__main__":
    main()