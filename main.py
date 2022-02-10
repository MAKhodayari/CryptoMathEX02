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


def Multiply(Rows, Key, M):
    AffineHillRes = list()
    for Row in Rows:
        Temp = list()
        for Mat in Row:
            Temp.append(matmul(Key, Mat).tolist())
        AffineHillRes.append(Temp)
    for i in range(len(AffineHillRes)):
        for j in range(len(AffineHillRes[i])):
            for k in range(len(AffineHillRes[i][j])):
                AffineHillRes[i][j][k] = AffineHillRes[i][j][k] % M
    return AffineHillRes


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


def ExtractInfo(KeyPath):
    with open(KeyPath, 'r') as KeyFile:
        Info = list()
        for Row in KeyFile.readlines():
            Info.append(Row.strip().split(' '))
    M = int(Info[0][-1])
    InitialBlockSize = int(Info[1][-1])
    XORKey = int(Info[2][-1])
    HyperBlockSize = int(Info[3][-1])
    HyperBlockKey = list()
    for Row in Info[5:]:
        HyperBlockKey.append(int(Row[0]))
    return M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey


def Encrypt():
    KeyPath = input('Enter key location: ')
    OriginalPath = input('Enter original file location: ')
    EncryptedPath = input('Enter location to save encrypted file: ')
    M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey = ExtractInfo(KeyPath)
    CharD = FileHandle(OriginalPath)
    CharXOR = BlockXOR(CharD, XORKey)
    ReqLenM = len(base_repr(2 ** InitialBlockSize - 1, M))
    CharM = Decimal2BaseM(CharXOR, M, ReqLenM)
    CharH = HyperBlocking(CharM, HyperBlockSize)
    CharAH = Multiply(CharH, HyperBlockKey, M)
    ReqLenB = len(binary_repr(M - 1))
    with open(EncryptedPath + '\Encrypted.txt', 'w') as EncryptedFile:
        for Row in CharAH:
            for Mat in Row:
                for Num in Mat:
                    EncryptedFile.write(binary_repr(Num).zfill(ReqLenB) + ' ')
            EncryptedFile.write('\n')


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
    # a = FileHandle(r'C:\Users\User\Desktop\1.txt')
    # # print(a)
    # b = BlockXOR(a, 123)
    # # print(b)
    # BlockSize = 8
    # ReqLenM = len(base_repr(2 ** BlockSize, 5))
    # c = Decimal2BaseM(b, 5, ReqLenM)
    # # print(c)
    # d = HyperBlocking(c, 7)
    # # pprint(d)
    # e = Multiply(d, [1, 2, 2, 3, 4, 2, 1], 5)
    # print(e)
    print('Welcome.')
    print('Please select your desired action from the list below.' + '\n')
    Menu()
    Option = input('Which one do you choose? Option: ')
    print()
    while Option != '0':
        if Option == '1':
            GenerateKey()
            print('Key generation successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '2':
            Encrypt()
            print('Encryption  successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '3':
            Decrypt()
            print('Decryption successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '4':
            DiscoverKey()
            print('Key discovery successful.' + '\n' + 'Anything else?' + '\n')
        else:
            print('Wrong input. Try again.' + '\n')
        Menu()
        Option = input('Which one do you choose? Option: ')
        print()
    print('Thank You.')
