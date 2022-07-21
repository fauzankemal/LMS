"""
Author: Fauzan Kemal Musthofa
Description: Create library and student class as the main code
"""
class Library:
    """
    Contains functions that regulate books and members, including:
    1. Read existing database (__init__)
    2. View list of books ( bookstock() )
    3. Add book to the database ( addbook() )
    4. Book search engine( searchbook() )
    5. View list of members ( listmembers() )
    6. Add a member ( addmember() )
    7. Search members ( searchmember() )
    8. Check outstanding books ( transaction () )
    8. Borrow book ( borrow() )
    9. Return book ( returnbook() )
    """
    def __init__(self):
        """Fetch three tables at the start of the program"""

        read_books_query = """SELECT id_buku, nama_buku, penulis, kategori,  stok_tersedia FROM lms.stok_buku;"""
        read_member_query = """SELECT id, nama_lengkap, alamat, no_hp_telepon FROM lms.list_member"""
        read_lending_query = """
        SELECT a.id_peminjam, c.nama_lengkap, b.nama_buku, a.id_buku, a.tanggal_keluar, a.tanggal_kembali, a.id_transaksi
        FROM lms.buku_keluar a
            LEFT JOIN lms.stok_buku b
                ON a.id_buku = b.id_buku
            LEFT JOIN lms.list_member c 
                ON a.id_peminjam = c.id
        """
        try:
            mycursor.execute(read_books_query)
            self.read_books = mycursor.fetchall()

            mycursor.execute(read_member_query)
            self.read_member = mycursor.fetchall()

            mycursor.execute(read_lending_query)
            self.read_lending = mycursor.fetchall()
            
        except Error as err:
            print(f"Error: {err}")
    
    #View list of books
    def bookstock(self,printer=0):
        """
        View list of books in the library, converting SQL query into presentable dataframe
        Args:
            printer: print the dataframe (1), default is zero

        Returns:
            books_db: List of books in the library in a df format
        """
        books_db = pd.DataFrame(self.read_books, columns = ["ID Buku", "Judul Buku", "Penulis", "Kategori Buku", "Stok tersedia"])
        if printer == 1:
            print("Daftar Buku dan ketersediaannya:")
            print(books_db)
        else:
            pass
        return books_db
        
    #Add book to the library
    def addbook(self):
        """
        Add a new book to the SQL database . User must input book ID, title, author, and category/genre

        returns:
        Nothing

        """
        print("Silahkan isi data buku yang dimasukkan: ")
        while True:
            id_buku = input("Tuliskan ID buku: ")
            if id_buku == "":
                print("ID buku tidak boleh kosong!")
                continue
            elif re.search("[^0-9]",id_buku) != None:
                print("ID buku harus berupa angka dan harus 6 digit")
                continue
            elif len(id_buku)!=6:
                print("ID buku harus 6 digit")
                continue
            else:
                break
        
        while True:
            nama_buku = input("Tuliskan judul buku: ")
            if nama_buku == "":
                print("Judul buku tidak boleh kosong")
                continue
            elif len(nama_buku)<5:
                print("Judul buku minimal 5 karakter")
                continue
            else:
                break

        while True:
            penulis = input("Tuliskan penulis buku: ")
            if nama_buku == "":
                print("Penulis tidak boleh kosong")
                continue
            elif len(nama_buku)<5:
                print("Penulis minimal 5 karakter")
                continue
            else:
                break
        
        while True:
            kategori_buku = input("Tuliskan kategori buku: ")
            if kategori_buku == "":
                print("Judul buku tidak boleh kosong")
                continue
            elif len(kategori_buku)<3:
                print("Judul buku minimal 3 karakter")
                continue
            else:
                break
        
        while True:
            try:
                stok_tersedia = int(input("Tuliskan banyaknya stok buku yang bisa dipinjam: "))
            except ValueError:
                print("Hanya tuliskan angka saja")
                continue
            else:
                break
        
        insertbook_query = """
        INSERT INTO lms.stok_buku(
                        id_buku, nama_buku, kategori, penulis, stok_tersedia)
            VALUES (%s,%s,%s,%s,%s);"""
        try:
            mycursor.execute(insertbook_query,(id_buku, nama_buku, kategori_buku, penulis, stok_tersedia))
            connection.commit()
            print("Sukses memasukkan buku ke dalam database")
        except mysql.connector.Error as err:
            if err.errno == 1062:
                print("ID Buku sudah terdaftar")
            else:
                raise

        

    #Searchbook
    def searchbook(self, user=1,keyword=""):
        """
        Book search function. User can input book ID, title, or author of the book

        Args:
            user: Whether we call the function as a user-input search function (1) or we can call the function for other commands (0)
            keyword: Used when user==1, the search keyword

        Returns:
            searched: list of searched book(s) in a df format
        """
        #Queries
        searchid_query = """SELECT * FROM lms.stok_buku WHERE id_buku LIKE %s"""
        searchtitle_query = "SELECT * from lms.stok_buku WHERE nama_buku LIKE %s OR penulis LIKE %s"

        #Non-user input search function
        if user==0:
            try:
                mycursor.execute(searchid_query,[keyword])
                searched = pd.DataFrame(mycursor.fetchall(), columns = ["ID Buku", "Judul Buku", "Penulis", "Kategori Buku", "Stok tersedia"])
                return searched
            except Error as err:
                print(f"Error: {err}")
                return
        else:
            pass

        while True:
            search = input("Masukkan ID buku, judul buku, atau penulis: ")
            if search=="":
                print("Jawaban tidak boleh kosong")
                continue
            else:
                break
        #ID-based search
        if re.search("^[0-9][0-9][0-9][0-9][0-9][0-9]$",search) != None:
            try:
                mycursor.execute(searchid_query,[search])
                searched = pd.DataFrame(mycursor.fetchall(), columns = ["ID Buku", "Judul Buku", "Penulis", "Kategori Buku", "Stok tersedia"])
                if searched.empty:
                    print("Buku tidak ditemukan")
                    return searched
                else:
                    print(searched)
                    return searched
                    
            except Error as err:
                print(f"Error: {err}")
        
        #Author/title-based search
        else:
            try:
                mycursor.execute(searchtitle_query,["%"+search+"%", "%"+search+"%"])
                searched = pd.DataFrame(mycursor.fetchall(), columns = ["ID Buku", "Judul Buku", "Penulis", "Kategori Buku", "Stok tersedia"])
                if searched.empty:
                    print("Buku tidak ditemukan")
                    return searched
                else:
                    print(searched)
                    return searched
            except Error as err:
                print(f"Error: {err}")
    
    #View list of members
    def listmembers(self,printer=0):
        """
        Show list of members from the database

        Args:
            printer: whether the database is printed to the console (1) or not (0)

        Returns:
            db_members: list of members in a df format
        """
        db_members = pd.DataFrame(self.read_member, columns = ["ID", "Nama Lengkap", "Alamat", "No HP/Telepon"])
        if printer==1:
            print("Daftar anggota perpus:")
            print(db_members)
        else:
            pass
        return db_members

    #Add members
    def addmember(self):
        """
        Add a new library member from user-input data to the SQL database

        Returns:
            Nothing

        """

        print("Silahkan isi data calon anggota: ")
        while True:
            name = input("Masukkan nama lengkap calon anggota: ")
            if len(name)<3:
                print("Masukkan minimal 3 karakter")
                continue
            elif re.search("[0-9]",name) != None:
                print("Tidak boleh ada angka")
                continue
            else:
                break
        
        while True:
            address = input("Masukkan alamat calon anggota: ")
            if len(address)<10:
                print("Alamat terlalu pendek, minimal 10 karakter")
                continue
            else:
                break
        
        while True:
            phone = input("Masukkan No. HP/telepon calon anggota: ")
            if re.search("[^0-9+]",phone) != None:
                print("Tidak boleh ada karakter selain angka atau '+' untuk kode negara")
                continue
            if len(phone)<10:
                print("No hp/telepon terlalu pendek. Jika pakai no. telepon kabel, gunakan kode wilayah")
                continue
            else:
                break

        insertmember_query = """
        INSERT INTO lms.list_member(
                 nama_lengkap, alamat, no_hp_telepon)
            VALUES (%s, %s, %s)"""
        
        try:
            mycursor.execute(insertmember_query,(name, address, phone))
            connection.commit()
            print("Sukses memasukkan anggota ke dalam database")
        except Error as err:
             print(f"Error: {err}")
    
    def searchmember(self):
        """
        Search function for library members, can be searched through ID, phone number, or name

        Returns:
            searched_member: List of members found in a df format

        """
        search_m = input("Masukkan ID, no telepon, atau nama anggota: ")
        while True:
            if search_m=="":
                print("Jawaban tidak boleh kosong")
                continue
            else:
                break
        #ID-based search
        if len(search_m)<10 and re.search("[0-9+]",search_m) != None:
            searchidmember_query = """SELECT * FROM lms.list_member WHERE id LIKE %s"""
            mycursor.execute(searchidmember_query,["%"+search_m+"%"])
            searched_member = pd.DataFrame(mycursor.fetchall(), columns = ["ID", "Nama Lengkap", "Alamat", "No HP/Telepon"])
            if searched_member.empty:
                print("Anggota tidak ditemukan")
                return searched_member
            else:
                print(searched_member)
                return searched_member

        #Phone number-based search
        elif len(search_m)>9 and re.search("[0-9]",search_m) != None:
            searchphonemember_query = """SELECT * FROM lms.list_member WHERE no_hp_telepon LIKE %s"""
            mycursor.execute(searchphonemember_query,["%"+search_m+"%"])
            searched_member = pd.DataFrame(mycursor.fetchall(), columns = ["ID", "Nama Lengkap", "Alamat", "No HP/Telepon"])
            if searched_member.empty:
                print("Anggota tidak ditemukan")
                return searched_member
            else:
                print(searched_member)
                return searched_member

        #Name-based search
        else:
            searchname_query = """SELECT * FROM lms.list_member WHERE nama_lengkap LIKE %s"""
            mycursor.execute(searchname_query,["%"+search_m+"%"])
            searched_member = pd.DataFrame(mycursor.fetchall(), columns = ["ID", "Nama Lengkap", "Alamat", "No HP/Telepon"])
            if searched_member.empty:
                print("Anggota tidak ditemukan")
                return searched_member
            else:
                print(searched_member)
                return searched_member
    
    #Borrowing books
    def borrow(self):
        """
        A function to borrow books. There are three main steps:
            1. Search books
            2. Searh members
            3. Execute SQL queries (add transaction data, adjust book stocks)

        """
        #Check if dataset exists
        check_book = self.bookstock()
        check_member = self.listmembers()
        if check_book.empty:
            return "Database buku masih kosong, isi database buku terlebih dahulu"
        elif check_member.empty:
            return "Database anggota masih kosong, isi database anggota terlebih dahulu"
        else:
            pass

        #Search member
        while True:
            member_result = self.searchmember()
            if len(member_result)!=1:
                print("Hasil pencarian tidak menghasilkan 1 anggota, silakan melakukan pencarian kembali")
                continue
            else:
                print(f"Baik, {member_result.iloc[0]['Nama Lengkap']} (ID: {member_result.iloc[0]['ID']}) akan meminjam sebuah buku ")
                break

        #Search books
        while True:
            books_result = self.searchbook()
            if len(books_result)!=1:
                print("Hasil pencarian tidak menghasilkan 1 buku, silakan melakukan pencarian kembali")
                continue
            elif books_result.iloc[0]['Stok tersedia']<1:
                print("Buku ini tidak tersedia, silakan pilih buku lain")
                continue
            else:
                print(f"Baik,buku berjudul {books_result.iloc[0]['Judul Buku']} (ID: {books_result.iloc[0]['ID Buku']}) akan dipinjam oleh {member_result.iloc[0]['Nama Lengkap']} (ID: {member_result.iloc[0]['ID']})")
                break

        #Insert transaction into table (+ date, current and 3 days from now)
        date_today = datetime.date.today()
        date_3days = date_today + datetime.timedelta(days=3)
        borrow_query = """
        INSERT INTO lms.buku_keluar(
                id_buku,id_peminjam,tanggal_keluar,tanggal_kembali)
            VALUES (%s,%s,%s,%s)
        """
        reducestock_query = """
        UPDATE lms.stok_buku
            SET stok_tersedia = %s
            WHERE id_buku = %s;"""
        try:
            mycursor.execute(borrow_query,[int(books_result.iloc[0]['ID Buku']) , int(member_result.iloc[0]['ID']), date_today, date_3days])
            connection.commit()
            mycursor.execute(reducestock_query,[int(books_result.iloc[0]['Stok tersedia'])-1, int(books_result.iloc[0]['ID Buku'])])
            connection.commit()
            print("Buku berhasil dipinjamkan")
        except Error as err:
             print(f"Error: {err}")
    
    def transaction(self, printer = 0):
        transaction_db = pd.DataFrame(self.read_lending, columns = ["ID Peminjam", "Nama Lengkap", "Nama Buku", "ID Buku", "Tanggal Keluar", "Tanggal Kembali", "ID Transaksi"])
        if printer == 1:
            if transaction_db.empty:
                print("Belum ada buku yang dipinjam")
            else:
                print(transaction_db)
        else:
            pass
        return transaction_db

    def outsidebooks(self):
        """
        Function to search outstanding books.
        Outstanding books can be searched through member ID, member name, or transaction ID

        Returns:
            searched_trans: Search transactions in a df format
        """
        while True:
            search_ob = input("Masukkan ID atau nama anggota: ")
            if search_ob == "":
                print("Jawaban tidak boleh kosong")
                continue
            else:
                break

        search_trans =  input("Masukkan ID transaksi (jika ada): ")

        search_trans_query = """
        SELECT a.id_peminjam, c.nama_lengkap, b.nama_buku, a.id_buku, a.tanggal_keluar, a.tanggal_kembali, a.id_transaksi
        FROM lms.buku_keluar a
            LEFT JOIN lms.stok_buku b
                ON a.id_buku = b.id_buku
            LEFT JOIN lms.list_member c 
                ON a.id_peminjam = c.id
        WHERE (a.id_peminjam LIKE %s OR c.nama_lengkap LIKE %s AND a.id_transaksi LIKE %s)
        """
        try:
            mycursor.execute(search_trans_query,["%"+search_ob+"%", "%"+search_ob+"%", "%"+search_trans+"%"])
            searched_trans = pd.DataFrame(mycursor.fetchall(), columns = ["ID Peminjam", "Nama Lengkap", "Nama Buku", "ID Buku", "Tanggal Keluar", "Tanggal Kembali", "ID Transaksi"])
        except Error as err:
            print(f"Error: {err}")

        if searched_trans.empty:
            print("Catatan peminjaman tidak ditemukan")
            return searched_trans
        else:
            print(searched_trans)
            return searched_trans

    def returnbook(self):
        """
        Functions to return outstanding books.
        Deleting 1 book from buku_keluar table, adding one stock to stok_buku table
        """
        #Check if database exists
        check_trans = self.transaction()
        if check_trans.empty:
            print("Belum ada buku yang sedang dipinjamkan")
            return 
        else:
            pass

        #Search outstanding books
        while True:
            trans_result = self.outsidebooks()
            if len(trans_result)!=1:
                print("Hasil pencarian tidak memberikan satu catatan peminjaman, silahkan melakukan pencarian kembali")
                continue
            else:
                break

        #Edit database to return books
        return_query = """
        DELETE FROM lms.buku_keluar
        WHERE id_transaksi = %s
        """
        reducestock_query = """
        UPDATE lms.stok_buku
            SET stok_tersedia = %s
            WHERE id_buku = %s;
        """
        book_returned = self.searchbook(0,int(trans_result.iloc[0]['ID Buku']))

        try:
            mycursor.execute(return_query,[int(trans_result.iloc[0]['ID Transaksi'])])
            connection.commit()
            mycursor.execute(reducestock_query,[int(book_returned.iloc[0]['Stok tersedia'])+1, int(book_returned.iloc[0]['ID Buku'])])
            connection.commit()
            print("Buku berhasil dikembalikan")
        except Error as err:
             print(f"Error: {err}")

    








 
            

        
