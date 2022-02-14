from numpy import binary_repr, base_repr
from numpy import add, subtract, matmul
from numpy import array, zeros
from sympy import Matrix


def ExtractFileInfo(Path, Mode):
    CharCode = list()
    if Mode == 'EA':
        with open(Path, 'rb') as File:
            for Row in File.readlines():
                CharCode.append(list(Row.strip()))
    elif Mode == 'EB':
        with open(Path, 'r') as File:
            for Row in File.readlines():
                CharCode.append(Row.strip().split(' '))
    return CharCode


def BlockXOR(Rows, Key):
    CharCodeXOR = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(Num ^ Key)
        CharCodeXOR.append(Temp)
    return CharCodeXOR


def ChangeBase(Rows, Mode, Base=1, Len=0):
    CharCode = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            if Mode == 'D2M':
                Temp.append(base_repr(Num, Base).zfill(Len))
            elif Mode == 'B2D':
                Temp.append(int(Num, 2))
            elif Mode == 'M2D':
                Temp.append(int(Num, Base))
        CharCode.append(Temp)
    return CharCode


def SoloBlock(Rows, Size):
    HyperBlock = list()
    for Row in Rows:
        AppendedRow = ''.join(Row)
        BlockTemp = list()
        Count = (len(AppendedRow) // Size) + 1
        for c in range(Count):
            Temp = zeros((Size, 1), int)
            for i in range(Size):
                if len(AppendedRow) != 0:
                    Temp[i][0] = int(AppendedRow[0])
                    AppendedRow = AppendedRow[1:]
            BlockTemp.append(Temp.tolist())
        HyperBlock.append(BlockTemp)
    return HyperBlock


def AffineHill(Rows, Key, B, Base, Mode):
    Temp = list()
    for Mat in Rows:
        if Mode == 'E':
            Temp.append(add(matmul(Key, Mat), B).tolist())
        elif Mode == 'D':
            Temp.append(matmul(Key, subtract(Mat, B)).tolist())
    AffineHillRes = ModularDivision(Temp, Base)
    return AffineHillRes


def ModularDivision(Rows, Divisor):
    Remainders = list()
    for Row in Rows:
        Temp1 = list()
        for Mat in Row:
            Temp2 = list()
            for Col in Mat:
                Temp3 = list()
                for Num in Col:
                    Temp3.append(Num % Divisor)
                Temp2.append(Temp3)
            Temp1.append(Temp2)
        Remainders.append(Temp1)
    return Remainders


def KeyStr2Int(KeyStr, Size):
    Size = int(Size)
    KeyInt = zeros((Size, Size), int)
    for i in range(Size):
        for j in range(Size):
            KeyInt[i][j] = int(KeyStr.pop(0))
    KeyInt = KeyInt.tolist()
    return KeyInt


def ChangeShape(Rows, Mode, Size=1):
    NewShape = list()
    if Mode == '1X':
        for Char in Rows:
            NewShape.append(array(Char).reshape(Size, -1).tolist())
    elif Mode == 'S1':
        for Row in Rows:
            Temp = list()
            for i in range(0, len(Row), Size):
                Temp.append(array(Row[i:i + Size]).reshape((Size, 1)).tolist())
            NewShape.append(Temp)
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


def GroupBlock(Rows, Size):
    NewBlock = list()
    for i in range(len(Rows)):
        Temp = list()
        for j in range(0, len(Rows[i]), Size):
            if len(Rows[i][j:j + Size]) == Size:
                Temp.append(''.join(Rows[i][j:j + Size]))
        NewBlock.append(Temp)
    return NewBlock


def GenerateKey():
    M = input('Enter your desired prime odd number for M: ')
    XORKey = input('Enter your desired key for XOR with each block: ')
    HyperBlockSize = input('Enter your desired number for hyper block size: ')
    HyperBlockKey = input('Enter Affine-Hill key values: ').split(' ')
    AffineHillB = input('Enter Affine-Hill B values: ').split(' ')
    KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    AffineHillKey = KeyStr2Int(HyperBlockKey, HyperBlockSize)
    InitialBlockSize = '8'
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('M (Base Number): ' + M + '\n')
        KeyFile.write('Initial block size: ' + InitialBlockSize + '\n')
        KeyFile.write('XOR key: ' + XORKey + '\n')
        KeyFile.write('Hyper block size: ' + HyperBlockSize + '\n')
        KeyFile.write('Affine-Hill key: ' + '\n')
        for Row in AffineHillKey:
            for Num in Row:
                KeyFile.write(str(Num) + ' ')
            KeyFile.write('\n')
        KeyFile.write('Affine-Hill b: ' + '\n')
        for Num in AffineHillB:
            KeyFile.write(Num + '\n')


def ExtractKeyInfo(Path):
    with open(Path, 'r') as File:
        Info = list()
        for Row in File.readlines():
            Info.append(Row.strip().split(' '))
    M = int(Info[0][-1])
    InitialBlockSize = int(Info[1][-1])
    XORKey = int(Info[2][-1])
    HyperBlockSize = int(Info[3][-1])
    AffineHillKey = list()
    for Row in Info[5:5 + HyperBlockSize]:
        AffineHillKey.append(list(Row))
    for i in range(len(AffineHillKey)):
        for j in range(len(AffineHillKey[i])):
            AffineHillKey[i][j] = int(AffineHillKey[i][j])
    AffineHillB = list()
    for Num in Info[6 + HyperBlockSize:]:
        AffineHillB.append(int(Num[0]))
    AffineHillB = array(AffineHillB).reshape(-1, 1).tolist()
    return M, InitialBlockSize, XORKey, HyperBlockSize, AffineHillKey, AffineHillB


def Encrypt():
    KeyPath = input('Enter key location: ')
    FilePath = input('Enter original file location: ')
    ASCIIFilePath = input('Enter location to save original file in ASCII format: ') + '\OriginalASCII.txt'
    EncryptedPath = input('Enter location to save encrypted file: ') + '\Encrypted.txt'
    M, InitialBlockSize, XORKey, HyperBlockSize, AffineHillKey, AffineHillB = ExtractKeyInfo(KeyPath)
    CharD = ExtractFileInfo(FilePath, 'EA')
    CharXOR = BlockXOR(CharD, XORKey)
    ReqLenM = len(base_repr(2 ** InitialBlockSize - 1, M))
    CharM = ChangeBase(CharXOR, 'D2M', M, ReqLenM)
    CharH = SoloBlock(CharM, HyperBlockSize)
    CharAH = AffineHill(CharH, AffineHillKey, AffineHillB, M, 'E')
    ReqLenB = len(binary_repr(M - 1))
    with open(EncryptedPath, 'w') as EncryptedFile:
        for Row in CharAH:
            for Mat in Row:
                for Col in Mat:
                    for Num in Col:
                        EncryptedFile.write(binary_repr(Num).zfill(ReqLenB) + ' ')
            EncryptedFile.write('\n')
    with open(ASCIIFilePath, 'w') as ASCIIFile:
        for Row in CharD:
            for Num in Row:
                ASCIIFile.write(str(Num) + ' ')
            ASCIIFile.write('\n')


def Decrypt():
    KeyPath = input('Enter key location: ')
    EncryptedPath = input('Enter Encrypted file location: ')
    # Save location for decrypted text file
    DecryptedPath = input('Enter location to save decrypted file: ') + '\Decrypted.txt'
    ASCIIDecryptedPath = input('Enter location to save ASCII decrypted file: ') + '\DecryptedASCII.txt'
    M, InitialBlockSize, XORKey, HyperBlockSize, AffineHillKey, AffineHillB = ExtractKeyInfo(KeyPath)
    CharB = ExtractFileInfo(EncryptedPath, 'EB')
    CharD = ChangeBase(CharB, 'B2D')
    CharH = ChangeShape(CharD, 'S1', HyperBlockSize)
    HyperBlockKeyInv = Matrix(AffineHillKey).inv_mod(M).tolist()
    CharAH = AffineHill(CharH, HyperBlockKeyInv, AffineHillB, M, 'D')
    ReqLenM = len(base_repr(2 ** InitialBlockSize - 1, M))
    CharM = GroupBlock(StringMatrix(ReduceDepth(ChangeShape(CharAH, '1X'))), ReqLenM)
    CharD = ChangeBase(CharM, 'M2D', M)
    CharXOR = BlockXOR(CharD, XORKey)
    # This part is used to write decrypted text file
    # with open(DecryptedPath, 'w') as DecryptedFile:
    #     for i in range(len(CharXOR)):
    #         for j in range(len(CharXOR[i])):
    #             if CharXOR[i][j] == XORKey and j == len(CharXOR[i]) - 1:
    #                 pass
    #             else:
    #                 DecryptedFile.write(chr(CharXOR[i][j]))
    #         DecryptedFile.write('\n')
    with open(ASCIIDecryptedPath, 'w') as ASCIIDecryptedFile:
        for i in range(len(CharXOR)):
            for j in range(len(CharXOR[i])):
                if CharXOR[i][j] == XORKey and j == len(CharXOR[i]) - 1:
                    pass
                else:
                    ASCIIDecryptedFile.write(str(CharXOR[i][j]) + ' ')
            ASCIIDecryptedFile.write('\n')


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
