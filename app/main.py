
from random import randint
import bitarray
import os


# Функция для нахождения обратного элемента
def evcalg(a: int, b: int):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = evcalg(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# Функция для нахождения мультипликативно обратного r по модулю q
def multiinv(r, q):
    gcd, x, y = evcalg(r, q)
    return q + x

# Функция для генерации простого числа, большего заданного
def prime_number(a): #q
    count = 0
    for i in range(a + 1, 100000000000000):
        for j in range(1, i + 1):
            if i % j == 0:
                count += 1
            if count > 2:
                count = 0
                break
        if count == 2:
            return i

# Функция для генерации открытого и закрытого ключей
def generate_keys(close_key):
    S = sum(close_key)  # Сумма элементов секретного ключа
    q = prime_number(S)  # Генерация большого простого числа q
    r = randint(1, q)  # Выбор случайного числа r меньшего q
    open_key = []
    for k in close_key:
        open_key.append(k * r % q)  # Генерация открытого ключа
    return S, q, r, open_key

# Функция для шифрования текста
def encrypt(text, open_key):
    crypted_text = []
    for char in text:
        char_bites = bitarray.bitarray() #преобразование из символьного в бинарный вид
        char_bites.frombytes(char.encode('utf-8'))
        char_bites = char_bites.tolist()
        s = 0
        i = 0
        while i < len(char_bites):
            s += open_key[i] * char_bites[i]
            i += 1
        crypted_text.append(s)
    return crypted_text

# Функция для дешифрования текста
def decrypt(crypted_text, r, q, close_key):
    decrypted_text = ""
    decrypted_list_bites = []
    for crypred_char in crypted_text:
        temp = (crypred_char * multiinv(r, q)) % q  #С′
        raz = temp
        decrypted_char_num_bites = []  # Номера битов, которые должны быть равны 1
        while raz != 0:
            for i in range(len(close_key)):
                if close_key[i] > raz:
                    raz -= close_key[i - 1]
                    decrypted_char_num_bites.append(i - 1)
                    break
                if i == 7:
                    raz -= close_key[i]
                    decrypted_char_num_bites.append(i)
        decrypted_char_bites = [0, 0, 0, 0, 0, 0, 0, 0]
        for el in decrypted_char_num_bites:
            decrypted_char_bites[el] = 1
        decrypted_list_bites.append(decrypted_char_bites)
    for char_bite in decrypted_list_bites: #перевод из бинарного вида в символьный
        bit_array = bitarray.bitarray(char_bite)
        byte_array = bit_array.tobytes()
        decrypted_text += byte_array.decode()
    return decrypted_text

#mes = "Hello world"
print(f"Enter text:")
mes = os.getenv("text")
close_key = {1, 2, 4, 8, 16, 32, 64, 128}
close_key_list = list(sorted(close_key))
S, q, r, open_key = generate_keys(close_key_list)
enc = encrypt(mes, open_key)
print(f"Encrypted text - {enc}")
print(f"Decrypted text - {decrypt(enc, r, q, close_key_list)}")

#{1, 3, 7, 15, 32, 63, 125, 251}
#{7, 13, 27, 53, 106, 213, 422, 850}
#{11, 23, 51, 101, 213, 444, 913, 1999}





