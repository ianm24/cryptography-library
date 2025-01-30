import math
import random

DATA_FILEPATH = "./input/"
LATIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LATIN_IGNORED_CHARACTERS = " `~1234567890!@#$%^&*()-_=+[]{}\\|;:'\",<.>/?"

# =============================Helper Functions START==========================


def read_data_file(filename):
    """Reads the data file and returns a list of strings for each line."""
    data = None
    with open(DATA_FILEPATH+filename, "r") as data_file:
        lines = data_file.readlines()

        # Need to remove unneeded new line characters
        for i, line in enumerate(lines):
            line = line.replace("\n", "")
            lines[i] = line

        data = lines

    return data

def check_text_in_alphabet(text, alphabet):
    """Verifies that all letters in the text are in the alphabet"""

    # Make dictionary of alphabet
    lookup = {}
    for letter in alphabet:
        lookup[letter] = 1
    
    for letter in text:
        if letter in LATIN_IGNORED_CHARACTERS:
            continue
        check_letter = letter.upper()
        if check_letter not in lookup:
            return False
    
    return True

def encrypt_decrypt_symmetric(plaintext, key, crypto_func, alphabet=LATIN_ALPHABET):
    """For easy testing symmetric encryption functions."""
    print("==========================================================")
    print("Plaintext is: "+plaintext)
    print("Alphabet is: "+alphabet)
    print("Cipher is: "+str(crypto_func.__name__))
    print("Key is: "+str(key))
    ciphertext = crypto_func(plaintext,key,True,alphabet)
    print("Ciphertext is: "+ciphertext)
    print("Deciphered Text is: "+crypto_func(ciphertext,key,False,alphabet))
    print("==========================================================")

# =============================Helper Functions END============================


