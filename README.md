## Library Management System

A simple, Python console-based library management system that manages books and library members. All books and members' information are stored in an SQL database. This software is designed for the librarian or library administrator. The program runs in the Indonesian language.

## Features

<img src="file:///C:/Users/fkemal/AppData/Roaming/marktext/images/2022-07-21-15-08-34-image.png" title="" alt="" data-align="center">

##### 1. Pendaftaran Anggota Baru (Register a new library member)

Register user-input member information and save it to the SQL database



##### 2. Pendaftaran Buku Baru (Register a new book)

Register user-input book information and save it to the SQL database



##### 3. Peminjaman (Borrow books)

Borrow a book based on existing registered users and books. Each borrowing (we'll call it "transaction" afterward) is stored in the database



##### 4. Tampilkan Daftar Buku (Show list of books)

Show list of books in the database

   

##### 5. Tampilkan Daftar Anggota (Show list of  members)

Show list of books in the database



##### 6. Cari Anggota (Find members)

Search library members, based on ID, name, or phone number. he search function relies on MySQL query `LIKE`



##### 7. Tampilkan Daftar Peminjaman (Show list of outstanding books)

Show list of books borrowed



##### 8. Cari Buku (Search books)

Search books in the library based on books ID, title, or author. The search function relies on MySQL query `LIKE`



##### 9. Pengembalian (Return book)

Return borrowed books, removing transaction data



## How to Run

Before running, make sure that you have installed SQL/have access to SQL server and Python. Several python packages  used that may need installation:

- `dotenv` : Store environment variable in a file (used it to store password to access SQL database)

- `pandas` : Simple data manipulation

- `mysql.connector` : Module to run SQL queries in a `.py`



Then, in `Database setup.py`, please change the `nama_host` (hostname), `user`, and `password` variables suitable for your SQL server.



Finally, just run `Main.py`



## Future Improvements

- Needs to be tested on a grander scale (thousands of books, thousands of users, multi-admin, etc)

- Interface improvements to make the job of librarian easier
