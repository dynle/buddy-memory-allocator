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

memory = 64
# li_memory=[(4,True),(4,False),(8,False),(16,True),(32,False)]
# li_memory = (memory 시작 idx, memory크기, 사용여부)
li_memory = [(0, memory, False)]

def print_memory():
    print('|', end='')
    for i in li_memory:
        if i[2] == True:
            print('#'*i[0], end='')
        else:
            print('-'*i[0], end='')
        print('|', end='')
    print()

while(1):
    # print('|'+'-'*memory+'|')
    print_memory()


    print("How many blocks do you want to allocate/free?")
    cmd, blocks = input().split()
    blocks = int(blocks)
    if(cmd == 'a'):
        # splitting 0/64 ...
        if(blocks > memory):
            print("You can't allocate more than 64 blocks")
        else:
            space_size = max(li_memory, key=itemgetter(1))[1]
            while(1):
                if(blocks>space_size//2 and blocks <= space_size):
                    # 안나눠도됨 / 할당
                    idx = li_memory.index(space_size)
                    # 블록의 idx 시작 - idx 끝 형태
                    print(f'Blocks{0}-{3} allcoated:')
                    break
                else:
                    # 나눠야됨 / 나눠줌
                    space_size = space_size//2
                    print(f'(splitting) {0}/{space_size}')
                    pass
                # if(blocks < max(li_memory, key=itemgetter(0))[0]):
                #     pass
    elif(cmd == 'f'):
        # li_memory의 false, true를 기준으로 merge할지 안할지 결정 if statement
        # merging 0/4 and 4/4 ...
        print(f'Blocks{0}-{3} freed:')
    elif(cmd == 'q'):
        print('quit')
        break
    else:
        print('Invalid command')
