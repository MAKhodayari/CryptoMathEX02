from numpy import base_repr, binary_repr, zeros, matmul, array, add, subtract
from sympy import Matrix
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


def Binary2Decimal(Rows):
    CharCodeB = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(int(Num, 2))
        CharCodeB.append(Temp)
    return CharCodeB


def BaseM2Decimal(Rows, M):
    CharCodeD = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(int(Num, M))
        CharCodeD.append(Temp)
    return CharCodeD


def HyperBlocking(Rows, K):
    HyperBlock = list()
    for Row in Rows:
        AppendRow = ''.join(Row)
        HyperTemp = list()
        Count = (len(AppendRow) // K) + 1
        for c in range(Count):
            Temp = zeros((K, 1), int)
            for i in range(K):
                if len(AppendRow) != 0:
                    Temp[i][0] = int(AppendRow[0])
                    AppendRow = AppendRow[1:]
            HyperTemp.append(Temp.tolist())
        HyperBlock.append(HyperTemp)
    return HyperBlock


def Multiply(Rows, Key, M, Mode):
    AffineHill = list()
    for Mat in Rows:
        if Mode == 'E':
            AffineHill.append(matmul(Key, Mat).tolist())
        elif Mode == 'D':
            AffineHill.append(matmul(Key, Mat).tolist())
    AffineHillRes = list()
    for Row in AffineHill:
        Temp1 = list()
        for Mat in Row:
            Temp2 = list()
            for Col in Mat:
                Temp3 = list()
                for Num in Col:
                    Temp3.append(Num % M)
                Temp2.append(Temp3)
            Temp1.append(Temp2)
        AffineHillRes.append(Temp1)
    return AffineHillRes


def GenerateKey():
    M = input('Enter your desired prime odd number for M: ')
    XORKey = input('Enter your desired key for XOR with each block: ')
    HyperBlockSize = input('Enter your desired number for hyper block size: ')
    HyperBlockKeyInput = input('Enter Affine-Hill key values: ').split(' ')
    HyperBlockKey = zeros((int(HyperBlockSize), int(HyperBlockSize)), int)
    for i in range(int(HyperBlockSize)):
        for j in range(int(HyperBlockSize)):
            HyperBlockKey[i][j] = int(HyperBlockKeyInput.pop(0))
    HyperBlockKey = HyperBlockKey.tolist()
    InitialBlockSize = '8'
    KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('M (Base Number): ' + M + '\n')
        KeyFile.write('Initial block size: ' + InitialBlockSize + '\n')
        KeyFile.write('XOR key: ' + XORKey + '\n')
        KeyFile.write('Hyper block size: ' + HyperBlockSize + '\n')
        KeyFile.write('Hyper block key: ' + '\n')
        for Row in HyperBlockKey:
            for Num in Row:
                KeyFile.write(str(Num) + ' ')
            KeyFile.write('\n')


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
        HyperBlockKey.append(list(Row))
    for i in range(len(HyperBlockKey)):
        for j in range(len(HyperBlockKey[i])):
            HyperBlockKey[i][j] = int(HyperBlockKey[i][j])
    return M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey


def Encrypt():
    # KeyPath = input('Enter key location: ')
    # OriginalPath = input('Enter original file location: ')
    # EncryptedPath = input('Enter location to save encrypted file: ')
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    OriginalPath = r'C:\Users\User\Desktop\1.txt'
    EncryptedPath = r'C:\Users\User\Desktop'
    M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey = ExtractInfo(KeyPath)
    CharD = FileHandle(OriginalPath)
    print(CharD)
    CharXOR = BlockXOR(CharD, XORKey)
    print(CharXOR)
    ReqLenM = len(base_repr(2 ** InitialBlockSize - 1, M))
    CharM = Decimal2BaseM(CharXOR, M, ReqLenM)
    print(CharM)
    CharH = HyperBlocking(CharM, HyperBlockSize)
    print(CharH)
    CharAH = Multiply(CharH, HyperBlockKey, M, 'E')
    print(CharAH)
    ReqLenB = len(binary_repr(M - 1))
    with open(EncryptedPath + '\Encrypted.txt', 'w') as EncryptedFile:
        for Row in CharAH:
            for Mat in Row:
                for Col in Mat:
                    for Num in Col:
                        EncryptedFile.write(binary_repr(Num).zfill(ReqLenB) + ' ')
            EncryptedFile.write('\n')


def Decrypt():
    # KeyPath = input('Enter key location: ')
    # EncryptedPath = input('Enter Encrypted file location: ')
    # DecryptedPath = input('Enter location to save decrypted file: ')
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    EncryptedPath = r'C:\Users\User\Desktop\Encrypted.txt'
    DecryptedPath = r'C:\Users\User\Desktop'
    M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey = ExtractInfo(KeyPath)
    with open(EncryptedPath, 'r') as EncryptedFile:
        CharB = list()
        for Row in EncryptedFile.readlines():
            CharB.append(Row.strip().split(' '))
    print(CharB)
    CharD = Binary2Decimal(CharB)
    print(CharD)
    CharH = list()
    for Row in CharD:
        Temp = list()
        for i in range(0, len(Row), HyperBlockSize):
            Temp.append(array(Row[i:i + HyperBlockSize]).reshape((3, 1)).tolist())
        CharH.append(Temp)
    print(CharH)
    HyperBlockKeyInv = Matrix(HyperBlockKey).inv_mod(M).tolist()
    print(HyperBlockKey)
    print(HyperBlockKeyInv)
    CharAH = Multiply(CharH, HyperBlockKeyInv, M, 'D')
    print(CharAH)
    Temp1 = list()
    for Char in CharAH:
        Temp1.append(array(Char).reshape(1, -1).tolist())
    print(Temp1)
    Temp2 = list()
    for Mat in Temp1:
        for Row in Mat:
            Temp2.append(Row)
    print(Temp2)
    Temp3 = list()
    for Row in Temp2:
        Temp4 = list()
        for Num in Row:
            Temp4.append(str(Num))
        Temp3.append(Temp4)
    print(Temp3)
    CharM = list()
    for i in range(len(Temp3)):
        Temp6 = list()
        for j in range(0, len(Temp3[i]), 4):
            if len(Temp3[i][j:j + 4]) == 4:
                Temp6.append(''.join(Temp3[i][j:j + 4]))
        CharM.append(Temp6)
    print(CharM)
    CharD = BaseM2Decimal(CharM, M)
    print(CharD)
    CharXOR = BlockXOR(CharD, XORKey)
    print(CharXOR)
    with open(DecryptedPath + '\Decrypted.txt', 'w') as DecryptedFile:
        for Row in CharXOR:
            for Num in Row:
                DecryptedFile.write(chr(Num))
            DecryptedFile.write('\n')


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
    # e = Multiply(d, [[1, 1, 1, 1, 1, 1, 1],
    #               [2, 1, 1, 1, 1, 1, 1],
    #               [2, 1, 1, 1, 1, 1, 1],
    #               [3, 1, 1, 1, 1, 1, 1],
    #               [4, 1, 1, 1, 1, 1, 1],
    #               [2, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1]], 5)
    # print(e)
    print('Welcome.')
    print('Please select your desired action from the list below.' + '\n')
    Menu()
    # Option = input('Which one do you choose? Option: ')
    Option = '2'
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
