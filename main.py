from numpy import base_repr, binary_repr, zeros, matmul, array, add, subtract
from sympy import Matrix


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


def ChangeBase(Rows, Mode, M=1, Len=0):
    CharCode = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            if Mode == 'D2M':
                Temp.append(base_repr(Num, M).zfill(Len))
            elif Mode == 'B2D':
                Temp.append(int(Num, 2))
            elif Mode == 'M2D':
                Temp.append(int(Num, M))
        CharCode.append(Temp)
    return CharCode


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


def Multiply(Rows, Key, B, M, Mode):
    AffineHill = list()
    for Mat in Rows:
        if Mode == 'E':
            AffineHill.append(add(matmul(Key, Mat), B).tolist())
        elif Mode == 'D':
            AffineHill.append(matmul(Key, subtract(Mat, B)).tolist())
    AffineHillRes = Remainder(AffineHill, M)
    return AffineHillRes


def Remainder(Rows, M):
    Remainders = list()
    for Row in Rows:
        Temp1 = list()
        for Mat in Row:
            Temp2 = list()
            for Col in Mat:
                Temp3 = list()
                for Num in Col:
                    Temp3.append(Num % M)
                Temp2.append(Temp3)
            Temp1.append(Temp2)
        Remainders.append(Temp1)
    return Remainders


def KeyStr2Int(KeyStr, Size):
    KeyInt = zeros((int(Size), int(Size)), int)
    for i in range(int(Size)):
        for j in range(int(Size)):
            KeyInt[i][j] = int(KeyStr.pop(0))
    KeyInt = KeyInt.tolist()
    return KeyInt


def ChangeShape(Rows):
    NewShape = list()
    for Char in Rows:
        NewShape.append(array(Char).reshape(1, -1).tolist())
    return NewShape


def ReduceDepth(Rows):
    NewDepth = list()
    for Mat in Rows:
        for Row in Mat:
            NewDepth.append(Row)
    return NewDepth


def StringMatrix(Rows):
    NewMatrix = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(str(Num))
        NewMatrix.append(Temp)
    return NewMatrix


def Blocking(Rows):
    NewBlock = list()
    for i in range(len(Rows)):
        Temp = list()
        for j in range(0, len(Rows[i]), 4):
            if len(Rows[i][j:j + 4]) == 4:
                Temp.append(''.join(Rows[i][j:j + 4]))
        NewBlock.append(Temp)
    return NewBlock


def GenerateKey():
    M = input('Enter your desired prime odd number for M: ')
    XORKey = input('Enter your desired key for XOR with each block: ')
    HyperBlockSize = input('Enter your desired number for hyper block size: ')
    AffineHillKey = input('Enter Affine-Hill key values: ').split(' ')
    AffineHillB = input('Enter Affine-Hill B values: ').split(' ')
    HyperBlockKey = KeyStr2Int(AffineHillKey, HyperBlockSize)
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
        KeyFile.write('Hyper block b: ' + '\n')
        for Num in AffineHillB:
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
    for Row in Info[5:5 + HyperBlockSize]:
        HyperBlockKey.append(list(Row))
    for i in range(len(HyperBlockKey)):
        for j in range(len(HyperBlockKey[i])):
            HyperBlockKey[i][j] = int(HyperBlockKey[i][j])
    HyperBlockB = list()
    for Num in Info[6 + HyperBlockSize:]:
        HyperBlockB.append(int(Num[0]))
    HyperBlockB = array(HyperBlockB).reshape(-1, 1).tolist()
    return M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey, HyperBlockB


def Encrypt():
    # KeyPath = input('Enter key location: ')
    # OriginalPath = input('Enter original file location: ')
    # EncryptedPath = input('Enter location to save encrypted file: ') + '\Encrypted.txt'
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    OriginalPath = r'C:\Users\User\Desktop\1.txt'
    EncryptedPath = r'C:\Users\User\Desktop' + '\Encrypted.txt'
    M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey, HyperBlockB = ExtractInfo(KeyPath)
    CharD = FileHandle(OriginalPath)
    print(CharD)
    CharXOR = BlockXOR(CharD, XORKey)
    print(CharXOR)
    ReqLenM = len(base_repr(2 ** InitialBlockSize - 1, M))
    CharM = ChangeBase(CharXOR, 'D2M', M, ReqLenM)
    print(CharM)
    CharH = HyperBlocking(CharM, HyperBlockSize)
    print(CharH)
    CharAH = Multiply(CharH, HyperBlockKey, HyperBlockB, M, 'E')
    print(CharAH)
    ReqLenB = len(binary_repr(M - 1))
    with open(EncryptedPath, 'w') as EncryptedFile:
        for Row in CharAH:
            for Mat in Row:
                for Col in Mat:
                    for Num in Col:
                        EncryptedFile.write(binary_repr(Num).zfill(ReqLenB) + ' ')
            EncryptedFile.write('\n')


def Decrypt():
    # KeyPath = input('Enter key location: ')
    # EncryptedPath = input('Enter Encrypted file location: ')
    # DecryptedPath = input('Enter location to save decrypted file: ') + '\Decrypted.txt'
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    EncryptedPath = r'C:\Users\User\Desktop\Encrypted.txt'
    DecryptedPath = r'C:\Users\User\Desktop' + '\Decrypted.txt'
    M, InitialBlockSize, XORKey, HyperBlockSize, HyperBlockKey, HyperBlockB = ExtractInfo(KeyPath)
    with open(EncryptedPath, 'r') as EncryptedFile:
        CharB = list()
        for Row in EncryptedFile.readlines():
            CharB.append(Row.strip().split(' '))
    print(CharB)
    CharD = ChangeBase(CharB, 'B2D')
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
    CharAH = Multiply(CharH, HyperBlockKeyInv, HyperBlockB, M, 'D')
    print(CharAH)
    CharM = Blocking(StringMatrix(ReduceDepth(ChangeShape(CharAH))))
    print(CharM)
    CharD = ChangeBase(CharM, 'M2D', M)
    print(CharD)
    CharXOR = BlockXOR(CharD, XORKey)
    print(CharXOR)
    with open(DecryptedPath, 'w') as DecryptedFile:
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
