# -*- coding: utf-8 -*- .

# Автор: Галлямов Азат, группа 06-751
# Дата: 20.02.2021


from tkinter import *
import random
import matplotlib.pyplot as plt
from tkinter import filedialog
import time


def FastExponentiation(x,d):
    # функция реазизует быстрое возведение в степень. Возвращаемое число равно ( x^d )
    y = 1
    while d>0:
        if (d%2 != 0):
            y = (y*x)
        d = d//2
        x = (x*x)
    return y

def FastExponentiationNOD(x,d,n):
    # функция реазизует быстрое возведение в степень. Возвращаемое число равно ( x^d mod n )
    # y = 1
    # while d>0:
    #     if (d%2 != 0):
    #         y = (y*x) % n
    #     d = d//2
    #     x = (x*x) % n
    y = pow(x,d,n)
    return y

def Euclid(a,b):
    # функция реазизует поиск НОД=(a,b)
    while (b != 0):
        t = a % b
        a = b
        b = t
    return a

def ExtendetEuclid(m,n):
    # функция реазизует поиск НОД=(m,n), а также находим `s` и `t`, так что d=s*m+t*m
    a = m ; b = n
    u1 = 1 ; v1 = 0
    u2 = 0 ; v2 = 1
    while b != 0:
        q = a//b
        r = a % b
        a = b
        b = r
        r = u2
        u2 = u1 - q*u2
        u1 = r
        r = v2
        v2 = v1 - q*v2
        v1 = r
    d = a
    s = u1
    t = v1
    return s

def FermaNumber(n):
    F = FastExponentiation(2, FastExponentiation(2,n))+1
    return F

def GeneratePrimeNumber(length):
    simpleNum = [random.getrandbits(1) for _ in range(0,length)]
    simpleNum[0], simpleNum[length-1] = 1, 1
    primeNum = int(''.join(str(simpleNum[i]) for i in range(0,len(simpleNum))),2)
    i=0
    a = [2,3,5,7,9,11,13,17,19,23,27,29,31,37]
    while i<14:
        if FastExponentiationNOD(a[i], primeNum-1, primeNum) != 1:
            i = 0
            simpleNum = [random.getrandbits(1) for _ in range(0, length)]
            simpleNum[0] = 1
            primeNum = int(''.join(str(simpleNum[i]) for i in range(0, len(simpleNum))), 2)
        else:
            i +=1
    return primeNum

def KeyGen(r1=0.5,r2=0.5):
    # функция реазизует генерацию закрытого и открытого ключей
    global length
    l1_2['text'], l1_2['fg'] = '', '#1e7c4b'
    length = int(message_entry.get())
    try: length1 = int(length*r1); length2 = int(length*r2)
    except ValueError: l1_2['text'], l1_2['fg'] = "Неверная длина ключа!", '#bd1705' ; return 0
    p = GeneratePrimeNumber(length1)
    q = GeneratePrimeNumber(length2)
    n = p*q
    eiler = (p-1)*(q-1)
    e = 65537
    d = ExtendetEuclid(e, eiler)
    if d <0:
        d += eiler
    publicKey = [e,n]
    privateKey = [d,n]
    print('\n Public key:',publicKey)
    print(' Private key:',privateKey)
    with open("public.txt",'w',encoding='utf-8') as file:
        file.write(''.join(str(publicKey[0]))+" "+''.join(str(publicKey[1])))
        file.close()
    with open("private.txt",'w',encoding='utf-8') as file:
        file.write(''.join(str(privateKey[0]))+" "+''.join(str(privateKey[1])))
        file.close()
    l1_2['text'] = "Выполнено!"

