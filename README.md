File System Hash Table Implementation

This project implements a simulated file system management tool using a hash table with multiple collision-handling strategies.

The system efficiently stores and manages file records while supporting dynamic resizing, lazy deletion, and multiple probing policies to handle collisions.

🚀 Project Overview

The system stores File objects that are uniquely identified by a combination of:

    File name

    Disk block number

To manage these records efficiently, the FileSys class implements a hash table that supports:

    Multiple collision resolution strategies

    Lazy deletion using tombstones

    Automatic rehashing when the load factor becomes too high

This design ensures efficient insertion, search, and deletion, even under heavy collision scenarios.

⭐ Core Features
🪦 Lazy Deletion (Tombstones)

    Deleted entries are not physically removed from the table.

    Instead, they are marked as tombstones.

    This preserves probe chains and ensures that future searches remain correct.

🔄 Dynamic Rehashing

    When the load factor (λ) exceeds 0.75, the table automatically resizes.

    The new table size is chosen as the next prime number, approximately double the current capacity.

    All active (non-deleted) records are reinserted into the new table.

🔍 Multiple Probing Policies

The hash table supports three collision resolution strategies:

    Linear Probing
    Sequentially checks the next available slot.

    Quadratic Probing
    Uses offsets of the form step² to reduce primary clustering.

    Double Hashing
    Applies a secondary hash function to compute the step size, minimizing clustering even further.

🗂️ File Structure
filesys.py

Contains the core implementation of the file system.

    File class

        Stores file metadata such as:

        File name

        Disk block

        Usage status (active or deleted)

    FileSys class

        Implements the hash table

        Supports:

        Insertion

        Removal (lazy deletion)

        File lookup (getFile)

        Dynamic rehashing

        Multiple probing strategies

mytest.py

    Provides a testing and validation suite.

    Random class

    Generates repeatable pseudorandom data for consistent testing

    main() function

    Tests non-colliding insertions

    Forces collisions to verify probing behavior

    Validates correct retrieval of files

    Ensures rehashing triggers at the correct load factor

🧠 Key Concepts Demonstrated

    Hash table design

    Collision resolution techniques

    Lazy deletion using tombstones

    Load factor–based resizing

    Prime-sized table optimization

🛠️ Technologies Used

    Python 3

    Object-Oriented Programming

    Hashing and probing algorithms

📌 Notes


This project is designed for educational purposes, making it a strong demonstration of data structure implementation and performance-aware design.