# =============================Cryptographic Functions START===================
def caesar_cipher(plaintext, key, encrypt=True, alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (integer between 0 and len(alphabet)-1)
    and returns ciphertext for the caesar cipher using a given alphabet."""

    ciphertext = ""

    #Verify key is < len(alphabet)
    if key >= len(alphabet) or key != math.ceil(key):
        print("Key must be an integer between 0 and the length of the alphabet minus one.")
        return ciphertext
    
    #Verify plaintext uses letters in alphabet
    if not check_text_in_alphabet(plaintext, alphabet):
        print("Plaintext must use letters in the given alphabet.")
        return ciphertext
    
    if not encrypt:
        key = -key

    # Clean input
    plaintext = plaintext.upper()

    # Perform cipher
    for i in range(len(plaintext)):
        letter = plaintext[i]
        if letter in LATIN_IGNORED_CHARACTERS:
            ciphertext += letter
            continue
        new_letter_idx = (alphabet.find(letter)+key) % len(alphabet)
        ciphertext += alphabet[new_letter_idx]
        
    return ciphertext

def monoalphabetic_cipher(plaintext, key, encrypt=True, alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (corresponding alphabet)
    and returns ciphertext for the monoalphabetic cipher using a given alphabet."""

    ciphertext = ""

    #Verify len(key) = len(alphabet) and key has no duplicates
    if len(key) != len(alphabet) or len(key) != len(set(key)):
        print("Key must be a corresponding alphabet with no duplicates.")
        return ciphertext
    
    #Verify key and plaintext uses letters in alphabet
    if not check_text_in_alphabet(key, alphabet) or not check_text_in_alphabet(plaintext, alphabet):
        print("Key and plaintext must use letters in the given alphabet.")
        return ciphertext

    if not encrypt:
        temp = key
        key = alphabet
        alphabet = temp

    # Clean input
    plaintext = plaintext.upper()

    # Perform cipher
    for i in range(len(plaintext)):
        letter = plaintext[i]
        if letter in LATIN_IGNORED_CHARACTERS:
            ciphertext += letter
            continue
        ciphertext += key[alphabet.find(letter)]
        
    return ciphertext

def playfair_cipher(plaintext, key, encrypt=True, combined_letters=['I','J'], filler_letter='X', alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (word) and returns ciphertext for the
    playfair cipher, skipping a given letter for the 5x5 matrix."""

    ciphertext = ""
    skip_letter = combined_letters[1]
    shift_multiplier = 1

    #Verify key and plaintext uses letters in alphabet
    if not check_text_in_alphabet(key, alphabet) or not check_text_in_alphabet(plaintext, alphabet):
        print("Key and plaintext must use letters in the given alphabet.")
        return ciphertext

    if not encrypt:
        shift_multiplier = -1

    # Clean input
    plaintext = plaintext.upper()
    plaintext = plaintext.replace(" ","")

    # Create 5x5 matrix
    cipher_matrix = ""
    used_letters = {}
    alphabet = alphabet.replace(skip_letter,"")
    for i in range(5):
        row = ""
        for j in range(5):
            letter = ""

            # Get next letter
            if len(key) > 0:
                letter = key[0]
            else:
                letter = alphabet[0]

            # append letter to row and add it to used letters
            row += letter
            alphabet = alphabet.replace(letter, "")
            key = key.replace(letter, "")
        cipher_matrix += row
    
    # print(cipher_matrix)

    # Add filler letter to double-letter pairs
    letter_pairs = [plaintext[i:i+2] for i in range(0,len(plaintext),2)]
    for i in range(len(letter_pairs)):
        pair = letter_pairs[i]
        if len(pair) == 2 and pair[0] == pair[1]:
            ciphertext += pair[0]+filler_letter+pair[1]
        else:
            ciphertext += pair
    
    if len(ciphertext) % 2 == 1:
        ciphertext += filler_letter
    letter_pairs = [ciphertext[i:i+2] for i in range(0,len(ciphertext),2)]
    ciphertext = ""

    # Perform cipher
    for i in range(len(letter_pairs)):
        pair = letter_pairs[i]
        
        if pair[0] == skip_letter:
            pair = combined_letters[0]+pair[1]
        letter1_idx = cipher_matrix.find(pair[0])
        letter1_row = math.floor(letter1_idx / 5)
        letter1_col = letter1_idx % 5

        if pair[1] == skip_letter:
            pair = pair[0]+combined_letters[0]
        letter2_idx = cipher_matrix.find(pair[1])
        letter2_row = math.floor(letter2_idx / 5)
        letter2_col = letter2_idx % 5

        # Use playfair rules to get new matrix locations
        if letter1_row == letter2_row:
            letter1_col = (letter1_col + shift_multiplier) % 5
            letter2_col = (letter2_col + shift_multiplier) % 5
        elif letter1_col == letter2_col:
            letter1_row = (letter1_row + shift_multiplier) % 5
            letter2_row = (letter2_row + shift_multiplier) % 5
        else:
            temp = letter1_col
            letter1_col = letter2_col
            letter2_col = temp
        
        letter1 = cipher_matrix[letter1_row*5 + letter1_col]
        letter2 = cipher_matrix[letter2_row*5 + letter2_col]

        ciphertext += letter1 + letter2
        
    return ciphertext

def vigenere_cipher(plaintext, key, encrypt=True, alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (word) and returns ciphertext for the
    vigenere cipher."""

    ciphertext = ""
    shift_multiplier = 1
    
    #Verify key and plaintext uses letters in alphabet
    if not check_text_in_alphabet(key, alphabet) or not check_text_in_alphabet(plaintext, alphabet):
        print("Key and plaintext must use letters in the given alphabet.")
        return ciphertext
    
    if not encrypt:
        shift_multiplier = -1

    # Clean input
    plaintext = plaintext.upper()

    # Perform cipher
    for i in range(len(plaintext)):
        key_idx = i%len(key)
        key_letter = key[key_idx]
        key_alphabet_idx = alphabet.find(key_letter)
        
        plaintext_alphabet_idx = alphabet.find(plaintext[i])
        
        ciphertext_alphabet_idx = (plaintext_alphabet_idx + shift_multiplier*key_alphabet_idx) % len(alphabet)
        ciphertext += alphabet[ciphertext_alphabet_idx]
    
    return ciphertext

def autokey_cipher(plaintext, key, encrypt=True, alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (word) and returns ciphertext for the
    autokey cipher."""

    ciphertext = ""
    shift_multiplier = 1
    
    #Verify key and plaintext uses letters in alphabet
    if not check_text_in_alphabet(key, alphabet) or not check_text_in_alphabet(plaintext, alphabet):
        print("Key and plaintext must use letters in the given alphabet.")
        return ciphertext
    
    if not encrypt:
        shift_multiplier = -1

    # Clean input
    plaintext = plaintext.upper()

    # Perform cipher
    for i in range(len(plaintext)):
        key_letter = ""
        if i < len(key) or not encrypt:
            key_letter = key[i]
        else:
            key_letter = plaintext[i-len(key)]
        
        key_alphabet_idx = alphabet.find(key_letter)
        
        plaintext_alphabet_idx = alphabet.find(plaintext[i])
        
        ciphertext_alphabet_idx = (plaintext_alphabet_idx + shift_multiplier*key_alphabet_idx) % len(alphabet)
        ciphertext += alphabet[ciphertext_alphabet_idx]

        if not encrypt:
            key += alphabet[ciphertext_alphabet_idx]
    
    return ciphertext

def generate_psuedorandom_onetimepad_key(length, alphabet=LATIN_ALPHABET):
    """Generates a psuedorandom key of a certain length to be used for the
    one-time pad cipher"""

    key = ""
    for i in range(length):
        key += alphabet[random.randint(0,len(alphabet)-1)]
    
    return key
        
def onetimepad_cipher(plaintext, key, encrypt=True, alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (truly random sequence of letters >= in
    length to plaintext) and returns ciphertext for the one-time pad cipher."""

    ciphertext = ""

    #Verify key and plaintext uses letters in alphabet
    if len(key) < len(plaintext):
        print("Key must be at least as long as plaintext.")
        return ciphertext
    
    # One-time pad is just a special case of the vigenere cipher
    ciphertext = vigenere_cipher(plaintext, key, encrypt, alphabet)

    return ciphertext

def railfence_cipher(plaintext, key, encrypt=True, alphabet=LATIN_ALPHABET):
    """Takes in plaintext and a key (integer between 2 and len(plaintext)-1
    indicating number of rails) and returns ciphertext for the railfence cipher
    using a given alphabet."""

    ciphertext = ""
    ptr = None
    if not encrypt:
        ciphertext = ["" for i in range(len(plaintext))]
        ptr = 0

    #Verify 2 <= key < len(alphabet)
    if key >= len(alphabet) or key < 2 or key != math.ceil(key):
        print("Key must be an integer between 2 and the length of the plaintext minus one.")
        return ciphertext
    
    #Verify plaintext uses letters in alphabet
    if not check_text_in_alphabet(plaintext, alphabet):
        print("Plaintext must use letters in the given alphabet.")
        return ciphertext

    # Clean input
    plaintext = plaintext.upper()

    # Perform cipher
    for i in range(key):
        # First gap is "2(k-i-1)-1" until i=k-1, then its "2(k-1)-1"
        steps = []
        if i==key-1:
            steps.append(2*(key-1))
        else:
            steps.append(2*(key-i-1))
        
        # Second gap is "2(k-1)-1" for i=0 then its "2(i-1)+1"
        if i==0:
            steps.append(2*(key-1))
        else:
            steps.append(2*(i-1)+2)

        j=0
        idx=i
        while idx < len(plaintext):
            if encrypt:
                ciphertext += plaintext[idx]
            else:
                ciphertext[idx] = plaintext[ptr]
                ptr += 1

            idx += steps[j%2]
            j += 1
    
    if not encrypt:
        ciphertext = "".join(ciphertext)
    return ciphertext
    

# =============================Cryptographic Functions End=====================

def main():
    """Imports data then gets and prints the solution."""
    data_filename = "test.txt"
    plaintext = read_data_file(data_filename)[0]
    
    encrypt_decrypt_symmetric(plaintext,5,caesar_cipher)

    mono_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM"
    encrypt_decrypt_symmetric(plaintext,mono_alphabet,monoalphabetic_cipher)

    playfair_key = "WORDSTHATARECOOL"
    encrypt_decrypt_symmetric(plaintext,playfair_key,playfair_cipher)

    vignere_key = "FUNANDEXCITING"
    encrypt_decrypt_symmetric(plaintext,vignere_key,vigenere_cipher)

    autokey_key = "SENTENCES"
    encrypt_decrypt_symmetric(plaintext,autokey_key,autokey_cipher)

    onetimepad_key = generate_psuedorandom_onetimepad_key(len(plaintext))
    encrypt_decrypt_symmetric(plaintext,onetimepad_key,onetimepad_cipher)

    railfence_key = 3
    encrypt_decrypt_symmetric(plaintext,railfence_key,railfence_cipher)


if __name__ == "__main__":
    main()