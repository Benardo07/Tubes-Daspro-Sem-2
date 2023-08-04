import data
from base import *
# import random
from util import hitungJumlah, get_cycle, cycle_length

def run(command: str, state: State) -> int:
    # menerima command yang diberikan dan state program
    # fungsi-fungsi spesifikasi memanipulasi state program lewat side effects
    # nilai return adalah 0 (normal), 1 (kesalahan)
    
    if command == "exit":
        exit(state)
        return 1 # kalau berhasil return, exit gagal
    elif command == "login":
        return login(state)
    elif command == "logout":
        return logout(state)
    elif command == "save":
        return save(state)
    elif command == "help":
        return help(state)
    elif command == "summonjin":
        return summonjin(state)
    elif command == "hapusjin":
        return hapusjin(state)
    elif command == "ubahjin":
        return ubahjin(state)
    elif command == "cekUser":
        return cekUser(state)
    elif command == "bangun":
        return bangun(state)
    elif command == "kumpul" :
        return kumpul(state)
    elif command == "batchkumpul":
        return batchkumpul(state)
    elif command == "batchbangun":
        return batchbangun(state)
    elif command == "cekBahan":
        return cekBahan(state)
    elif command == "cekCandi":
        return cekCandi(state)
    elif command == "ayamberkokok":
        return ayamberkokok(state)
    elif command == "hancurkancandi":
        return hancurkancandi(state)
    elif command == "laporanjin":
        return laporanjin(state)
    elif command == "laporancandi":
        return laporancandi(state)
    # lanjutkan spam elif 
    else:
        print("Perintah tidak diketahui")
        return 1

# Inisialisasi LCG
# lcg = LCG(get_cycle(35, 21, 31, 100), cycle_length(0, 21, 31, 100), 0)
lcg_len = cycle_length(3, 3, 0, 28657)
lcg = LCG(get_cycle(3, 3, 0, 28657, lcg_len), lcg_len, 0)

def get_randint(lcg: LCG, min: int, max: int) -> int:
    # ambil angka dari LCG dan majukan index
    while True:
        lcg.index = (lcg.index + 1) % lcg.length
        res = lcg.cycle[lcg.index] % (max + 1)
        if res >= min: break
    return res

def save(state: State) -> int:
    dir = input("Masukkan nama folder: ")
    return data.__save__(state, dir)
    
def exit(state: State) -> None:
    while True:
        choice = input("Apakah Anda mau melakukan penyimpanan file yang sudah diubah? (y/n) ")
        if choice == "Y" or choice == "y":
            to_save = True
            break
        elif choice == "N" or choice == "n":
            to_save = False
            break
    
    if to_save:
        data.__save__(state, "")
        quit()
    else:
        quit()

def login(state: State) -> int:
    users = state.t_user.users
    n = state.t_user.length
    
    if state.c_user.username != ANON.username:
        print("Pengguna sudah login!")
        return 1
    
    username = input("Username: ")
    password = input("Password: ")

    # contoh loop setelah penggunaan tabel
    for i in range(n):
        if (users[i].username != USER_MARK.username
        and username == users[i].username):
            # user ditemukan
            if password == users[i].password:
                # password benar
                state.c_user = users[i]
                print(f"Selamat datang, {state.c_user.username}!")
                print("Masukkan command “help” untuk daftar command yang dapat kamu panggil.")
                return 0
            else:
                print("Password salah")
                return 1
    
    print("Username tidak terdaftar!")                
    return 1

def logout(state: State) -> int:
    if state.c_user.username == ANON.username:
        print("Pengguna belum login!")
        return 1
    
    state.c_user = ANON
    return 0

