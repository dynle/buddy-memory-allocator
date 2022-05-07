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
# li_memory = [memory 시작 idx, memory크기, 사용여부]
li_memory = [[0, memory, False]]

def print_memory():
    print('|', end='')
    # 전체를 #로 취급하면 안됨 ex) 메모리 공간이 32인데 31을 할당한 경우.
    for i in li_memory:
        if i[2] == True:
            print('#'*i[1], end='')
        else:
            print('-'*i[1], end='')
        print('|', end='')
    print()

while(1):
    # print('|'+'-'*memory+'|')
    print_memory()


    print("How many blocks do you want to allocate/free?")
    cmd = input().split()
    blocks = int(cmd[-1]) if len(cmd) != 1 else None

    # Allcoate
    if(cmd[0] == 'a'):
        # splitting 0/64 ...
        if(blocks > memory):
            print("You can't allocate more than 64 blocks")
        else:
            # 나뉘어진 상태에서 적절한 공간이 있으면 할당
            for space in li_memory:
                if (blocks <= space[1] and blocks > space[1]//2):
                    print("공간있어요")
                    # 있으면 그 idx를 넣어줌
                    if [(y[1],y[2]) for y in li_memory].index((blocks,False)):
                        idx = [(y[1],y[2]) for y in li_memory].index((blocks,False))
                    # 없는데 MIN 공간보다 작으면 split 해주고 할당
                    else:
                        pass
                    # idx = [(y[1],y[2]) for y in li_memory].index((blocks,False))
                    li_memory[idx][2] = True
                    print(f'Blocks {li_memory[idx][0]}-{li_memory[idx][0]+blocks} allcoated:')
                    print("li_memory", li_memory)
                    break
            else:
                print("공간없어요")
                upper_space_size = max(li_memory, key=itemgetter(1))[1]
                print("max upper space size: ", upper_space_size)
                tmp = 1
                while(1):
                    if(blocks>upper_space_size//2 and blocks <= upper_space_size):
                        # 안나눠도됨 / 할당
                        idx = [(y[1],y[2]) for y in li_memory].index((upper_space_size,False))
                        li_memory[idx][2] = True
                        # 블록의 idx 시작 - idx 끝 형태
                        print(f'Blocks {li_memory[idx][0]}-{li_memory[idx][0]+blocks} allcoated:')
                        print("li_memory", li_memory)
                        break
                    else:
                        # 나눠야됨 / 나눠줌
                        # memory size가 MIN인 값 하나를 두개롤 나누고, 나머지 MAX인 값은 붙여준다. if len(li_memory) 값이 2이상일때
                        if (len(li_memory) == 1):
                            # 64일때
                            li_memory=[[0, upper_space_size//2, False],[upper_space_size//2, upper_space_size//2, False]]
                        else:
                            # 64가 아닐때
                            li_memory=[[0, upper_space_size//2, False],[upper_space_size//2, upper_space_size//2, False]]+li_memory[-tmp:]
                            tmp+=1
                        # 0 대신에 시작 idx를 넣어줘야함
                        print(f'(splitting {0}/{upper_space_size})')
                        upper_space_size = upper_space_size//2
                    # if(blocks < max(li_memory, key=itemgetter(0))[0]):
                    #     pass

        # elif (blocks <= y[1] and blocks > y[1]//2 for y in li_memory):
        #     idx = [y[1] for y in li_memory if y[2] == False].index(upper_space_size)
        #     li_memory[idx][2] = True
        #     print(f'Blocks {li_memory[idx][0]}-{li_memory[idx][0]+blocks} allcoated:')
        #     print("li_memory", li_memory)
        #     break

        # 적절한 공간이 없으면 나눠준 다음 할당
        # else:
        #     upper_space_size = max(li_memory, key=itemgetter(1))[1]
        #     print("max upper space size: ", upper_space_size)
        #     tmp = 1
        #     while(1):
        #         if(blocks>upper_space_size//2 and blocks <= upper_space_size):
        #             # 안나눠도됨 / 할당
        #             idx = [y[1] for y in li_memory if y[2] == False].index(upper_space_size)
        #             li_memory[idx][2] = True
        #             # 블록의 idx 시작 - idx 끝 형태
        #             print(f'Blocks {li_memory[idx][0]}-{li_memory[idx][0]+blocks} allcoated:')
        #             print("li_memory", li_memory)
        #             break
        #         else:
        #             # 나눠야됨 / 나눠줌
        #             # memory size가 MIN인 값 하나를 두개롤 나누고, 나머지 MAX인 값은 붙여준다. if len(li_memory) 값이 2이상일때
        #             if (len(li_memory) == 1):
        #                 # 64일때
        #                 li_memory=[[0, upper_space_size//2, False],[upper_space_size//2, upper_space_size//2, False]]
        #             else:
        #                 # 64가 아닐때
        #                 li_memory=[[0, upper_space_size//2, False],[upper_space_size//2, upper_space_size//2, False]]+li_memory[-tmp:]
        #                 tmp+=1
        #             # 0 대신에 시작 idx를 넣어줘야함
        #             print(f'(splitting {0}/{upper_space_size})')
        #             upper_space_size = upper_space_size//2
        #         # if(blocks < max(li_memory, key=itemgetter(0))[0]):
        #         #     pass
    
    # Free
    elif(cmd[0] == 'f'):
        # li_memory의 false, true를 기준으로 merge할지 안할지 결정 if statement, 옆 공간이 나와 같을 때까지 while statement
        # merging 0/4 and 4/4 ...

        print(f'Blocks{0}-{3} freed:')

    elif(cmd[0] == 's'):
        print(li_memory)

    # Quit
    elif(cmd[0] == 'q'):
        break

    # Invalid command
    else:
        print('Invalid command')