def Crypt():
    # функция реазизует шифрование выбранного файла по открытому ключу

    l2_1['text'], l2_2['text'], l2_wayc['text'], l2_wayd['text']= '','','',''
    length = int(message_entry.get())
    filename = filedialog.askopenfilename()
    file = open(filename, 'rb')
    preamb = file.read(25000)
    btext = file.read()
    file.close()

    file = open("public.txt", 'r')
    key = file.read() ; file.close()
    eStr , nStr, i = '', '', 0
    while key[i] !=' ':
        eStr +=key[i] ; i+=1
    i+=1
    while key[i] != '':
        nStr +=key[i] ; i += 1
        try: key[i]
        except IndexError: break
    e , n = int(eStr), int(nStr)

    crypt_part = [ int.from_bytes((btext[i+j] for i in range(0,int(length/32))),'big') for j in range(0,len(btext)-int(length/32), int(length/32))]
    crypt_part.append(int.from_bytes((btext[i] for i in range(len(btext)-int(length/32),len(btext))),'big'))
    crypted_part = [(FastExponentiationNOD(i, e, n)) for i in crypt_part]
    with open('crypted.jpg', 'wb') as file:
        file.write(preamb)
        for i in range(0,len(crypted_part)):
            file.write(crypted_part[i].to_bytes(length,'big'))
        file.close()
    print(' Зашифрован: \n -------------------------------------------------------------------------------------------')
    l2_1['text'] = 'Зашифрован : '
    l2_wayc['text'] = filename

def Decrypt():
    # функция реазизует шифрование выбранного файла по открытому ключу

    l2_1['text'], l2_1['text'], l2_wayc['text'], l2_wayd['text'] = '', '', '', ''
    length = int(message_entry.get())
    filename = filedialog.askopenfilename()
    file = open(filename, 'rb')
    preamb = file.read(25000)
    btext = file.read()
    file.close()

    file = open("private.txt", 'r')
    key = file.read(); file.close()
    dStr, nStr, i = '', '', 0
    while key[i] != ' ':
        dStr += key[i]; i += 1
    i += 1
    while key[i] != '':
        nStr += key[i]; i += 1
        try: key[i]
        except IndexError: break
    d, n = int(dStr), int(nStr)

    decrypt_part = [ int.from_bytes((btext[i+j] for i in range(0, int(length))), 'big') for j in range(0,len(btext), int(length))]
    decrypted_part = [(FastExponentiationNOD(i, d, n)) for i in decrypt_part]
    with open('decrypted.jpg', 'wb') as file:
        file.write(preamb)
        for i in range(0, len(decrypted_part)):
            file.write( (decrypted_part[i]).to_bytes(int(length/32), byteorder='big'))
        file.close()
    print(' Расшифрован : \n -----------------------------------------------------------------------------------------')
    l2_2['text'] = 'Расшифрован : '
    l2_wayd['text'] = filename
    return 0

def Pollard():
    file = open("public.txt", 'r')
    key = file.read()
    file.close()
    eStr, nStr = '', ''
    i = 0
    while key[i] != ' ':
        eStr += key[i]; i += 1
    i += 1
    while key[i] != '':
        nStr += key[i]; i += 1
        try: key[i]
        except IndexError: break
    e = int(eStr)
    n = int(nStr)
    print('\n Открытый ключ : ', "[ "+ str(e) + " , " + str(n) + " ]")

    file = open("private.txt", 'r')
    key = file.read()
    file.close()
    dStr, nStr = '', ''
    i = 0
    while key[i] != ' ':
        dStr += key[i]; i += 1
    i += 1
    while key[i] != '':
        nStr += key[i]; i += 1
        try: key[i]
        except IndexError: break
    d = int(dStr)
    print(' Закрытый ключ : ', "[ "+ str(d) + " , " + str(n) + " ]")

    start = time.time()
    x, y, i, stage = random.randint(1, n-2), 1, 0, 2
    while (Euclid(n, abs(x-y)) == 1):
        if (i == stage):
            y = x
            stage = stage * 2
        x = (x * x + 1) % n
        i = i + 1
    p = Euclid(n, abs(x-y))
    q = int(n/p)
    eiler = (p-1)*(q-1)
    d_pol = ExtendetEuclid(e,eiler)
    if d_pol <0:
        d_pol += eiler
    end = time.time()
    print(' Вычисленный закрытый ключ :  '+ "[ "+ str(d_pol) + " , " + str(n) + " ]")
    print(' Время вычисления : ' + str(end - start))
    print("-----------------------------------------------------------------------------------\n")

    length = message_entry.get()
    lenKey.append(length)
    timeKey.append(end - start)

