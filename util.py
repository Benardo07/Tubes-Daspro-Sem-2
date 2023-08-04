# berisi fungsi2 utility untuk pemrosesan data secara general

# LCG versi stream -> ribet di notal
# def lcg(seed: int, a: int, c: int, mod: int):
#     next_num = (a * seed + c) % mod
#     return (next_num, lambda : lcg(next_num, a, c, mod))

def cycle_length(seed: int, a: int, c: int, mod: int) -> int:
    # menghitung panjang siklus LCG
    seed0 = seed
    length = 0
    while True:
        length += 1
        seed = (a * seed + c) % mod
        if seed == seed0:
            break
    return length

def get_cycle(seed: int, a: int, c: int, mod: int, length: int) -> list[int]:
    # menyimpan siklus LCG dalam array
    cycle = [0 for i in range(length)]     
    for i in range(length):
        cycle[i] = seed
        seed = (a * seed + c) % mod
    return cycle
    
def count_sep(s: str, sep: str) -> int:
    # menghitung banyak string yang dipisahkan oleh separator
    # ASUMSI string input hanya berbentuk satu baris
    
    s += "\n"
    i = 0
    count = 1
    while s[i] != "\n":
        if s[i] == sep: count += 1
        i += 1
    return count

def split(s: str, sep: str) -> list[str]:
    # memisahkan s menjadi n bagian
    # s adalah string yang akan dipecah
    # sep adalah separator atau karakter pemisah
    # ASUMSI string input hanya berbentuk satu baris
    item_count = count_sep(s, sep)

    s += "\n"
    i = 0
    j = 0
    res = ["" for i in range(item_count)]
    while s[j] != "\n":
        if s[j] == sep:
            i += 1
        else:
            res[i] += s[j]
        j += 1
    return res

def merge_n(los: list[str], n: int, sep: str) -> str:
    # menggabungkan suatu list of string menjadi
    # satu string dipisahkan dengan separator
    res = los[0]
    for i in range(1, n):
        res = res + sep + los[i]
    return res

def hitungJumlah (data : list,index : int,n : int) -> int:
    jumlah = 0
    for i in range(n):
        jumlah += data[i][index]
    return jumlah