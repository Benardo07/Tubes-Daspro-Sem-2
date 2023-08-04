# import untuk typing fungsi atau mengunakan konstanta
# DEFINISI TIPE

# Berdasarkan PEP 484 self tidak diberikan type dan return type __init__ adalah None
class User:
    def __init__(self, username: str, password: str, role: str) -> None:
        self.username = username
        self.password = password
        self.role = role
        
class Temple:
    def __init__(self, id: int, creator: str, 
                 sand: int, rock: int, water: int) -> None:
        self.id = id
        self.creator = creator
        self.sand = sand
        self.rock = rock
        self.water = water
        
class Material:
    def __init__(self, name: str, description: str, quantity: int) -> None:
        self.name = name
        self.description = description
        self.quantity = quantity

# NOTE: perhitungan panjang tabel MENCAKUP MARK (elemen kosong)

# NOTE: untuk menambahkan elemen pada tabel,
#       lakukan while loop hingga bertemu MARK dan ambil indeksnya
#       isi indeks tersebut dengan elemen yang ditambahkan

# NOTE: jika penambahan elemen terjadi pada: 
#       index > length - 1, TAMBAHKAN length tabel
#       JANGAN ditambah jika: index < length - 1

class TabUser:
    def __init__(self, users: list[User], length: int) -> None:
        self.users = users
        self.length = length
        
class TabTemple:
    def __init__(self, temples: list[Temple], length: int) -> None:
        self.temples = temples
        self.length = length
        
class TabMaterial:
    def __init__(self, materials: list[Material], length: int) -> None:
        self.materials = materials
        self.length = length

class State:
    def __init__(self, t_user: TabUser, t_temple: TabTemple,
                 t_material: TabMaterial, c_user: User) -> None:
        self.t_user = t_user
        self.t_temple = t_temple
        self.t_material = t_material
        self.c_user = c_user # current user
        
class History:
    def __init__(self, stack: list[State], length: int) -> None:
        self.stack = stack
        self.length = length

class LCG:
    def __init__(self, cycle: list[int], length: int, index: int) -> None:
        self.cycle = cycle
        self.length = length
        self.index = index

# DEFINISI KONSTANTA
MAX_USER = 102 # 100 jin + roro + bondo
MAX_TEMPLE = 100 # lebih dari 100 tidak disimpan

# asumsi username tidak boleh memiliki whitespace sebelum karakter pertama
ANON = User(" ", " ", " ") # pengguna belum login
USER_MARK = User(" MARK", "ZUCKER", "BERG") # mark pengguna berupa seorang alien

TEMPLE_MARK = Temple(-1, "Malin Kundang", 0, 0, 0) # mark candi berupa sebuah gunung

DEFAULT_MATERIALS = [Material("pasir", "pasir pantai Nyi Roro Kidul", 0),
                     Material("batu", "batu dari Mars", 0),
                     Material("air", "Nyi Roro Kidul bath water (air Laut Selatan)", 0)]
MATERIALS_COUNT = 3 # untuk for loop

BASE_STATE = State(TabUser([USER_MARK for i in range(MAX_USER)], MAX_USER),
                   TabTemple([TEMPLE_MARK for i in range(MAX_TEMPLE)], MAX_TEMPLE),
                   TabMaterial(DEFAULT_MATERIALS, MATERIALS_COUNT),
                   ANON)

SAVE_DIR = "save/"