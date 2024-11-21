import random


def is_prime(n, k=5):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
        
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1
        if is_prime(n):
            return n

def generate_keys(bits=1024):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    d = pow(e, -1, phi)
    
    return (e, n), (d, n)

def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    
    return result

def text_to_numbers(text):
    numbers = []
    bytes_data = text.encode('utf-8')
    block_size = 128
    
    for i in range(0, len(bytes_data), block_size):
        block = bytes_data[i:i+block_size]
        number = int.from_bytes(block, byteorder='big')
        numbers.append(number)
    
    return numbers

def numbers_to_text(numbers):
    text_bytes = b''
    for number in numbers:
        byte_length = (number.bit_length() + 7) // 8
        bytes_data = number.to_bytes(byte_length, byteorder='big')
        text_bytes += bytes_data
    
    return text_bytes.decode('utf-8')

def encrypt_text(text, public_key):
    numbers = text_to_numbers(text)
    encrypted_numbers = []
    
    for number in numbers:
        encrypted_number = square_and_multiply(number, public_key[0], public_key[1])
        encrypted_numbers.append(encrypted_number)
    
    return encrypted_numbers

def decrypt_text(encrypted_numbers, private_key):
    decrypted_numbers = []
    
    for number in encrypted_numbers:
        decrypted_number = square_and_multiply(number, private_key[0], private_key[1])
        decrypted_numbers.append(decrypted_number)
    
    return numbers_to_text(decrypted_numbers)

def sign_text(text, private_key):
    """Создание цифровой подписи для текста"""
    numbers = text_to_numbers(text)
    signatures = []
    
    for number in numbers:
        signature = square_and_multiply(number, private_key[0], private_key[1])
        signatures.append(signature)
    
    return signatures

def verify_signature(signatures, text, public_key):
    """Проверка цифровой подписи текста"""
    numbers = text_to_numbers(text)
    
    for number, signature in zip(numbers, signatures):
        verified = square_and_multiply(signature, public_key[0], public_key[1])
        if verified != number:
            return False
    return True

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(data))

def run_tests():
    test_texts = [
        "Hello, World!",
        "This is a test message.",
        "Привет, мир!",
        "1234567890",
        "Special characters: !@#$%^&*()",
        "Lorem ipsum dolor sit amet",
        "Multiple\nLine\nText",
        "Short",
        "A very long text " * 10,
        "Mixed текст with различными characters"
    ]
    
    for i, test_text in enumerate(test_texts, 1):
        print(f"\nТест #{i}")
        print(f"Исходный текст: {test_text}")
        
        public_key, private_key = generate_keys()
        print("\nСгенерированные ключи:")
        print(f"Открытый ключ (e, n):")
        print(f"e = {public_key[0]}")
        print(f"n = {public_key[1]}")
        print(f"\nЗакрытый ключ (d, n):")
        print(f"d = {private_key[0]}")
        print(f"n = {private_key[1]}")
        
        save_to_file(f"{public_key[0]}\n{public_key[1]}", f"test{i}_public_key.txt")
        save_to_file(f"{private_key[0]}\n{private_key[1]}", f"test{i}_private_key.txt")
        
        encrypted = encrypt_text(test_text, public_key)
        print("\nЗашифрованный текст (в числовом представлении):")
        print(encrypted)
        
        save_to_file(encrypted, f"test{i}_encrypted.txt")
        
        decrypted = decrypt_text(encrypted, private_key)
        print(f"\nРасшифрованный текст:")
        print(decrypted)
        
        signature = sign_text(test_text, private_key)
        print("\nЦифровая подпись (в числовом представлении):")
        print(signature)
        
        save_to_file(signature, f"test{i}_signature.txt")
        
        is_valid = verify_signature(signature, test_text, public_key)
        print(f"\nПроверка подписи: {'Успешно' if is_valid else 'Ошибка'}")
        
        assert test_text == decrypted, f"Ошибка в тесте #{i}"
        assert is_valid, f"Ошибка в проверке подписи в тесте #{i}"
        
        print(f"\nТест #{i} успешно пройден")
        print("-" * 50)

if __name__ == "__main__":
    run_tests()