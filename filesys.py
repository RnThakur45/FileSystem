import math

# Constants from filesys.h
DISKMIN = 100000
DISKMAX = 999999
MINPRIME = 101
MAXPRIME = 99991

# Probing Policies
QUADRATIC, DOUBLEHASH, LINEAR = 0, 1, 2

class File:
    """Represents a File object with name and disk block as unique identifiers."""
    def __init__(self, name="", disk_block=0, used=False):
        self.m_name = name
        self.m_disk_block = disk_block
        self.m_used = used

    def getName(self): return self.m_name
    def getDiskBlock(self): return self.m_disk_block
    def setDiskBlock(self, block): self.m_disk_block = block

    def __eq__(self, other):
        """Equality based on name and disk block."""
        if not isinstance(other, File): return False
        return self.m_name == other.m_name and self.m_disk_block == other.m_disk_block

    def __str__(self):
        return f"{self.m_name} ({self.m_disk_block}, {self.m_used})"

class FileSys:
    """Hash table implementation using open addressing and lazy deletion."""
    def __init__(self, size, hash_fn, probing):
        self.m_hash = hash_fn
        self.m_curr_probing = probing
        self.m_current_cap = size
        self.m_current_size = 0  # Includes live and tombstones
        self.m_current_table = [None] * self.m_current_cap

    def lambda_factor(self):
        """Returns the load factor of the table."""
        return self.m_current_size / self.m_current_cap

    def insert(self, file_obj):
        """Inserts a file into the current table. Triggers rehash if load factor > 0.75."""
        if self.lambda_factor() > 0.75:
            self.rehash()

        base_idx = self.m_hash(file_obj.getName()) % self.m_current_cap
        step = 0
        while step < self.m_current_cap:
            idx = self._apply_probing(base_idx, step)
            slot = self.m_current_table[idx]

            # Slot is free or a tombstone
            if slot is None or slot == "TOMBSTONE":
                self.m_current_table[idx] = file_obj
                self.m_current_size += 1
                return True
            
            # Check for duplicate
            if slot == file_obj:
                return False
            step += 1
        return False

    def remove(self, file_obj):
        """Lazy deletion using tombstones."""
        base_idx = self.m_hash(file_obj.getName()) % self.m_current_cap
        step = 0
        while step < self.m_current_cap:
            idx = self._apply_probing(base_idx, step)
            slot = self.m_current_table[idx]
            
            if slot is None: return False
            if slot != "TOMBSTONE" and slot == file_obj:
                self.m_current_table[idx] = "TOMBSTONE"
                return True
            step += 1
        return False

    def getFile(self, name, block):
        """Retrieves a file or raises RuntimeError if not found."""
        base_idx = self.m_hash(name) % self.m_current_cap
        step = 0
        target = File(name, block)
        while step < self.m_current_cap:
            idx = self._apply_probing(base_idx, step)
            slot = self.m_current_table[idx]
            if slot is None: break
            if slot != "TOMBSTONE" and slot == target:
                return slot
            step += 1
        raise RuntimeError("File not found")

    def _apply_probing(self, base, step):
        """Handles collision resolution policies."""
        if self.m_curr_probing == QUADRATIC:
            return (base + step * step) % self.m_current_cap
        elif self.m_curr_probing == DOUBLEHASH:
            hash2 = 11 - (base % 11)
            return (base + step * hash2) % self.m_current_cap
        return (base + step) % self.m_current_cap # Linear

    def rehash(self):
        """Resizes the table to the next prime number."""
        new_cap = self._find_next_prime(self.m_current_cap * 2)
        old_table = self.m_current_table
        self.m_current_table = [None] * new_cap
        self.m_current_cap = new_cap
        self.m_current_size = 0
        for item in old_table:
            if item and item != "TOMBSTONE":
                self.insert(item)

    def _find_next_prime(self, current):
        def is_prime(n):
            if n < 2: return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0: return False
            return True
        curr = current + 1
        while curr < MAXPRIME:
            if is_prime(curr): return curr
            curr += 1
        return MAXPRIME

    def dump(self):
        """Prints the current contents of the hash table."""
        print("\n--- FileSys Dump ---")
        for i, item in enumerate(self.m_current_table):
            print(f"[{i}] : {item if item else 'Empty'}")