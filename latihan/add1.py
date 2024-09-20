import streamlit as st
import numpy as np

# Fungsi Enkripsi Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = []
    key_index = 0  # Untuk melacak posisi huruf pada keyword
    
    for char in plaintext:
        if char.isalpha():
            # Proses enkripsi hanya untuk karakter alfabet
            letter = (ord(char) - ord('A') + ord(key[key_index % len(key)]) - ord('A')) % 26
            ciphertext.append(chr(letter + ord('A')))
            key_index += 1  # Hanya majukan key_index jika huruf
        else:
            # Pertahankan karakter non-alfabetik (spasi, tanda baca, dll.)
            ciphertext.append(char)
    
    return ''.join(ciphertext)

# Fungsi Enkripsi Playfair Cipher
def generate_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()
    
    # Menambahkan karakter dari keyword ke matriks
    for char in key:
        if char not in seen and char.isalpha():  # Hanya tambahkan huruf alfabet
            seen.add(char)
            matrix.append(char)
    
    # Menambahkan sisa alfabet yang belum ada ke matriks
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # J digabung dengan I
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    
    return [matrix[i:i+5] for i in range(0, len(matrix), 5)]

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)
    matrix_pos = {char: (row, col) for row in range(5) for col, char in enumerate(matrix[row])}
    
    # Handle same letter pairs and add X if length is odd
    plaintext = plaintext.upper().replace('J', 'I').replace(" ", "")
    i = 0
    prepared_text = []
    
    # Memastikan teks dipasangkan dengan benar
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
        else:
            b = 'X'  # Tambahkan X jika pasangan tidak lengkap
        
        if a == b:
            b = 'X'  # Tambahkan X jika ada pasangan huruf yang sama
        
        prepared_text.append((a, b))
        i += 2  # Lompat ke pasangan berikutnya
    
    ciphertext = []
    
    # Proses enkripsi pasangan huruf
    for a, b in prepared_text:
        row_a, col_a = matrix_pos[a]
        row_b, col_b = matrix_pos[b]
        
        if row_a == row_b:
            # Jika kedua huruf ada di baris yang sama, geser ke kanan
            ciphertext.append(matrix[row_a][(col_a + 1) % 5])
            ciphertext.append(matrix[row_b][(col_b + 1) % 5])
        elif col_a == col_b:
            # Jika kedua huruf ada di kolom yang sama, geser ke bawah
            ciphertext.append(matrix[(row_a + 1) % 5][col_a])
            ciphertext.append(matrix[(row_b + 1) % 5][col_b])
        else:
            # Jika tidak di baris atau kolom yang sama, buat persegi panjang dan ambil sudut yang lain
            ciphertext.append(matrix[row_a][col_b])
            ciphertext.append(matrix[row_b][col_a])
    
    return ''.join(ciphertext)

# Fungsi Enkripsi Hill Cipher
def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(' ', '')
    if len(plaintext) % len(key_matrix) != 0:
        plaintext += 'X' * (len(key_matrix) - len(plaintext) % len(key_matrix))
    
    text_vector = [ord(char) - ord('A') for char in plaintext]
    key_matrix = np.array(key_matrix)
    
    ciphertext = ''
    for i in range(0, len(text_vector), len(key_matrix)):
        block = text_vector[i:i + len(key_matrix)]
        result_vector = np.dot(key_matrix, block) % 26
        ciphertext += ''.join(chr(num + ord('A')) for num in result_vector)
    
    return ciphertext

# Streamlit UI
st.title("Enkripsi Plaintext ke Ciphertext")

# Pilihan metode enkripsi
encryption_method = st.selectbox("Pilih Metode Enkripsi", ["Vigenere Cipher", "Playfair Cipher", "Hill Cipher"])

# Input plaintext
plaintext = st.text_input("Masukkan Plaintext (minimal 12 karakter)")

# Verifikasi panjang plaintext
if len(plaintext) < 12:
    st.warning("Plaintext harus minimal 12 karakter!")

# Vigenere Cipher
if encryption_method == "Vigenere Cipher":
    key = st.text_input("Masukkan Keyword untuk Vigenere Cipher")
    if st.button("Enkripsi dengan Vigenere Cipher"):
        if len(plaintext) >= 12 and key:
            ciphertext = vigenere_encrypt(plaintext, key)
            st.write("Ciphertext:", ciphertext)
        else:
            st.warning("Masukkan keyword dan pastikan panjang plaintext minimal 12 karakter!")

# Playfair Cipher
elif encryption_method == "Playfair Cipher":
    key = st.text_input("Masukkan Keyword untuk Playfair Cipher")
    if st.button("Enkripsi dengan Playfair Cipher"):
        if len(plaintext) >= 12 and key:
            ciphertext = playfair_encrypt(plaintext, key)
            st.write("Ciphertext:", ciphertext)
        else:
            st.warning("Masukkan keyword dan pastikan panjang plaintext minimal 12 karakter!")

# Hill Cipher
elif encryption_method == "Hill Cipher":
    st.write("Masukkan Matriks Kunci untuk Hill Cipher (2x2 atau 3x3)")
    matrix_size = st.selectbox("Pilih ukuran matriks", [2, 3])
    key_matrix = []
    
    for i in range(matrix_size):
        row = st.text_input(f"Masukkan baris ke-{i+1} (pisahkan dengan spasi)", key=f"row{i+1}")
        if row:
            key_matrix.append([int(x) for x in row.split()])
    
    if st.button("Enkripsi dengan Hill Cipher"):
        if len(plaintext) >= 12 and len(key_matrix) == matrix_size:
            ciphertext = hill_encrypt(plaintext, key_matrix)
            st.write("Ciphertext:", ciphertext)
        else:
            st.warning("Masukkan matriks kunci yang sesuai dan pastikan panjang plaintext minimal 12 karakter!")