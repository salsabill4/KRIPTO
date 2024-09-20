import streamlit as st
import numpy as np

# Fungsi Enkripsi Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            letter = (ord(char) - ord('A') + ord(key[key_index % len(key)]) - ord('A')) % 26
            ciphertext.append(chr(letter + ord('A')))
            key_index += 1
        else:
            ciphertext.append(char)
    
    return ''.join(ciphertext)

# Fungsi Dekripsi Vigenere Cipher
def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            letter = (ord(char) - ord('A') - (ord(key[key_index % len(key)]) - ord('A'))) % 26
            plaintext.append(chr(letter + ord('A')))
            key_index += 1
        else:
            plaintext.append(char)
    
    return ''.join(plaintext)

# Fungsi Enkripsi Playfair Cipher
def generate_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()
    
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)
    
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    
    return [matrix[i:i+5] for i in range(0, len(matrix), 5)]

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)
    matrix_pos = {char: (row, col) for row in range(5) for col, char in enumerate(matrix[row])}
    
    plaintext = plaintext.upper().replace('J', 'I').replace(" ", "")
    i = 0
    prepared_text = []
    
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
        else:
            b = 'X'
        
        if a == b:
            b = 'X'
        
        prepared_text.append((a, b))
        i += 2
    
    ciphertext = []
    
    for a, b in prepared_text:
        row_a, col_a = matrix_pos[a]
        row_b, col_b = matrix_pos[b]
        
        if row_a == row_b:
            ciphertext.append(matrix[row_a][(col_a + 1) % 5])
            ciphertext.append(matrix[row_b][(col_b + 1) % 5])
        elif col_a == col_b:
            ciphertext.append(matrix[(row_a + 1) % 5][col_a])
            ciphertext.append(matrix[(row_b + 1) % 5][col_b])
        else:
            ciphertext.append(matrix[row_a][col_b])
            ciphertext.append(matrix[row_b][col_a])
    
    return ''.join(ciphertext)

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    matrix_pos = {char: (row, col) for row in range(5) for col, char in enumerate(matrix[row])}
    
    ciphertext = ciphertext.upper().replace('J', 'I')
    prepared_text = []
    
    i = 0
    while i < len(ciphertext):
        a = ciphertext[i]
        if i + 1 < len(ciphertext):
            b = ciphertext[i + 1]
        else:
            b = 'X'
        
        prepared_text.append((a, b))
        i += 2
    
    plaintext = []
    
    for a, b in prepared_text:
        row_a, col_a = matrix_pos[a]
        row_b, col_b = matrix_pos[b]
        
        if row_a == row_b:
            plaintext.append(matrix[row_a][(col_a - 1) % 5])
            plaintext.append(matrix[row_b][(col_b - 1) % 5])
        elif col_a == col_b:
            plaintext.append(matrix[(row_a - 1) % 5][col_a])
            plaintext.append(matrix[(row_b - 1) % 5][col_b])
        else:
            plaintext.append(matrix[row_a][col_b])
            plaintext.append(matrix[row_b][col_a])
    
    return ''.join(plaintext)

# Fungsi Enkripsi Hill Cipher
def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(' ', '')
    
    while len(plaintext) % len(key_matrix) != 0:
        plaintext += 'X'
    
    text_vector = [ord(char) - ord('A') for char in plaintext]
    key_matrix = np.array(key_matrix)
    
    ciphertext = ''
    for i in range(0, len(text_vector), len(key_matrix)):
        block = text_vector[i:i + len(key_matrix)]
        
        if len(block) < len(key_matrix):
            block += [0] * (len(key_matrix) - len(block))
        
        result_vector = np.dot(key_matrix, block) % 26
        ciphertext += ''.join(chr(num + ord('A')) for num in result_vector)
    
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    key_matrix = np.array(key_matrix)
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    inv_det = pow(det, -1, 26)  # Invers mod 26
    
    # Menghitung matriks kofaktor dan transpose
    cofactors = np.round(np.linalg.inv(key_matrix) * det).astype(int) % 26
    adjugate = np.transpose(cofactors) % 26
    inv_matrix = (inv_det * adjugate) % 26
    
    ciphertext_vector = [ord(char) - ord('A') for char in ciphertext]
    
    plaintext = ''
    for i in range(0, len(ciphertext_vector), len(key_matrix)):
        block = ciphertext_vector[i:i + len(key_matrix)]
        
        if len(block) < len(key_matrix):
            block += [0] * (len(key_matrix) - len(block))
        
        result_vector = np.dot(inv_matrix, block) % 26
        plaintext += ''.join(chr(num + ord('A')) for num in result_vector)
    
    return plaintext

