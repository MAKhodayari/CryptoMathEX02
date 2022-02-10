from numpy import base_repr, binary_repr, zeros, matmul
from pprint import pprint


def FileHandle(Path):
    with open(Path, 'rb') as File:
        CharCodeD = list()
        for Row in File.readlines():
            CharCodeD.append(list(Row.strip()))
    return CharCodeD


def BlockXOR(Rows, Key):
    CharCodeXOR = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(Num ^ Key)
        CharCodeXOR.append(Temp)
    return CharCodeXOR


def Decimal2BaseM(Rows, M, Len):
    CharCodeM = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(base_repr(Num, M).zfill(Len))
        CharCodeM.append(Temp)
    return CharCodeM


def HyperBlocking(Rows, K):
    HyperBlock = list()
    for Row in Rows:
        AppendRow = list(''.join(Row))
        HyperTemp = list()
        Count = (len(AppendRow) // (K ** 2)) + 1
        for c in range(Count):
            Temp = zeros((K, K), int)
            for i in range(K):
                for j in range(K):
                    if len(AppendRow) != 0:
                        Temp[i, j] = int(AppendRow.pop(0))
                    else:
                        break
            HyperTemp.append(Temp.tolist())
        HyperBlock.append(HyperTemp)
    return HyperBlock


def GenerateKey():
    M = input('Enter your desired prime odd number for M: ')
    XORKey = input('Enter your desired key for XOR with each block: ')
    HyperBlockSize = input('Enter your desired number for hyper block size: ')
    HyperBlockKey = input('Enter Affine-Hill key numbers: ').split(' ')
    InitialBlockSize = '8'
    KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('M (Base Number): ' + M + '\n')
        KeyFile.write('Initial block size: ' + InitialBlockSize + '\n')
        KeyFile.write('XOR key: ' + XORKey + '\n')
        KeyFile.write('Hyper block size: ' + HyperBlockSize + '\n')
        KeyFile.write('Hyper block key: ' + '\n')
        for Num in HyperBlockKey:
            KeyFile.write(Num + '\n')


def ExtractInfo():
    pass


def Encrypt():
    pass


def Decrypt():
    pass


def DiscoverKey():
    pass


def Menu():
    print('[1] Key Generation.')
    print('[2] Encryption.')
    print('[3] Decryption.')
    print('[4] Key Discovery.')
    print('[0] Exit.')
    print()


if __name__ == '__main__':
    a = FileHandle(r'C:\Users\User\Desktop\1.txt')
    print(a)
    b = BlockXOR(a, 123)
    print(b)
    BlockSize = 8
    ReqLenM = len(base_repr(2 ** BlockSize, 5))
    c = Decimal2BaseM(b, 5, ReqLenM)
    print(c)
    d = HyperBlocking(c, 7)
    pprint(d)
    # print('Welcome.')
    # print('Please select your desired action from the list below.' + '\n')
    # Menu()
    # Option = input('Which one do you choose? Option: ')
    # print()
    # while Option != '0':
    #     if Option == '1':
    #         GenerateKey()
    #         print('Key generation successful.' + '\n' + 'Anything else?' + '\n')
    #     elif Option == '2':
    #         Encrypt()
    #         print('Encryption  successful.' + '\n' + 'Anything else?' + '\n')
    #     elif Option == '3':
    #         Decrypt()
    #         print('Decryption successful.' + '\n' + 'Anything else?' + '\n')
    #     elif Option == '4':
    #         DiscoverKey()
    #         print('Key discovery successful.' + '\n' + 'Anything else?' + '\n')
    #     else:
    #         print('Wrong input. Try again.' + '\n')
    #     Menu()
    #     Option = input('Which one do you choose? Option: ')
    #     print()
    # print('Thank You.')
