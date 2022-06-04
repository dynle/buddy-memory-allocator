# Buddy Memory Allocator

<p align="center">
  <img width="700" alt="Screen Shot 2022-06-04 at 2 35 43 PM" src="https://user-images.githubusercontent.com/36508771/171986046-112731a5-0b46-422f-bf50-1c3069c7b09e.png">
</p>
Buddy memory allocator is a memory allocation algorithm that divides memory into partitions to try to satisfy a memory request as suitably as as possible *[Wikipedia](https://en.wikipedia.org/wiki/Buddy_memory_allocation). This program allows 64 blocks to be allocated and deallocated, and it correctly merges freed blocks. Each time the program splits a block, it adds a ’|’ to show where the split happened. ’-’ represents free blocks, and ’#’ represents in-use blocks. The two numbers printed out as in 0/4 represent the beginning address and number of blocks in a chunk. The program takes three one-letter commands: ’a’ for allocate, ’f’ for free, and ’q’ for quit. The second argument on a line is the number of blocks (for allocate) or the address, or first block number, of the allocated chunk (for free).

## Run

Use Python to run buddy-memory-allocator.py.

```bash
python buddy-memory-allocator.py
```

## Usage

```bash
# 'a' for allocation
a 4

# 'f' foor free
f 0

# 'q' for quit
q
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
