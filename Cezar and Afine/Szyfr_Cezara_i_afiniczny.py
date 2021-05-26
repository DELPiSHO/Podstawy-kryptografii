import optparse
from string import ascii_letters,ascii_lowercase, ascii_uppercase
import numpy as np

"""
Przedmiot: Podstawy kryptografii
Projekt: Szyfr Cezara i Afiniczny
Autor: Yauheni Dzianisau
Numer indeksu: 238213
Data: 07.03.2021
"""

def read_file(file_name):
    file = open(file_name, "r")
    content = file.read()
    file.close()
    return content

def write_to_file(file_name, content):
    file = open(file_name, "w+")
    file.write(content)
    file.close()

def read_key(file_name):
    content = read_file(file_name)
    founded_keys = content.split(' ')
    if len(founded_keys) == 1:
        return (int(founded_keys[0]))
    elif len(founded_keys) == 2:
        return (int(founded_keys[0]), int(founded_keys[1]))

def encrypt_letter_af(letter, x, y):
    letters = None
    if (letter >= 'a' and letter <= 'z'):
        letters = ascii_lowercase
    elif (letter >= 'A' and letter <= 'Z'):
        letters = ascii_uppercase
    else:
        return letter
    code = list(letters).index(letter)
    new_code = ((code * x + y) % 26)
    return list(letters)[new_code]

def encrypt_letter_ce(letter, y):
    letters = None
    if (letter >= 'a' and letter <= 'z'):
        letters = ascii_lowercase
    elif (letter >= 'A' and letter <= 'Z'):
        letters = ascii_uppercase
    else:
        return letter
    code = list(letters).index(letter)
    new_code = ((code + y) % 26)
    return list(letters)[new_code]

def decrypt_letter_af(letter, x, y):
    reversed_x = find_reverse(x, 26)
    letters = None
    if reversed_x != -1:
        if (letter >= 'a' and letter <= 'z'):
            letters = ascii_lowercase
        elif (letter >= 'A' and letter <= 'Z'):
            letters = ascii_uppercase
        else:
            return letter
        code = list(letters).index(letter)
        new_code = ((reversed_x * (code - y)) % 26)
        return list(letters)[new_code]

def decrypt_letter_ce(letter, y):
    letters = None
    if (letter >= 'a' and letter <= 'z'):
        letters = ascii_lowercase
    elif (letter >= 'A' and letter <= 'Z'):
        letters = ascii_uppercase
    else:
        return letter
    code = list(letters).index(letter)
    new_code = ((code - y) % 26)
    return list(letters)[new_code]


def encrypt_alphabet_af(x,y):
    encrypt = ''.join(map(lambda i : encrypt_letter_af(i, x, y), list(ascii_letters)))
    return encrypt

def decrypt_alphabet_af(alphabet, x, y):
    decrypt = ''.join(map(lambda i: decrypt_letter_af(i, x, y), list(alphabet)))
    return decrypt

def encrypt_alphabet_ce(y):
    encrypt = ''.join(map(lambda i : encrypt_letter_ce(i, y), list(ascii_letters)))
    return encrypt

def decrypt_alphabet_ce(alphabet, y):
    decrypt = ''.join(map(lambda i: decrypt_letter_ce(i, y), list(alphabet)))
    return decrypt

def check_reverse(x, y, n):
    if ((x * y) % n) != 1:
        return False
    else:
        return True

def find_reverse(x, n):
    for i in range(n):
        if check_reverse(x, i, n):
            return i
    return -1

def gcd(x, y):
    a, b = x, y
    while (b != 0):
        c = a % b
        a = b
        b = c
    return a

def translate_text(text, alphabet1, alphabet2):
    text = text.translate(str.maketrans(alphabet1, alphabet2))
    return text

def encrypt_text_af(text, x, y):
    encrypt = translate_text(text, ascii_letters, encrypt_alphabet_af(x, y))
    return encrypt

def decrypt_text_af(text, x, y):
    decrypt = translate_text(text, encrypt_alphabet_af(x, y), ascii_letters)
    return decrypt

def encrypt_text_ce(text, y):
    encrypt = translate_text(text, ascii_letters, encrypt_alphabet_ce(y))
    return encrypt

def decrypt_text_ce(text, y):
    decrypt = translate_text(text, encrypt_alphabet_ce(y), ascii_letters)
    return decrypt

