# 📖 Panduan Penggunaan Sistem Transkrip Nilai Akademik

## 🎯 Cara Menggunakan Sistem

### 1. **Persiapan Awal**

Pastikan Anda memiliki Python 3.7+ terinstall. Kemudian:

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan demo untuk melihat sistem bekerja
python demo.py

# Jalankan unit tests untuk memastikan semuanya berfungsi
python -m unittest tests.py
```

### 2. **Menggunakan Fungsi Perhitungan IPK**

```python
from main import calculate_ipk

# Contoh data nilai mahasiswa
grades = [
    {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'A'},
    {'kode': 'TI102', 'nama': 'Matematika Diskrit', 'sks': 3, 'nilai': 'B'},
    {'kode': 'TI103', 'nama': 'Basis Data', 'sks': 3, 'nilai': 'A'},
    {'kode': 'TI104', 'nama': 'Jaringan Komputer', 'sks': 2, 'nilai': 'C'},
    # Mata kuliah diulang - sistem akan ambil nilai tertinggi
    {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'B'},
]

# Hitung IPK
ipk = calculate_ipk(grades)
print(f"IPK Mahasiswa: {ipk}")  # Output: 3.36
```

### 3. **Menghasilkan PDF Transkrip**

```python
from main import generate_transcript_pdf

# Data mahasiswa lengkap
student_data = {
    'nim': '12345678',
    'nama': 'Ahmad Rahman',
    'program_studi': 'Teknik Informatika',
    'angkatan': 2020,
    'semesters': [
        {
            'nomor': 1,
            'grades': [
                {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'A'},
                {'kode': 'TI102', 'nama': 'Matematika Diskrit', 'sks': 3, 'nilai': 'B'},
            ]
        },
        {
            'nomor': 2,
            'grades': [
                {'kode': 'TI103', 'nama': 'Basis Data', 'sks': 3, 'nilai': 'A'},
                {'kode': 'TI104', 'nama': 'Jaringan Komputer', 'sks': 2, 'nilai': 'C'},
                {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'B'},  # Diulang
            ]
        }
    ]
}

# Generate PDF
generate_transcript_pdf(student_data, 'transkrip_ahmad.pdf')
print("PDF transkrip berhasil dibuat!")
```

### 4. **Menggunakan Sistem Database (Opsional)**

Jika Anda ingin menggunakan fitur audit perubahan nilai:

```bash
# Setup database PostgreSQL
createdb transkrip_nilai
psql -U your_username -d transkrip_nilai < sql/schema.sql
psql -U your_username -d transkrip_nilai < sql/trigger.sql
psql -U your_username -d transkrip_nilai < sql/view.sql
```

### 5. **Contoh Lengkap dalam Script**

Buat file `contoh_penggunaan.py`:

```python
#!/usr/bin/env python3
from main import calculate_ipk, get_predikat, generate_transcript_pdf

def main():
    # Data nilai mahasiswa
    grades = [
        {'kode': 'MK001', 'nama': 'Pemrograman Dasar', 'sks': 3, 'nilai': 'A'},
        {'kode': 'MK002', 'nama': 'Matematika', 'sks': 3, 'nilai': 'B'},
        {'kode': 'MK003', 'nama': 'Fisika', 'sks': 2, 'nilai': 'A'},
        {'kode': 'MK004', 'nama': 'Kimia', 'sks': 2, 'nilai': 'C'},
        {'kode': 'MK001', 'nama': 'Pemrograman Dasar', 'sks': 3, 'nilai': 'B'},  # Diulang
    ]

    # Hitung IPK
    ipk = calculate_ipk(grades)
    predikat = get_predikat(ipk)

    print("=== HASIL PERHITUNGAN IPK ===")
    print(f"IPK: {ipk}")
    print(f"Predikat: {predikat}")

    # Data untuk PDF
    student_data = {
        'nim': '20210001',
        'nama': 'Budi Santoso',
        'program_studi': 'Teknik Informatika',
        'angkatan': 2021,
        'semesters': [
            {
                'nomor': 1,
                'grades': grades  # Menggunakan data grades yang sama
            }
        ]
    }

    # Generate PDF
    try:
        generate_transcript_pdf(student_data, 'transkrip_budi.pdf')
        print("✅ PDF transkrip berhasil dibuat: transkrip_budi.pdf")
    except Exception as e:
        print(f"❌ Gagal membuat PDF: {e}")

if __name__ == '__main__':
    main()
```

Jalankan script:
```bash
python contoh_penggunaan.py
```

## 🔧 Troubleshooting

### PDF Tidak Bisa Dibuat
- Pastikan WeasyPrint terinstall dengan benar
- Pada Windows, mungkin perlu install GTK+ libraries
- Sistem akan memberikan pesan error yang jelas jika PDF gagal dibuat

### Import Error
- Pastikan semua dependencies terinstall: `pip install -r requirements.txt`
- Gunakan virtual environment untuk menghindari konflik package

### Database Connection Error
- Pastikan PostgreSQL running
- Periksa username dan password database
- Database setup bersifat opsional - sistem bisa berjalan tanpa database

## 📊 Memahami Output

### IPK Calculation
- **A=4, B=3, C=2, D=1, E=0**
- Hanya nilai ≥ D yang dihitung (lulus)
- Mata kuliah diulang: ambil nilai tertinggi
- Rumus: IPK = Σ(SKS × Nilai Angka) / Σ(SKS)

### Predikat
- ≥ 3.5: Cum Laude
- ≥ 3.0: Sangat Memuaskan
- ≥ 2.5: Memuaskan
- ≥ 2.0: Cukup
- < 2.0: Kurang

## 🎯 Tips Penggunaan

1. **Untuk Testing**: Gunakan `python demo.py` untuk melihat sistem bekerja
2. **Untuk Development**: Jalankan `python -m unittest tests.py` setelah setiap perubahan
3. **Untuk Production**: Pastikan semua dependencies terinstall dengan benar
4. **Database**: Setup database hanya jika butuh fitur audit perubahan nilai

## 📞 Bantuan

Jika mengalami masalah:
1. Periksa pesan error yang diberikan sistem
2. Pastikan semua dependencies terinstall
3. Jalankan unit tests untuk memastikan sistem berfungsi
4. Lihat file README.md untuk dokumentasi lengkap
