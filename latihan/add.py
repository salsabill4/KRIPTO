import streamlit as st

st.title('Hitung Luas Persegi Panjang')

panjang = st.number_input ("Masukkan Nilai Panjang", 0)
lebar = st.number_input ("Masukkan Nilai Lebar", 0)
hitung = st.button ("Hitung Luas")

if hitung :
    luas = panjang * lebar
    st.write ("Luas Persegi Panjang Adalah = ", luas)