if __name__ == "__main__":
    FILE_PLAIN = "plain.txt"
    FILE_ENCRYPT = "crypto.txt"
    FILE_DECRYPT = "decrypt.txt"
    FILE_KEY = "key.txt"
    FILE_EXTRA = "extra.txt"
    FILE_KEY_FOUND = "key-found.txt"
    FILE_ANALIZE = "kryptoanaliza.txt"

    parser = optparse.OptionParser(usage="Program ktory pozwala na szyfrowanie i deszyfrowanie tekstu za pomocą szyfru Cezara i szyfru Afinicznego",
                          version="%version 1.02")
    parser.add_option("-c", "--cipher_Cezar",
                      action="store_true",
                      dest="cipher_Cezar_flag",
                      default=False,
                      help="Trzeba użyć szyfr Cezara")

    parser.add_option("-a", "--cipher_afine",
                      action="store_true",
                      dest="cipher_afine_flag",
                      default=False,
                      help="Trzeba użyć szyfr afiniczny")

    parser.add_option("-e", "--encrypt",
                      action="store_true",
                      dest="encrypt_flag",
                      default=False,
                      help="Szyfrowanie przez podany szyfr pliku Plain.txt")

    parser.add_option("-d", "--decrypt",
                      action="store_true",
                      dest="decrypt_flag",
                      default=False,
                      help="Deszyfrowanie przez podany szyfr pliku crypto.txt")

    parser.add_option("-j", "--kryptoanaliza_z_tekstem_jawnym_i_extra",
                      action="store_true",
                      dest="extra_flag",
                      default=False,
                      help="Używamy tekst pomocniczy dla znalezienia kluczy")

    parser.add_option("-k", "--wszystkie przypadki",
                      action="store_true",
                      dest="all_flag",
                      default=False,
                      help="Zapisywanie wszystkich możliwych wariantów do pliku decrypt.txt")
    options,args = parser.parse_args()
    if len(args) != 0:
        parser.error("Wrong number of arguments.")

    x = 0
    y = 0
    #if options.cipher_Cezar_flag:
    #   continue
        #x = read_key(FILE_KEY)[0]
    #elif options.cipher_afine_flag:
        #(x, y) = read_key(FILE_KEY)
    #else:
    #    print("You must choose cipher Cezar or cipher afine.")

    if options.encrypt_flag:
        print("Encrypt...\n")
        keys = read_key(FILE_KEY)
        text = read_file(FILE_PLAIN)
        if options.cipher_Cezar_flag:
            x = read_key(FILE_KEY)[0]
            if (x < 0 ) or (x > 26):
                print("Wrong key")
            else:
                write_to_file(FILE_ENCRYPT, encrypt_text_ce(text, x))
        else:
            if (x < 0 or y < 0 or x > 26 or y > 26):
                print("Wrong key")
            else:
                (x, y) = read_key(FILE_KEY)
                write_to_file(FILE_ENCRYPT, encrypt_text_af(text, x, y))

    elif options.decrypt_flag:
        print("Decrypt...\n")
        keys = read_key(FILE_KEY)
        encrypted_text = read_file(FILE_ENCRYPT)
        if options.cipher_Cezar_flag:
            x = read_key(FILE_KEY)[0]
            if (x < 0 ) or (x > 26):
                print("Wrong key")
            else:
                write_to_file(FILE_DECRYPT, decrypt_text_ce(encrypted_text, x))
        else:
            (x, y) = read_key(FILE_KEY)
            if (x < 0 or y < 0 or x > 26 or y > 26):
                print("Wrong key")
            else:
                write_to_file(FILE_DECRYPT, decrypt_text_af(encrypted_text, x, y))

    elif options.extra_flag:
        print("Decrypt cipher without key...\n")
        if options.cipher_Cezar_flag:
            all_possible_keys = []
            extra = read_file(FILE_EXTRA).strip()
            encrypted_text = read_file(FILE_ENCRYPT)
            if (len(extra) < len(encrypted_text)):
                length = len(extra)
            else:
                length = len(encrypted_text)
            results = set()
            for i in range(length):
                result = set()
                for x in range(26):
                    if ((decrypt_letter_ce(encrypted_text[i], x)) == extra[i]):
                        result.add(x)
                if (len(results) == 0):
                    for a in result:
                        results.add(a)
                else:
                    results = results & result
                    isEmpty = (len(results) == 0)
                    if isEmpty:
                        print("Cant find key")
            # Oddzielnie zapisałem do pliku wszystkie możliwe klucze które mogą być,
            # i porównujemy czy z prawej i z lewej strony jest jeden klucz taki samy.
            # Jeżeli jest to my znaleźliśmy dobry klucz
            all_possible_keys.append(result)
            all_possible_keys.append(" & ")
            all_possible_keys.append(results)
            write_to_file(FILE_ANALIZE, all_possible_keys.__str__())
            if len(results) == 1:
                x = results.pop()
                text = decrypt_text_ce(encrypted_text, x)
                founded_key = ''.join((x).__str__())
                print("Key(s) was found")
                write_to_file(FILE_KEY_FOUND, founded_key)
                write_to_file(FILE_DECRYPT, text)

        else:
            all_possible_keys = []
            extra = read_file(FILE_EXTRA).strip()
            encrypted_text = read_file(FILE_ENCRYPT)
            if (len(extra) < len(encrypted_text)):
                length = len(extra)
            else:
                length = len(encrypted_text)
            results = set()
            for i in range(length):
                result = set()
                for x in range(26):
                    if (gcd(x, 26) == 1):
                        for y in range(26):
                            if (decrypt_letter_af(encrypted_text[i], x, y) == extra[i]):
                                result.add((x, y))
                if (len(results) == 0):
                    for a in result:
                        results.add(a)
                else:
                    results = results & result
                    isEmpty = (len(results) == 0)
                    if isEmpty:
                        print("Cant find keys")

            all_possible_keys.append(result)
            all_possible_keys.append(" & ")
            all_possible_keys.append(results)
            write_to_file(FILE_ANALIZE, all_possible_keys.__str__())
            if len(results) == 1:
                x, y = results.pop()
                text = decrypt_text_af(encrypted_text, x, y)
                founded_key = ''.join((x, y).__str__())
                print("Key(s) was found")
                write_to_file(FILE_KEY_FOUND, founded_key)
                write_to_file(FILE_DECRYPT, text)

    elif options.all_flag:
        if options.cipher_Cezar_flag:
            print("Write all possible variants...\n")
            text = ""
            encrypted_text = read_file(FILE_ENCRYPT)
            for i in range(26):
                text += decrypt_text_ce(encrypted_text, i) + "\n"
            write_to_file(FILE_DECRYPT, text)
        else:
            print("Write all possible variants...")
            text = ""
            encrypted_text = read_file(FILE_ENCRYPT)
            for i in range(26):
                if gcd(i, 26) == 1:
                    for y in range(26):
                        text += decrypt_text_af(encrypted_text, i, y) + "\n"
            write_to_file(FILE_DECRYPT, text)