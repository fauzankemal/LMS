"""
Author: Fauzan Kemal Musthofa
Project: Library Management System
Usage: Setup database for the first time

"""


##Set variables
nama_host = "localhost"
user = "root"
password = os.getenv('SQLPW')


##Execution

#Create connection
connection = mysql.connector.connect(host = nama_host, user = user, password = password)

#Make cursor
mycursor = connection.cursor()

#Create database and tables
db_query = "CREATE SCHEMA IF NOT EXISTS lms"

#Create necessary tables
tb1_query = """
CREATE TABLE IF NOT EXISTS lms.list_member (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nama_lengkap VARCHAR(300) NOT NULL,
    alamat VARCHAR(500) NOT NULL,
    no_hp_telepon VARCHAR(20) NOT NULL 
	);
"""
tb2_query = """
CREATE TABLE IF NOT EXISTS lms.stok_buku (
	id_buku INT PRIMARY KEY,
    nama_buku VARCHAR(300) NOT NULL,
    penulis VARCHAR(300) NOT NULL,
    kategori VARCHAR(50) NOT NULL,
    stok_tersedia INT NOT NULL
	);
"""

tb3_query = """
CREATE TABLE IF NOT EXISTS lms.buku_keluar (
    id_transaksi INT PRIMARY KEY AUTO_INCREMENT,
    id_buku INT,
	FOREIGN KEY (id_buku) REFERENCES lms.stok_buku(id_buku),
    id_peminjam INT,
    FOREIGN KEY (id_peminjam) REFERENCES lms.list_member(id),
	tanggal_keluar DATE,
    tanggal_kembali DATE
    );
"""

mycursor.execute(db_query)

mycursor.execute(tb1_query)

mycursor.execute(tb2_query)

mycursor.execute(tb3_query)

#Connect Database & Cursor with new database
connection = mysql.connector.connect(host = nama_host, user = user, password = password, database = "lms")
mycursor = connection.cursor()


#Success indicator
print("Koneksi ke MySQL berhasil, databse siap digunakan")