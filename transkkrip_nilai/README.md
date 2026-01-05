# Transkrip Nilai Akademik

Sistem untuk menghitung IPK dan menghasilkan transkrip akademik dalam format PDF.

## 🚀 Quick Start

1. **Clone atau download project ini**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan demo**:
   ```bash
   python demo.py
   ```
4. **Jalankan unit tests**:
   ```bash
   python -m unittest tests.py
   ```

## 📋 Fitur

- **Perhitungan IPK**: Mengikuti aturan IPK = Σ(SKS × Nilai Angka) / Σ(SKS)
- **Penanganan MK Diulang**: Mengambil nilai tertinggi untuk mata kuliah yang diulang
- **Filter Nilai Lulus**: Hanya menghitung MK dengan nilai ≥ D
- **Handle Edge Case**: Mahasiswa semester 1 tanpa nilai mengembalikan 0.0
- **Unit Test**: Test untuk berbagai skenario
- **PDF Generation**: Menggunakan WeasyPrint untuk menghasilkan PDF profesional
- **Database Auditing**: Track perubahan nilai dengan trigger dan view

## 🛠️ Instalasi Lengkap

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database (PostgreSQL) - Opsional
Jika ingin menggunakan fitur database auditing:
```bash
# Buat database baru
createdb transkrip_nilai

# Setup schema
psql -U username -d transkrip_nilai < sql/schema.sql
psql -U username -d transkrip_nilai < sql/trigger.sql
psql -U username -d transkrip_nilai < sql/view.sql
```

## Penggunaan

### Perhitungan IPK

```python
from main import calculate_ipk

grades = [
    {'kode': 'TI101', 'nama': 'Algoritma', 'sks': 3, 'nilai': 'A'},
    {'kode': 'TI102', 'nama': 'Matematika', 'sks': 3, 'nilai': 'B'}
]

ipk = calculate_ipk(grades)
print(f"IPK: {ipk}")
```

### Generate PDF Transkrip

```python
from main import generate_transcript_pdf

student_data = {
    'nim': '12345678',
    'nama': 'John Doe',
    'program_studi': 'Teknik Informatika',
    'angkatan': 2020,
    'semesters': [
        {
            'nomor': 1,
            'grades': [
                {'kode': 'TI101', 'nama': 'Algoritma', 'sks': 3, 'nilai': 'A'}
            ]
        }
    ]
}

generate_transcript_pdf(student_data, 'transcript.pdf')
```

### Menjalankan Unit Test

```bash
python -m unittest tests.py
```

### Demo

```bash
python demo.py
```

## Struktur Database

### Tabel `grades`
- `id`: Primary key
- `student_id`: NIM mahasiswa
- `course_code`: Kode mata kuliah
- `course_name`: Nama mata kuliah
- `sks`: SKS mata kuliah
- `grade`: Nilai (A, B, C, D, E)
- `semester`: Semester
- `academic_year`: Tahun akademik

### Tabel `grade_history`
- `id`: Primary key
- `grade_id`: Foreign key ke grades
- `old_value`: Nilai lama
- `new_value`: Nilai baru
- `changed_by`: Siapa yang mengubah
- `changed_at`: Waktu perubahan
- `reason`: Alasan perubahan

### View `student_grade_history`
Menampilkan riwayat perubahan nilai per mahasiswa.

## Aturan Perhitungan IPK

1. Nilai ke angka: A=4, B=3, C=2, D=1, E=0
2. Hanya hitung MK dengan nilai ≥ D (lulus)
3. Untuk MK diulang, ambil nilai tertinggi
4. IPK = Σ(SKS × Nilai Angka) / Σ(SKS)
5. Jika tidak ada nilai lulus, return 0.0

## Predikat

- ≥ 3.5: Cum Laude
- ≥ 3.0: Sangat Memuaskan
- ≥ 2.5: Memuaskan
- ≥ 2.0: Cukup
- < 2.0: Kurang
