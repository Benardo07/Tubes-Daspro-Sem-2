import data
from commands import run
from base import *

def main():
    # dibuat menjadi prosedur biar laporan praktis
    # loading data tabel
    (t_user, t_temple, t_material) = data.load()

    # anggap username " " jika belum login
    # state program untuk di-pass ke command yang dijalankan
    state = State(t_user, t_temple, t_material, ANON) 

    history = History([], 0)

    # main loop
    while True:
        command = input(">>> ")
        if command == "undo":
            if history.length != 0:
                state = history.stack[0]
                history = History([history.stack[i]
                                for i in range(1, history.length)],
                                history.length - 1)
            # abaikan jika history kosong
        else:
            old_state = data.copy(state)
            status = run(command, state)
            
            if (status == 0 and old_state.c_user.role == "bandung_bondowoso"):
                if command == "logout":
                    # bersihkan kelakuan bandung
                    history = History([], 0)
                else:
                    # command berhasil dijalankan
                    # state berubah dan snapshot disimpan
                    history = data.snap(old_state, history)

main()