def bangun(state : State) -> int:
    if state.c_user.role == "Pembangun":
        # pasir = random.randint(1,5)
        # batu = random.randint(1,5)
        # air = random.randint(1,5)
        pasir = get_randint(lcg, 1, 5)
        batu = get_randint(lcg, 1, 5)
        air = get_randint(lcg, 1, 5)
        
        if pasir <= state.t_material.materials[0].quantity and batu <= state.t_material.materials[1].quantity and air <= state.t_material.materials[2].quantity:
            print("Candi berhasil di bangun.")
            idx = 0
            if(state.t_temple.length < 100):
                for d in range(1,state.t_temple.length + 1):
                    ada = False
                    for i in range(state.t_temple.length):
                        if(d == state.t_temple.temples[i].id):
                            ada = True
                            break
                    
                    if not ada :
                        idx = d
                        break
                    else:
                        idx = d + 1
                    
                if(idx == 0):
                    idx = 1
                
                if(state.t_temple.temples[state.t_temple.length].id == -1) and state.t_temple.length <= 99 :
                    state.t_temple.temples[state.t_temple.length] = Temple(idx, state.c_user.username,pasir,batu,air)
                    state.t_temple.length += 1

            print("Sisa candi yang perlu di bangun : ",100-state.t_temple.length,".")
            for k in range(3):
                if(state.t_material.materials[k].name == "pasir"):
                    state.t_material.materials[k].quantity -= pasir
                elif(state.t_material.materials[k].name == "batu"):
                    state.t_material.materials[k].quantity -= batu
                elif(state.t_material.materials[k].name == "air"):
                    state.t_material.materials[k].quantity -= air
            return 0
        else:
            print("Bahan bangunan tidak mencukupi.")
            print("Candi tidak bisa dibangun!")
            return 1
    else: 
        print("Cuman jin pembangun yang bisa membangun candi")
        return 1

def kumpul(state : State) -> int:
    if state.c_user.role == "Pengumpul":
        # pasir = random.randint(0,5)
        # batu = random.randint(0,5)
        # air = random.randint(0,5)
        pasir = get_randint(lcg, 0, 5)
        batu = get_randint(lcg, 0, 5)
        air = get_randint(lcg, 0, 5)

        print("Jin menemukan ",pasir," pasir ", batu , " batu, dan ", air , " air.")
        for k in range(3):
            if(state.t_material.materials[k].name == "pasir"):
                state.t_material.materials[k].quantity += pasir
            elif(state.t_material.materials[k].name == "batu"):
                state.t_material.materials[k].quantity += batu                
            elif(state.t_material.materials[k].name == "air"):
                state.t_material.materials[k].quantity += air
        return 0
    else:
        print("Cuman jin pengumpul yang bisa melakukan kumpul.")
        return 1
    
def batchkumpul(state : State) -> int:
    if(state.c_user.username == "Bondowoso"):
        i = 0
        jumlah_pengumpul = 0
        pasir = 0
        batu = 0
        air = 0

        while state.t_user.users[i].role != USER_MARK.role and i < MAX_USER:
            if(state.t_user.users[i].role == "Pengumpul"):
                jumlah_pengumpul += 1
                pasir += get_randint(lcg, 0, 5)
                batu += get_randint(lcg, 0, 5)
                air += get_randint(lcg, 0, 5)
            i += 1
        if(jumlah_pengumpul == 0):
            print("Kumpul gagal. Anda tidak punya jin pengumpul. Silahkan summon terlebih dahulu.")
            return 1
        else:
            print("Mengerahkan ", jumlah_pengumpul, " jin untuk mengumpulkan bahan.")
            print("Jin menemukan total ", pasir, " pasir, ", batu, " batu, dan ", air, " air.")
            for k in range(3):
                if(state.t_material.materials[k].name == "pasir"):
                    state.t_material.materials[k].quantity += pasir
                elif(state.t_material.materials[k].name == "batu"):
                    state.t_material.materials[k].quantity += batu
                elif(state.t_material.materials[k].name == "air"):
                    state.t_material.materials[k].quantity += air
            return 0

    else: 
        print("Cuman Bondowoso yang bisa melakukan batchkumpul.")
        return 1

