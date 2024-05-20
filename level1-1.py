import os

while True: # 入力をループさせている.
    print('Please input create or remove or rename or search or exit.')
    print('create:create file.')
    print('remove:remove file.')
    print('rename:change filename.')
    print('search:search for uploaded file.')
    print('exit:exit it.')
    CommandInput = input()
    if CommandInput == 'create': # create part, input 1 name
        path = input('Please input filename.\n')
        f = open(path, 'w')
        f.write('')
        f.close()
    elif CommandInput == 'remove': # remove part, input 1 name
        path = input('Please input filename.\n')
        os.remove(path)
    elif CommandInput == 'rename': # rename part, input 2 name
        path = input('Please input Old filename.\n')
        path2 = input('Please input New filename.\n')
        os.rename(path,path2)
    elif CommandInput == 'search': # search part, but this isn't complete
        path = input('Please input filename.\n')
        f = open(path, "r")
        s = f.read()
        print(s)
    elif CommandInput == 'exit': # exit part.
        print('Bye!')
        break
    else:
        # error.
        print('Error. Please input accurately')
        continue