def is_invertible(matrix, mod):
    det = int(np.round(np.linalg.det(matrix))) % mod
    return det != 0 and np.gcd(det, mod) == 1

# Streamlit UI
st.title("Enkripsi dan Dekripsi Plaintext ke Ciphertext")

# Upload file
uploaded_file = st.file_uploader("Upload file yang berisi plaintext", type=["txt"])
if uploaded_file is not None:
    plaintext = uploaded_file.read().decode("utf-8")
else:
    plaintext = st.text_input("Masukkan Plaintext (minimal 12 karakter)")

if len(plaintext) < 12:
    st.warning("Plaintext harus minimal 12 karakter!")

encryption_method = st.selectbox("Pilih Metode Enkripsi", ["Vigenere Cipher", "Playfair Cipher", "Hill Cipher"])

if encryption_method == "Vigenere Cipher":
    key = st.text_input("Masukkan Keyword untuk Vigenere Cipher")
    if st.button("Enkripsi dengan Vigenere Cipher"):
        if len(plaintext) >= 12 and key:
            ciphertext = vigenere_encrypt(plaintext, key)
            st.write("Ciphertext:", ciphertext)
    if st.button("Dekripsi dengan Vigenere Cipher"):
        if len(plaintext) >= 12 and key:
            decrypted_text = vigenere_decrypt(plaintext, key)
            st.write("Plaintext:", decrypted_text)

elif encryption_method == "Playfair Cipher":
    key = st.text_input("Masukkan Keyword untuk Playfair Cipher")
    if st.button("Enkripsi dengan Playfair Cipher"):
        if len(plaintext) >= 12 and key:
            ciphertext = playfair_encrypt(plaintext, key)
            st.write("Ciphertext:", ciphertext)
    if st.button("Dekripsi dengan Playfair Cipher"):
        if len(plaintext) >= 12 and key:
            decrypted_text = playfair_decrypt(plaintext, key)
            st.write("Plaintext:", decrypted_text)

elif encryption_method == "Hill Cipher":
    st.write("Masukkan Matriks Kunci untuk Hill Cipher (2x2 atau 3x3)")
    matrix_size = st.selectbox("Pilih ukuran matriks", [2, 3])
    key_matrix = []
    
    for i in range(matrix_size):
        row = st.text_input(f"Masukkan baris ke-{i+1} (pisahkan dengan spasi)", key=f"row{i+1}")
        if row:
            key_matrix.append([int(x) for x in row.split()])
    
    if st.button("Enkripsi dengan Hill Cipher"):
        if len(plaintext) >= 12 and len(key_matrix) == matrix_size and all(len(row) == matrix_size for row in key_matrix):
            key_matrix_np = np.array(key_matrix)
            if is_invertible(key_matrix_np, 26):
                ciphertext = hill_encrypt(plaintext, key_matrix)
                st.write("Ciphertext:", ciphertext)
            else:
                st.warning("Matriks kunci tidak dapat digunakan (tidak invertible dalam modulo 26).")
    
    if st.button("Dekripsi dengan Hill Cipher"):
        if len(plaintext) >= 12 and len(key_matrix) == matrix_size and all(len(row) == matrix_size for row in key_matrix):
            key_matrix_np = np.array(key_matrix)
            if is_invertible(key_matrix_np, 26):
                decrypted_text = hill_decrypt(plaintext, key_matrix)
                st.write("Plaintext:", decrypted_text)
            else:
                st.warning("Matriks kunci tidak dapat digunakan (tidak invertible dalam modulo 26).")