def batchbangun(state : State) -> int:
    if(state.c_user.username == "Bondowoso"):
        i = 0
        jumlah_pembangun = 0
        pasir = 0
        batu = 0
        air = 0
        TBahan = [-1,-1,-1,-1]
        bahan = [TBahan for i in range(100)]
        while state.t_user.users[i].role != USER_MARK.role and i < MAX_USER:
            if(state.t_user.users[i].role == "Pembangun") :
                pasir = get_randint(lcg, 1, 5)
                batu = get_randint(lcg, 1, 5)
                air = get_randint(lcg, 1, 5)
                bahan[jumlah_pembangun] = [pasir,batu,air,state.t_user.users[i].username]
                jumlah_pembangun += 1
            i += 1
        
        TotPasir = hitungJumlah(bahan,0,jumlah_pembangun)
        TotBatu = hitungJumlah(bahan,1,jumlah_pembangun)
        TotAir = hitungJumlah(bahan,2,jumlah_pembangun)

        if(jumlah_pembangun == 0):
            print("Bangun gagal.Anda tidak punya jin pembangun. Silahkan summon terlebih dahulu.")
            return 1
        elif TotPasir <= state.t_material.materials[0].quantity and TotBatu <= state.t_material.materials[1].quantity and TotAir <= state.t_material.materials[2].quantity:   
            print("Mengerahkan ", jumlah_pembangun, " jin untuk membangun candi dengan total bahan ", TotPasir, " pasir, " , TotBatu, " batu, dan ",TotAir, " air." )    
            print("Jin berhasil membangun total ", jumlah_pembangun, " candi.") 
            j = 0
            idx = 0
            while j < jumlah_pembangun and state.t_temple.length < 100:
                for d in range(1,state.t_temple.length + 1):
                    ada = False
                    for i in range(state.t_temple.length):
                        if(d == state.t_temple.temples[i].id):
                            ada = True
                            break
                    if not(ada) :
                        idx = d
                        break
                    else:
                        idx = d + 1
                if (idx == 0):
                    idx = 1
                if state.t_temple.temples[state.t_temple.length].id == -1 and state.t_temple.length < 100:
                    state.t_temple.temples[state.t_temple.length] = Temple(idx, bahan[j][3],bahan[j][0],bahan[j][1],bahan[j][2])
                    j += 1
                    state.t_temple.length += 1
            for k in range(3):
                if(state.t_material.materials[k].name == "pasir"):
                    state.t_material.materials[k].quantity -= TotPasir
                elif(state.t_material.materials[k].name == "batu"):
                    state.t_material.materials[k].quantity -= TotBatu
                elif(state.t_material.materials[k].name == "air"):
                    state.t_material.materials[k].quantity -= TotAir
            return 0
        else:
            print("Mengerahkan ", jumlah_pembangun, " jin untuk membangun candi dengan total bahan ", TotPasir, " pasir, " , TotBatu, " batu, dan ",TotAir, " air." )  
            kurang_pasir = TotPasir - state.t_material.materials[0].quantity if(TotPasir > state.t_material.materials[0].quantity) else 0
            kurang_batu =  TotBatu - state.t_material.materials[1].quantity if(TotBatu > state.t_material.materials[1].quantity) else 0
            kurang_air = TotAir - state.t_material.materials[2].quantity if(TotAir > state.t_material.materials[2].quantity) else 0
            print("Bangun gagal. Kurang ",kurang_pasir, " pasir, " , kurang_batu, " batu, dan " , kurang_air ," air.")
            return 1
    else:
        print("Cuman Bondowoso yang bisa melakukan batchbangun.")
        return 1  

def cekBahan(state : State) -> int:
    print(state.t_material.materials[0].quantity)
    print(state.t_material.materials[1].quantity)
    print(state.t_material.materials[2].quantity)
    return 0
    
def cekCandi(state : State) -> int:
    print(state.t_temple.temples[0].id , " " ,state.t_temple.temples[0].creator )
    print(state.t_temple.temples[1].id, " " ,state.t_temple.temples[1].creator)
    print(state.t_temple.temples[2].id, " " ,state.t_temple.temples[2].creator)
    print(state.t_temple.temples[3].id, " " ,state.t_temple.temples[3].creator)
    print(state.t_temple.temples[4].id, " " ,state.t_temple.temples[4].creator)
    return 0

def cekUser (state : State) -> int:
    for i in range(state.t_user.length):
        print(state.t_user.users[i].username," " ,state.t_user.users[i].role)
    return 0

