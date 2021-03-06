class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here

        self.capacity = capacity
        self.storage = [None] * capacity
        self.item = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        # item count / total capacity
        """
        return self.item / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.

        FNV_prime is the 64-bit FNV prime value: 1099511628211
        FNV_offset_basis is the 64-bit FNV offset basis value: 14695981039346656037

        algorithm fnv-1a is
    hash := FNV_offset_basis

    for each byte_of_data to be hashed do
        hash := hash XOR byte_of_data
        hash := hash × FNV_prime

        """
        encodedKey = str(key).encode()
        hash = 14695981039346656037
        FNV_PRIME = 1099511628211

        for byte_of_data in encodedKey:
            hash *= FNV_PRIME
            hash ^= byte_of_data
            hash &= 0xffffffffffffffff

        return hash


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        #return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.

        if load factor is bigger than .7, double capacity
        

    return hash
        """
        # Your code here
        #Get index of key#
        index = self.hash_index(key)
        current = self.storage[index]

        while current is not None and current.key != key:
            current = current.next
        if current is not None:
            current.value = value
        else:
            # insert the key and value at the had of the linked list at that index 
            new_entry = HashTableEntry(key, value)
            new_entry.next = self.storage[index]
            self.storage[index] = new_entry
            self.item += 1
        if self.get_load_factor() >= .7:
            self.resize(self.capacity * 2)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.
        
        Implement this.

        if less than .2 shrink by half (stretch)
        """
        if self.get_load_factor() <= .2:
            if self.capacity // 2 > MIN_CAPACITY:
                self.resize(self.capacity // 2)
            else:
                self.resize(MIN_CAPACITY)

        index = self.hash_index(key)
        cur = self.storage[index]
        prev = None
        # Special case, empty head

        # Special case, delete head
        if cur.key == key:
            self.storage[index] = cur.next
            return cur

        while cur.next != None and cur.key != key:
            prev = cur
            cur = prev.next
        if cur == None:
            return None

        else:
            if prev == None:
                self.storage[index] = cur.next
            else:
                prev.next = cur.next


            if cur.next == key:
                deleted_node = cur.next
                cur.next = cur.next.next
                return deleted_node
            else:
                cur = cur.next
        return None


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        current = self.storage[index]

        while current != None:
            if current.key == key:
                return current.value
            current = current.next


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.

        # take in a new capacity
        # update current capacity -> new capacity
        # save old storage as a variable
        # update storage [None] * new capacity
        # iterate through old storage, within iterate through each linked list and call put
        # update item count
        
        """
        old_storage = self.storage
        self.item = 0
        self.capacity = new_capacity
        self.storage = [None] * new_capacity
        for node in old_storage:
            while node != None:
                self.put(node.key, node.value)
                node = node.next
                





if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
