# Set total memory space
memory = 64

# Initialize memory, li_memory = [[starting index, size, used], ...]
li_memory = [[0, memory, False]]

def print_blocks():
    print('|', end='')
    for i in li_memory:
        if i[2] == True:
            print('#'*i[1], end='')
        else:
            print('-'*i[1], end='')
        print('|', end='')
    print()

while(1):
    print_blocks()
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
            #  Find the minimum free space
            min_memory_space = min([mmy[1] for mmy in li_memory if mmy[1]>=blocks and mmy[2] == False])

            # Get the index of the minimum memory space which is not allocated
            idx = [(y[1],y[2]) for y in li_memory].index((min_memory_space,False))
            
            # Split the memory space
            while(min_memory_space > blocks):
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
                
                # Update the minimum memory space
                min_memory_space = min([mmy[1] for mmy in li_memory if mmy[1]>=blocks and mmy[2] == False])
            
            # Allocate the number of blocks to the memory space
            li_memory[idx][2] = True
            
            # (idx start - idx end) form
            allocation_start_idx = li_memory[idx][0]
            allocation_end_idx = li_memory[idx][0]+li_memory[idx][1]-1
            print(f'Blocks {allocation_start_idx}-{allocation_end_idx} allcoated:')


    # Free (Deallocate)
    elif(cmd[0] == 'f'):
        first_block_num = blocks
        if(first_block_num > memory and first_block_num < 0):
            print("Memory space doesn't exist")
        elif (first_block_num not in [x[0] for x in li_memory if x[2] == True]):
            print("Number is not first block number or is not a free block that is not allocated")
        else:
            # Free the number of blocks starting from the first_block_num
            curr_idx = [x[0] for x in li_memory].index(first_block_num)
            li_memory[curr_idx][2]=False

            free_start_idx = li_memory[curr_idx][0]
            free_end_idx = li_memory[curr_idx][0]+li_memory[curr_idx][1]-1

            # Merge memory space if a neighboring block is empty
            while(len(li_memory)!=1):
                curr_idx_start = li_memory[curr_idx][0]
                curr_idx_size = li_memory[curr_idx][1]

                # If left and right neighbor are both empty
                if ((curr_idx!=0 and curr_idx!=len(li_memory)-1) and li_memory[curr_idx-1][2]==False and li_memory[curr_idx+1][2]==False):
                    # print("in both")
                    target = curr_idx-1 if li_memory[curr_idx-1][1]<=li_memory[curr_idx+1][1] else curr_idx+1
                # If only left neighbor is empty
                elif (curr_idx!=0 and li_memory[curr_idx-1][2]==False):
                    # print("in L")
                    target = curr_idx-1
                # If only right neighbor is empty
                elif (curr_idx!=len(li_memory)-1 and li_memory[curr_idx+1][2]==False):
                    # print("in R")
                    target = curr_idx+1
                # Stop merging cuz no neighbor is empty
                else:
                    break
                
                target_start = li_memory[target][0]
                target_size = li_memory[target][1]

                # Merge the memory space between the target and the current idx
                li_memory[curr_idx][1]+=li_memory[target][1]

                # Change the starting index of the current index if the target is the left neighbor
                if(target<curr_idx):
                    li_memory[curr_idx][0]=li_memory[target][0]
                    curr_idx=target

                # Delete the target from memory space
                li_memory.pop(target)

                # Print the merged memory space
                if (curr_idx_start <= target_start):
                    print(f'(merging {curr_idx_start}/{curr_idx_size} and {target_start}/{target_size})')
                else:
                    print(f'(merging {target_start}/{target_size} and {curr_idx_start}/{curr_idx_size})')

            # Print the freed memory space
            print(f'Blocks {free_start_idx}-{free_end_idx} freed:')


    # Quit
    elif(cmd[0] == 'q'):
        break


    # Invalid command
    else:
        print('Invalid command')