def help(state: State):
    pengguna = state.c_user.username
    rolePengguna = state.c_user.role

    if pengguna == ANON.username: #login, load, exit
        print("=========== HELP ===========")
        print("1. login")
        print("   Untuk masuk menggunakan akun")
        print("2. load")
        print("   Untuk memakai data/file eksternal ke dalam game")
        print("3. exit")
        print("   Untuk keluar dari game")
        

    elif pengguna == "Roro":
        print("=========== HELP ===========")
        print("1. hancurkancandi")
        print("   Untuk menghancurkan candi yang dibuat dengan kerja keras jin")
        print("2. ayamberkokok")
        print("   Untuk memalsukan pagi hari dan menyelesaikan game")
        print("3. save")
        print("   Untuk menyimpan data yang berubah sejak memainkan game")
        print("4. logout")
        print("   Untuk keluar dari akun pengguna")
        print("5. exit")
        print("   Untuk keluar dari game")

    elif pengguna == "Bondowoso":
        print("=========== HELP ===========")
        print("1. summonjin")
        print("   Untuk memanggil jin untuk membantu dalam pembangunan candi atau pengumpulan material")
        print("2. hapusjin")
        print("   Untuk menghapus jin yang tidak diperlukan")
        print("3. ubahjin")
        print("   Untuk mengubah karakteristik jin")
        print("4. batchkumpul")
        print("   Untuk mengumpulkan bahan bangunan secara massal")
        print("5. batchbangun")
        print("   Untuk membangun candi secara massal")
        print("6. laporanjin")
        print("   Untuk melihat laporan tentang karakteristik jin")
        print("7. laporancandi")
        print("   Untuk melihat laporan tentang candi yang dibangun")
        print("8. save")
        print("   Untuk menyimpan data yang berubah sejak memainkan game")
        print("9. undo")
        print("   Untuk membatalkan aksi terakhir")
        print("10. logout")
        print("   Untuk keluar dari akun pengguna")
        print("11. exit")
        print("   Untuk keluar dari game")

    else:
        if rolePengguna == "Pembangun":
            print("=========== HELP ===========")
            print("1. bangun")
            print("   Untuk membangun candi")
            print("2. logout")
            print("   Untuk keluar dari akun pengguna")
            print("3. exit")
            print("   Untuk keluar dari game")


        else: #rolePengguna == "Pengumpul"
            print("=========== HELP ===========")
            print("1. kumpul")
            print("   Untuk mengumpulkan material untuk membuat candi")
            print("2. logout")
            print("   Untuk keluar dari akun pengguna")
            print("3. exit")
            print("   Untuk keluar dari game")


def summonjin(state: State) -> int:
    if state.c_user.username != "Bondowoso":
        print("Hanya Bondowoso yang bisa melakukan summon jin.")
        return 1
    elif state.t_user.length >= MAX_USER:
        print("Jumlah Jin telah maksimal! (100 jin). Bandung tidak dapat men-summon lebih dari itu")
        return 1
    else:
        indekskosong = 0
        i = 0
        while state.t_user.users[i].username != USER_MARK.username:
            i += 1
            if state.t_user.users[i].username == USER_MARK.username:
                indekskosong = i
                break

        print("Jenis jin yang dapat dipanggil:")
        print("   (1) Pengumpul - Bertugas mengumpulkan bahan bangunan")
        print("   (2) Pembangun - Bertugas membangun candi")
        print()

        while True:
            jenisjin = input("Masukkan nomor jenis jin yang ingin dipanggil: ")
            print()

            if jenisjin == "1":
                tipejin = "Pengumpul"
                print(f'Memilih jin "Pengumpul".')
                print()
                break

            elif jenisjin == "2":
                tipejin = "Pembangun"
                print(f'Memilih jin "Pembangun".')
                print()
                break

            else:  #salah input
                print(f'Tidak ada jenis jin bernomor "{jenisjin}"! ')
                print()
            
        loop1 = True
        while loop1:
            usernamejin = input("Masukkan username jin: ")

            loop2 = False
            sudahdiambil = False

            for f in range(MAX_USER):
                if state.t_user.users[f].username == usernamejin:
                    sudahdiambil = True
                    break

            if sudahdiambil == False:
                loop1 = False
            else:
                print(f'Username "{usernamejin}" sudah diambil!')

        passwordjin = ''
        while len(passwordjin) < 5 or len(passwordjin) > 25:
            passwordjin = input("Masukkan password jin: ")
            print()

            if len(passwordjin) < 5 or len(passwordjin) > 25:
                print("Password panjangnya harus 5-25 karakter!")

        state.t_user.users[indekskosong] = User(usernamejin, passwordjin, tipejin)
        state.t_user.length += 1
        
        print("Mengumpulkan sesajen...")
        print("Menyerahkan sesajen...")
        print("Membacakan mantra...")
        print()
        print(f'jin "{state.t_user.users[indekskosong].username}" berhasil dipanggil!')
        return 0
        
