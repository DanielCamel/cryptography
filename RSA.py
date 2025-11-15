import math
import random

# Функция для проверки простоты числа (простым перебором делителей)
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n**0.5)
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

# Генерируем случайные простые p и q, чтобы n = p*q был 16-битным
primes = [i for i in range(128, 256) if is_prime(i)]  # простые в некотором диапазоне
#p = random.choice(primes)
#q = random.choice(primes)
p = 257
q = 167

while q == p:
    q = random.choice(primes)

# Вычисляем n и phi(n)
n = p * q
phi = (p - 1) * (q - 1)

# Выбираем открытую экспоненту e, взаимно простую с phi
e = None
for candidate in [3, 5, 7, 11, 13, 17, 65537]:
    if candidate < phi and math.gcd(candidate, phi) == 1:
        e = candidate
        break

# Функция расширенного алгоритма Евклида для вычисления обратного элемента
def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    gcd, x1, y1 = egcd(b, a % b)
    # gcd = x1 * a + y1 * b
    x = y1
    y = x1 - (a // b) * y1
    return (gcd, x, y)

# Вычисляем секретную экспоненту d как мультипликативно обратную к e mod phi
g, x, y = egcd(e, phi)
if g != 1:
    raise Exception("e и phi(n) не взаимно просты!")
d = x % phi  # модульное обратное значение

# Данные задания (в двоичном виде)
x_bin = input("Введите открытый текст в двоичном виде: ")
y_bin = input("Введите шифртекст в двоичном виде: ")

# Валидация ввода
if not all(bit in '01' for bit in x_bin) or not x_bin:
    raise ValueError("x_bin должен содержать только 0 и 1")
if not all(bit in '01' for bit in y_bin) or not y_bin:
    raise ValueError("y_bin должен содержать только 0 и 1")

# Преобразуем их в целые числа
m = int(x_bin, 2)
c = int(y_bin, 2)


# Шифрование: вычисляем ciphertext = m^e mod n
cipher_text = pow(m, e, n)
cipher_bin = bin(cipher_text)[2:]  # представляем результат в двоичном формате

# Расшифрование: вычисляем plain_text = c^d mod n
plain_text = pow(c, d, n)
plain_bin = bin(plain_text)[2:]    # представляем результат в двоичном формате

# Вывод результатов
print("Выбранные простые p и q:", p, "и", q)
print("RSA-модуль n (16-бит) =", n)
print("Открытый ключ (e, n) =", (e, n))
print("Закрытый ключ d =", d)
print("Результат шифрования x в бинарном виде:", cipher_text,"=",cipher_bin)
print("Результат расшифрования y в бинарном виде:", plain_text,"=",plain_bin)