def Graph():
    global r, timeKey
    file = open('time_byte_key.txt', 'w')
    file.write(','.join(str(timeKey[i]) for i in range(0,len(timeKey))))
    file.write('\n')
    file.write(','.join(str(lenKey[i]) for i in range(0,len(lenKey))))
    file.write('\n')
    file.close()
    print(timeKey)
    print(lenKey)
    plt.plot(lenKey,timeKey)
    plt.title('Зависимость времени вычисления от длины ключа')
    plt.xlabel('Длина ключа в битах')
    plt.ylabel('Время расчета в секундах')
    plt.grid()
    plt.show()
    r = []
    timeKey = []

def Five():
    global timeKey
    r = []
    timeKey = []
    for i in range(250,505,5):
        j = i/1000
        print(' r = ' + str(j))
        KeyGen(j,1-j)
        Pollard()
        r.append(j)
    plt.grid()  # включение отображение сетки
    plt.title("Зависимость времени факторизации от r")
    plt.xlabel("Величина r")
    plt.ylabel("Время, с")
    plt.plot(r, timeKey)
    plt.show()


if __name__ == "__main__":

    timeKey = []
    lenKey = []

    root = Tk(); winsize = [630, 560]; root.title("RSA")
    root.geometry(str(winsize[0])+'x'+str(winsize[1])); root.resizable(False, False)
    can = Canvas(width=622, height=554, bg='#ddd')

    length = StringVar()
    length.set("1024")

    lKey=Label(root, text="1. Сгенерировать открытый и закрытый ключи", ba='#ddd', fg='#222', font=['Akrobat Bold', 12])
    lKey.place(x=15, y=15)
    l1 = Label(root, text="Введите длину ключа:                  (по умолч. = 1024)", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l1.place(x=40,y=55)
    message_entry= Entry(textvariable=length,width=8)
    message_entry.place(x=225, y=55)
    l1_2 =Label(root, text="", ba='#ddd', fg='#1e7c4b', font=['Akrobat Bold', 10])
    l1_2.place(x=150,y=95)
    bKey = Button(text="Генерация", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=KeyGen,padx=0)
    bKey.place(x=40, y=90)

    lCrypt = Label(root, text="2. Зашифровать и расшифровать файлы", ba='#ddd', fg='#222',font=['Akrobat Bold', 12])
    lCrypt.place(x=15, y=180)
    bCrypt = Button(text="Зашифровать", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Crypt,padx=0)
    bCrypt.place(x=55, y=230)
    bDecrypt = Button(text="Расшифровать", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Decrypt,padx=0)
    bDecrypt.place(x=230, y=230)
    l2_1 = Label(root, text="", ba='#ddd', fg='#1e7c4b', font=['Akrobat Bold', 10])
    l2_1.place(x=65, y=270)
    l2_wayc = Label(root, text="", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l2_wayc.place(x=65, y=290)
    l2_2 = Label(root, text="", ba='#ddd', fg='#1e7c4b', font=['Akrobat Bold', 10])
    l2_2.place(x=240, y=270)
    l2_wayd = Label(root, text="", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l2_wayd.place(x=240, y=290)

    lPolard = Label(root, text="3. Вычисление закрытого ключа по открытому", ba='#ddd', fg='#222', font=['Akrobat Bold', 12])
    lPolard.place(x=15, y=340)
    bCrypt = Button(text="Вычислить", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Pollard,padx=10)
    bCrypt.place(x=55, y=380)

    lBar = Label(root, text="4. График завис. времени вычисл. private Key от длины ключа", ba='#ddd', fg='#222',font=['Akrobat Bold', 12])
    lBar.place(x=15, y=450)
    bBar = Button(text="График", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Graph,padx=24)
    bBar.place(x=55, y=490)
    bBar = Button(text="5 задание", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Five, padx=14)
    bBar.place(x=230, y=490)

    can.place(x=2, y=0); root.mainloop()