def hapusjin(state: State) -> int:
    if state.c_user.username == "Bondowoso":
        
        usernamejin = input("Masukkan username jin: ")

        if usernamejin == "Bondowoso" or usernamejin == "Roro":
            print("Hanya jin yang bisa dihapus.")
            return 1

        adaUser = False
        for indeksjin in range(state.t_user.length):
            if (state.t_user.users[indeksjin].username != USER_MARK.username 
            and state.t_user.users[indeksjin].username  == usernamejin):
                # user ditemukan
                adaUser = True
                break

        if adaUser == False:
            print("tidak ada jin dengan username tersebut")
            return 1
            
        choice = input(f"Apakah Anda yakin ingin menghapus jin dengan username {usernamejin} (Y/N)? ")
        
        if choice == "y" or choice =="Y":
            
            #hilangkan jin
            state.t_user.users[indeksjin] = USER_MARK
            state.t_user.length -= 1
            
            #menghilangkan candi
            indekscandi = 0
            jumlahcandihilang = 0
            
            while indekscandi < MAX_TEMPLE:
                if state.t_temple.temples[indekscandi].creator == usernamejin:
                    state.t_temple.temples[indekscandi] = TEMPLE_MARK
                    state.t_temple.length -= 1
                indekscandi += 1
            print("Jin telah berhasil dihapus dari alam gaib.")
            return 0
        
        elif choice == "n" or choice =="N":
            return 1
        
        else:
            print("Input salah, silahkan ulangi lagi.")
            return 1
    else:
        print("Hanya Bondowoso yang bisa mengakses hapusjin")
        return 1

def ubahjin(state: State) -> int:
    if state.c_user.username == "Bondowoso":
        usernamejin = input("Masukkan username jin: ")
        
        if usernamejin == "Bondowoso" or usernamejin == "Roro":
            print("Hanya jin yang bisa diubah.")
            return 1

        adaUser = False
        for indeksjin in range(state.t_user.length):
            if (state.t_user.users[indeksjin].username != USER_MARK.username 
            and state.t_user.users[indeksjin].username  == usernamejin):
                # user ditemukan
                adaUser = True
                break

        if adaUser == False:
            print("tidak ada jin dengan username tersebut")
            return 1

        tipejin = state.t_user.users[indeksjin].role

        if tipejin == "Pembangun":
            tipejinbaru = "Pengumpul"
        elif tipejin == "Pengumpul":
            tipejinbaru = "Pembangun"
        else:
            print("User tersebut bukan jin.")
            return 1

        choice = input(f'Jin ini bertipe "{tipejin}". Yakin ingin mengubah ke tipe "{tipejinbaru}"(Y/N)? ')

        if choice == "y" or choice == "Y":
            state.t_user.users[indeksjin].role = tipejinbaru
            print("Jin telah berhasil diubah.")
            return 0
        elif choice == "n" or choice == "N":
            return 1
        else:
            print("Input salah, silahkan ulangi lagi.")
            return 1
    
    else:
        print("Hanya Bondowoso yang bisa mengakses ubahjin.")
        return 1

def hancurkancandi(state : State) :
    if state.c_user.username != "Roro" :
        print("Hanya Roro Jonggrang yang dapat menghancurkan candi")
        return

    idCandi = int(input("Masukkan ID candi: "))
    confirm = input(f"Apakah anda yakin ingin menghancurkan candi ID: {idCandi} (Y/N)?")
    
    if confirm == "y" or confirm == "Y" :
        for i in range(MAX_TEMPLE) :
            if state.t_temple.temples[i].id == idCandi :
                state.t_temple.temples[i] = TEMPLE_MARK
                print("Candi telah berhasil dihancurkan")
                return 1
        print("Tidak ada candi dengan ID tersebut")
        return 0

def ayamberkokok(state : State) :
    if state.c_user.username != "Roro" :
        print("Hanya Roro Jonggrang yang dapat mengakhirkan permainan!")
        return 0
    
    jumlah_candi = state.t_temple.length

    print("Kukuruyuk.. Kukuruyuk..")
    print(f"Jumlah Candi : {jumlah_candi}")

    if jumlah_candi < 100 :
        print("Selamat, Roro Jonggrang memenangkan permainan!")
        print("*Bandung Bondowoso angry noise*")
        print("Roro Jonggrang dikutuk menjadi candi.")
        
    elif jumlah_candi >= 100 :
        print("Yah, Bandung Bondowoso memenangkan permainan!")
    
    quit()

