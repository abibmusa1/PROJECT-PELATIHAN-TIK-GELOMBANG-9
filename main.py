import json
from datetime import datetime, timedelta
import time
import os

# Nama file database tugas
DATA_FILE = "tugas.json"

# Fungsi untuk memuat data tugas dari file
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Fungsi untuk menyimpan data tugas ke file
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Fungsi untuk menambahkan tugas baru
def add_task():
    nama = input("Masukkan nama tugas: ")
    tanggal = input("Masukkan tenggat (format: YYYY-MM-DD HH:MM): ")

    try:
        deadline = datetime.strptime(tanggal, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Format tanggal tidak valid! Gunakan format YYYY-MM-DD HH:MM.")
        return

    tasks = load_tasks()
    tasks.append({"nama": nama, "deadline": tanggal, "selesai": False})
    save_tasks(tasks)
    print("✅ Tugas berhasil ditambahkan!")

# Fungsi untuk menampilkan semua tugas
def show_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Belum ada tugas.")
        return

    print("\n📚 Daftar Tugas:")
    for i, t in enumerate(tasks, 1):
        status = "✅ Selesai" if t["selesai"] else "⏰ Belum"
        print(f"{i}. {t['nama']} - Deadline: {t['deadline']} - {status}")

# Fungsi untuk menandai tugas selesai
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

# Fungsi untuk mengingatkan tugas mendekati deadline
def reminder():
    tasks = load_tasks()
    now = datetime.now()
    for t in tasks:
        deadline = datetime.strptime(t["deadline"], "%Y-%m-%d %H:%M")
        if not t["selesai"] and 0 <= (deadline - now).total_seconds() <= 3600:
            print(f"⚠️  Pengingat: Tugas '{t['nama']}' akan jatuh tempo jam {deadline.strftime('%H:%M')}!")

# Menu utama
def main():
    while True:
        print("\n=== Aplikasi Pengingat Tugas Sekolah ===")
        print("1. Tambah Tugas")
        print("2. Lihat Tugas")
        print("3. Tandai Tugas Selesai")
        print("4. Jalankan Pengingat (cek tiap 1 menit)")
        print("5. Keluar")

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
            print("Sampai jumpa! 👋")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
