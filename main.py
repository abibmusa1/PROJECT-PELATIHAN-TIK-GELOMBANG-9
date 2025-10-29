import json
import os
import time
from datetime import datetime

# Nama file database tugas
DATA_FILE = "tugas.json"
USER_FILE = "user.json"

# ===============================
# Bagian Identitas Pengguna
# ===============================

def load_user():
    """Memuat data identitas pengguna dari file"""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return None
    return None

def save_user(user):
    """Menyimpan data identitas pengguna"""
    with open(USER_FILE, "w") as f:
        json.dump(user, f, indent=4)

def input_user():
    """Meminta input identitas pengguna di awal"""
    print("=== Masukkan Identitas Anda ===")
    nama = input("Nama: ")
    sekolah = input("Nama Sekolah: ")
    kelas = input("Kelas: ")
    user = {"nama": nama, "sekolah": sekolah, "kelas": kelas}
    save_user(user)
    print(f"\nSelamat datang, {nama} dari {sekolah} (Kelas {kelas})!\n")
    return user

# ===============================
# Bagian Data Tugas
# ===============================

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = f.read().strip()
                if not data:  # kalau file kosong
                    return []
                return json.loads(data)
            except json.JSONDecodeError:
                return []  # kalau isinya rusak
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task():
    nama = input("Masukkan nama tugas: ")

    while True:
        deadline_str = input("Masukkan tanggal deadline (contoh: 2025-10-29 17:50) : ")
        try:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            except ValueError:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d-%H:%M")
            break
        except ValueError:
            print("Format tanggal tidak valid! Gunakan format (contoh: 2025-10-29 17:50). ")

    tugas = {
        "nama": nama,
        "deadline": deadline.strftime("%Y-%m-%d %H:%M"),
        "selesai": False
    }
    tasks = load_tasks()
    tasks.append(tugas)
    save_tasks(tasks)
    print("Tugas berhasil ditambahkan!")

def show_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Belum ada tugas.")
        return

    print("\n📚 Daftar Tugas:")
    for i, t in enumerate(tasks, 1):
        status = "✅ Selesai" if t["selesai"] else "⏰ Belum"
        print(f"{i}. {t['nama']} - Deadline: {t['deadline']} - {status}")

def mark_done():
    show_tasks()
    tasks = load_tasks()
    if not tasks:
        return

    try:
        no = int(input("\nMasukkan nomor tugas yang sudah selesai: "))
        tasks[no - 1]["selesai"] = True
        save_tasks(tasks)
        print("🎉 Tugas ditandai selesai!")
    except (ValueError, IndexError):
        print("Nomor tidak valid!")

def reminder():
    tasks = load_tasks()
    now = datetime.now()
    for t in tasks:
        deadline = datetime.strptime(t["deadline"], "%Y-%m-%d %H:%M")
        if not t["selesai"] and 0 <= (deadline - now).total_seconds() <= 3600:
            print(f"⚠️  Pengingat: Tugas '{t['nama']}' akan jatuh tempo jam {deadline.strftime('%H:%M')}!")

# ===============================
# Menu Utama
# ===============================

def main():
    user = load_user()
    if not user:
        user = input_user()
    else:
        print(f"Selamat datang kembali, {user['nama']} dari {user['sekolah']} (Kelas {user['kelas']})!\n")

    while True:
        print("\n=== Aplikasi Pengingat Tugas Sekolah ===")
        print("1. Tambah Tugas")
        print("2. Lihat Tugas")
        print("3. Tandai Tugas Selesai")
        print("4. Jalankan Pengingat (cek tiap 1 menit)")
        print("5. Ganti Identitas")
        print("6. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            add_task()
        elif pilih == "2":
            show_tasks()
        elif pilih == "3":
            mark_done()
        elif pilih == "4":
            print("🔔 Mode pengingat aktif. Tekan Ctrl+C untuk berhenti.")
            try:
                while True:
                    reminder()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nPengingat dihentikan.")
        elif pilih == "5":
            input_user()
        elif pilih == "6":
            print("Sampaikan Jika Ada Tugas Lagi! 👋")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
