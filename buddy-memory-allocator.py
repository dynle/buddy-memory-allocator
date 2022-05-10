"""
Write an interactive demonstration of a buddy memory allocator.
Your demo should allow 64 blocks to be allocated and deallocated, and it should correctly merge freed blocks.
The output should be something like that in Fig. 5.2.
Each time your program splits a block, it should add a ’|’ to show where the split happened.
’-’ represents free blocks, and ’#’ represents in-use blocks.
The two numbers printed out as in 0/4 represent the beginning address and number of blocks in a chunk.
Your program should take three one-letter commands: ’a’ for allocate, ’f’ for free, and ’q’ for quit.
The second argument on a line should be the number of blocks (for allocate) or the address, or first block number, of the allocated chunk (for free).
If two neighboring blocks are both allocated, but were part of separate allocations, be careful to only free the one in the actual request!
For large numbers of blocks, there are many possible data structures you could use to track the set of blocks that are in use and the size of chunks.

See p. 17-108 of syspro-kiso-e.pdf for further description, though you can write this in any language of your choice.

"""

from operator import itemgetter
# set total memory space
memory = 64
# li_memory=[(4,True),(4,False),(8,False),(16,True),(32,False)]
# li_memory = [memory 시작 idx, memory크기, 사용여부]

# initialize memory
li_memory = [[0, memory, False]]

def print_memory():
    print('|', end='')
    for i in li_memory:
        if i[2] == True:
            print('#'*i[1], end='')
        else:
            print('-'*i[1], end='')
        print('|', end='')
    print()

while(1):
    print_memory()

    print("How many blocks do you want to allocate/free?")
    cmd = input().split()
    blocks = int(cmd[-1]) if len(cmd) != 1 else None

    # Allcoate
    if(cmd[0] == 'a'):
        if (blocks > memory):
            print("You can't allocate more than 64 blocks")
        elif (blocks > max([x[1] for x in li_memory if x[2] == False])):
            print("You can't allocate more than the biggest free blocks")
        else:
            # Get the index of the minimum memory space
            idx = [(y[1],y[2]) for y in li_memory].index((min([mmy[1] for mmy in li_memory if mmy[1]>=blocks and mmy[2] == False]),False))
            
            # Split the memory space
            while(min([mmy[1] for mmy in li_memory if mmy[1]>=blocks and mmy[2] == False]) > blocks):
                # min(li_memory, key=itemgetter(1))[1] 이런거 사용해서 clean code
                print(f'(splitting {li_memory[idx][0]}/{li_memory[idx][1]})')
                
                # Split the memory space by 2
                if (li_memory[idx][1]//2 >= blocks and li_memory[idx][1]%2 == 0):
                    li_memory[idx:idx+1] = [[li_memory[idx][0], li_memory[idx][1]//2, False],[li_memory[idx][0]+li_memory[idx][1]//2, li_memory[idx][1]//2, False]]
                    # li_memory=li_memory[:idx]+[[li_memory[idx][0], li_memory[idx][1]//2, False],[li_memory[idx][0]+li_memory[idx][1]//2, li_memory[idx][1]//2, False]]+li_memory[idx+1:]
                
                # Split the memory space by the number of blocks
                else:
                    li_memory[idx:idx+1] = [[li_memory[idx][0],blocks,False],[li_memory[idx][0]+blocks,li_memory[idx][1]-blocks,False]]
                    # li_memory=li_memory[:idx]+[[li_memory[idx][0],blocks,False],[li_memory[idx][0]+blocks,li_memory[idx][1]-blocks,False]]+li_memory[idx+1:]
            # Allocate the number of blocks to the memory space
            li_memory[idx][2] = True
            # (idx start - idx end) form
            allocation_start_idx = li_memory[idx][0]
            allocation_end_idx = li_memory[idx][0]+li_memory[idx][1]-1
            print(f'Blocks {allocation_start_idx}-{allocation_end_idx} allcoated:')
    
    # Free
    elif(cmd[0] == 'f'):
        first_block_num = blocks
        if(first_block_num > memory and first_block_num < 0):
            print("Memory space doesn't exist")
        elif (first_block_num not in [x[0] for x in li_memory if x[2] == True]):
            print("Number is not first block number or is not a free block that is not allocated")
        else:
            # Free the number of blocks starting from the first_block_num
            idx = [x[0] for x in li_memory].index(first_block_num)
            li_memory[idx][2]=False

            free_start_idx = li_memory[idx][0]
            free_end_idx = li_memory[idx][0]+li_memory[idx][1]-1

            # Merge memory space if two neighboring blocks are both empty
            while(len(li_memory)!=1 and ((idx==len(li_memory)-1 and li_memory[idx-1][2]==False) or (idx==0 and li_memory[idx+1][2]==False) or (li_memory[idx-1][2]==False and li_memory[idx+1][2]==False))):
                idx_start = idx
                idx_size = li_memory[idx][1]
                target_start = 0
                target_size = 0

                # If left and right neighbor are both empty
                if ((idx!=0 and idx!=len(li_memory)-1) and li_memory[idx-1][2]==False and li_memory[idx+1][2]==False):
                    # print("in both")
                    target = idx-1 if li_memory[idx-1][1]<=li_memory[idx+1][1] else idx+1
                    target_start = li_memory[target][0]
                    target_size = li_memory[target][1]
                    if (target<idx):
                        li_memory[target][1]+=li_memory[idx][1]
                        li_memory.pop(idx)
                        idx=target
                    else:
                        li_memory[idx][1]+=li_memory[target][1]
                        li_memory.pop(target)

                # If only left neighbor is empty
                elif (idx!=0 and li_memory[idx-1][2]==False):
                    # print("in L")
                    target = idx-1
                    target_start = li_memory[target][0]
                    target_size = li_memory[target][1]
                    li_memory[target][1]+=li_memory[idx][1]
                    li_memory.pop(idx)
                    idx=target

                # If only right neighbor is empty
                elif (li_memory[idx+1][2]==False):
                    # print("in R")
                    target = idx+1
                    target_start = li_memory[target][0]
                    target_size = li_memory[target][1]
                    li_memory[idx][1]+=li_memory[target][1]
                    li_memory.pop(idx+1)
                
                if (idx_start <= target_start):
                    print(f'(merging {idx_start}/{idx_size} and {target_start}/{target_size})')
                else:
                    print(f'(merging {target_start}/{target_size} and {idx_start}/{idx_size})')

            print(f'Blocks {free_start_idx}-{free_end_idx} freed:')

    # Quit
    elif(cmd[0] == 'q'):
        break

    # Invalid command
    else:
        print('Invalid command')
