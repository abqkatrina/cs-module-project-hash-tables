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
class LL:
    def __init__(self):
        self.head = None

class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [LL()] * capacity
        self.items = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.data)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # find load factor
        lf =  self.items/self.capacity

        # STRETCH if lf is less than .2, make cap 1/2 cap with 8 minimum slots
        if lf < .2:
            if self.capacity/2 >= 8:
                self.capacity = self.capacity/2
                return lf
            # if 1/2 cap is less than 8, don't change
            else:
                return lf
        #STRETCH if lf is greater than .7, make cap 2cap
        elif lf > .7:
            self.capacity = self.capacity*2
            return lf
        #if lf is between .2 and .7, return lf
        return lf

        
    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.
        """
        
            # The core of the FNV-1 hash algorithm is as follows:
            # hash = offset_basis
            # for each octet_of_data to be hashed
            # hash = hash * FNV_prime
            # hash = hash xor octet_of_data
            # return hash
        
        # FNV_offset_basis = 14695981039346656037 
        FNV_prime = 1099511628211 
        hashed_key = 14695981039346656037
        byte_keys = key.encode()
        for byte in byte_keys:
            hashed_key = hashed_key * FNV_prime
            hashed_key = hashed_key ^ byte
        return hashed_key


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash_var = 5381
        byte_keys = key.encode()
        for b in byte_keys:
            hash_var = ((hash_var < 5) + hash_var) + b
        return hash_var


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    
    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        Implement this.
        """

        i = self.hash_index(key)
   
        if self.data[i].head == None:
            self.data[i].head = HashTableEntry(key, value)
            self.items += 1
            return
        else: 
            cur = self.data[i].head
            while cur.next:
                if cur.key == key:
                    cur.value = value
                cur = cur.next
            cur.next = HashTableEntry(key, value)
            self.items += 1


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        cur = self.data[i].head

        if cur.key == key:
            self.data[i].head = self.data[i].head.next
            self.items -= 1
            return

        while cur.next:
            prev = cur
            cur = cur.next
            if cur.key == key:
                prev.next = cur.next
                self.items -= 1
                return None
                
                


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        cur = self.data[i].head
        
        # if the list is empty, return none
        if cur is None:
            return None
        # if the list exists...
        else:
            # if the current item is the key, return the value
            if cur.key == key:
                return cur.value
            # if current item isn't key, check next item (if it exists)
            while cur.next:
                cur = cur.next
                if cur.key == key:
                    return cur.value
            # if the current item and next item(s) are not key, return none
            return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """

        if new_capacity < 8:
            return('no can do')
       
        self.capacity = new_capacity
        new_array = [LL()] * new_capacity

        for item in self.data:
            cur = item.head

            while cur:
                i = self.hash_index(cur.key)

                if new_array[i].head == None:
                    new_array[i].head = HashTableEntry(cur.key, cur.value)
                else:
                    node = HashTableEntry(cur.key, cur.value)
                    node.next = new_array[i].head
                    new_array[i].head = node
                cur = cur.next
            self.data = new_array




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