def laporanjin(state:State):
    if(state.c_user.username == "Bondowoso"):
        print("Total Jin: " , state.t_user.length-2)
        jumlah_pembangun = 0
        jumlah_pengumpul = 0
        for i in range(state.t_user.length):
            if(state.t_user.users[i].role == "Pembangun"):
                jumlah_pembangun += 1
            elif(state.t_user.users[i].role == "Pengumpul"):
                jumlah_pengumpul += 1
        print("Total Jin Pengumpul: " , jumlah_pengumpul)
        print("Total Jin Pembangun: " , jumlah_pembangun)

        if(jumlah_pembangun == 0 ) or (state.t_temple.length == 0):
            jin_terajin = "-"
            jin_termalas = "-"
        else:
            jin_terajin = ""
            jin_termalas = ""
            candi_bangun_terbesar = 0
            candi_bangun_terkecil = 100
            temp_candi = 0
            for i in range(2,state.t_user.length):
                temp_candi = 0
                for j in range(state.t_temple.length):
                    if(state.t_temple.temples[j].creator == state.t_user.users[i].username):
                        temp_candi += 1
                
                if(temp_candi > candi_bangun_terbesar):
                    candi_bangun_terbesar = temp_candi
                    jin_terajin = state.t_user.users[i].username
                elif(temp_candi == candi_bangun_terbesar):
                    if(jin_terajin > state.t_user.users[i].username):
                        jin_terajin = state.t_user.users[i].username
                
                if(temp_candi < candi_bangun_terkecil):
                    candi_bangun_terkecil = temp_candi
                    jin_termalas = state.t_user.users[i].username
                elif(temp_candi == candi_bangun_terkecil):
                    if(jin_termalas < state.t_user.users[i].username):
                        jin_termalas = state.t_user.users[i].username
        
        print("Jin Terajin: " , jin_terajin)
        print("Jin Termalas: " , jin_termalas)
        print("Jumlah Pasir: " , state.t_material.materials[0].quantity)
        print("Jumlah Air: " , state.t_material.materials[2].quantity)
        print("Jumlah Batu: " , state.t_material.materials[1].quantity)
    else:
        print("Laporan jin hanya dapat diakses oleh akun Bandung Bondowoso.")


def laporancandi(state : State):
    if(state.c_user.username == "Bondowoso"):
        print("Total Candi: ", state.t_temple.length)
        if(state.t_temple.length == 0):
            id_termahal = "-"
            id_termurah = "-"
            harga_termahal = 0
            harga_termurah = 0
            print("Total Pasir yang digunakan: 0")
            print("Total Batu yang digunakan: 0")
            print("Total Air yang digunakan: 0")
            print("ID Candi Termahal: -")
            print("ID Candi Termurah: -")
        else:    
            Total_Pasir = 0
            Total_Batu = 0
            Total_Air = 0
            harga_termurah = 162500
            harga_termahal = 0
            id_termahal = "-"
            id_termurah = "-"
            for i in range(state.t_temple.length):
                temp_harga = 0
                Total_Pasir += state.t_temple.temples[i].sand
                Total_Batu += state.t_temple.temples[i].rock
                Total_Air += state.t_temple.temples[i].water
                temp_harga = (state.t_temple.temples[i].sand*10000) + (15000 * state.t_temple.temples[i].rock) + (7500 * state.t_temple.temples[i].water)

                if(temp_harga > harga_termahal):
                    harga_termahal = temp_harga
                    id_termahal = state.t_temple.temples[i].id
                if(temp_harga < harga_termurah):
                    harga_termurah = temp_harga
                    id_termurah = state.t_temple.temples[i].id

            print("Total Pasir yang digunakan: ", Total_Pasir)
            print("Total Batu yang digunakan: ", Total_Batu)
            print("Total Air yang digunakan: ", Total_Air)
            print("ID Candi Termahal: ",id_termahal," (Rp " ,harga_termahal,") ")
            print("ID Candi Termurah: ", id_termurah, " (Rp ",harga_termurah,") ")
    else:
        print("Laporan candi hanya dapat diakses oleh akun Bandung Bondowoso.")