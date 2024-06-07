import os
import search

def load_files(directory):
    files = os.listdir(directory)
    return files

def remove_file(files):
    print(files)
    path = input('Please input filename.\n')
    files.remove(path)
    return files

def rename_files(files):
    kNum = 1
    rNum = 1
    qExist = False
    for select_file in files:
        tmp = input(select_file + ': choose Q or K or R or no change\n')
        path2 = tmp + str()
        if tmp == 'Q':
            if qExist == False:
                path2 = 'Q.txt'
                qExist = True
            else:
                print('error')
        elif tmp == 'K':
            path2 = tmp + str(kNum) + '.txt'
            kNum = kNum + 1
        elif tmp == 'R':
            path2 = tmp + str(rNum) + '.txt'
            rNum = rNum + 1
        else:
            print('no change')
            continue
        select_file = os.path.join(directory,select_file)
        path2 = os.path.join(directory, path2)
        os.rename(select_file,path2)
    return files

# main
directory = 'dataset'
files = load_files(directory)
files = rename_files(files)
files = load_files(directory)
while True:
    print('Please input load or remove or search or exit.')
    print('load:load files.')
    print('remove:remove file.')
    print('search:search for uploaded file.')
    print('exit:exit it.')
    print(files)
    CommandInput = input()
    if CommandInput == 'load': # create part, input 1 name
        files = load_files(directory)
    elif CommandInput == 'remove': # remove part, input 1 name
        files = remove_file(files)
    # elif CommandInput == 'rename':
    elif CommandInput == 'search': # search part, but this isn't complete
        searchKind = input('What search{simple search, QvsK, KvsK, keyness}\n')
        # ifelifでどの分析をするか決める
        if searchKind == 'simple search':
            type_search = input("Enter type of search (i.e. word token, lemma, POS, n-gram or regex)\n")
            keyword = input("\nSearch using Key Word in Context\n")
            data_num = len(files)
            results_simple = []
            search.simpleSearch(files, keyword, type_search, results_simple)
        elif searchKind == 'QvsK':
            # QvsK
            search.QK(files)
        elif searchKind == 'KvsK':
            # KvsK
            search.KK(files)
        elif searchKind == 'keyness':
            # keyness
            path1 = input('input reference filename\n')
            path2 = input('input target filename\n')
            search.lookupKeyness(path1,path2)
        else:
            print('wrong!')
    elif CommandInput == 'exit': # exit part.
        print('Bye!')
        break
    else:
        # error.
        print('Error. Please input accurately')
        continue
