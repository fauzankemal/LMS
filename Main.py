
"""
Author: Fauzan Kemal Musthofa
Description: Main library application
"""
import os
from dotenv import load_dotenv, find_dotenv
import sys
import re
import mysql.connector 
import datetime
from mysql.connector import Error
import pandas as pd

load_dotenv(find_dotenv("pass.env"))


#Run database setup
exec(open("Database setup.py").read())

#Import Library and student class
exec(open("Engine.py").read())

#Main interface and functions
def main():
    mylibrary = Library()

    print("""
    LIBRARY MANAGEMENT SYSTEM
    1. Pendaftaran Anggota Baru
    2. Pendaftaran Buku Baru
    3. Peminjaman
    4. Tampilkan Daftar Buku
    5. Tampilkan Daftar Anggota
    6. Cari Anggota
    7. Tampilkan Daftar Peminjaman
    8. Cari Buku
    9. Pengembalian
    0. Exit
    """)

    while True:
        cmd = input("Masukkan perintah (0-9): ")
        if re.search("^[0-9]$",cmd) == None:
            print("Maaf, saya tidak mengerti perintah anda")
            continue
        else:
            print("Dimengerti.")
            break
    
    #Call Library and Member class

    if cmd=="1":
        mylibrary.addmember()
        input("Tekan enter untuk kembali ke menu utama:")
        main()

 
    if cmd=="2":
        mylibrary.addbook()
        input("Tekan enter untuk kembali ke menu utama:")
        main()
    
    if cmd=="3":
        mylibrary.borrow()
        input("Tekan enter untuk kembali ke menu utama:")
        main()

    if cmd=="4":
        mylibrary.bookstock(1)
        input("Tekan enter untuk kembali ke menu utama:")
        main()
    
    if cmd=="5":
        mylibrary.listmembers(1)
        input("Tekan enter untuk kembali ke menu utama:")
        main()

    if cmd=="6":
        mylibrary.searchmember()
        input("Tekan enter untuk kembali ke menu utama:")
        main()

    if cmd=="7":
        mylibrary.transaction(1)
        input("Tekan enter untuk kembali ke menu utama:")
        main()

    if cmd=="8":
        mylibrary.searchbook()
        input("Tekan enter untuk kembali ke menu utama:")
        main()

    if cmd=="9":
        mylibrary.returnbook()
        input("Tekan enter untuk kembali ke menu utama:")
        main()

    if cmd=="0":
        print("Terima kasih, keluar dari program....")
        sys.exit()

main()
