#!/usr/bin/env python3
"""
Demo script for the Transkrip Nilai Akademik system
"""

from main import calculate_ipk, get_predikat, generate_transcript_pdf

def main():
    print("=== Sistem Transkrip Nilai Akademik ===\n")

    # Sample data for demonstration
    sample_grades = [
        {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'A'},
        {'kode': 'TI102', 'nama': 'Matematika Diskrit', 'sks': 3, 'nilai': 'B'},
        {'kode': 'TI103', 'nama': 'Basis Data', 'sks': 3, 'nilai': 'A'},
        {'kode': 'TI104', 'nama': 'Jaringan Komputer', 'sks': 2, 'nilai': 'C'},
        {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'B'},  # Repeat course
    ]

    print("Sample grades:")
    for grade in sample_grades:
        print(f"  {grade['kode']} - {grade['nama']} ({grade['sks']} SKS): {grade['nilai']}")

    # Calculate IPK
    ipk = calculate_ipk(sample_grades)
    predikat = get_predikat(ipk)

    print(f"\nCalculated IPK: {ipk}")
    print(f"Predikat: {predikat}")

    # Sample student data for PDF generation
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
                    {'kode': 'TI101', 'nama': 'Algoritma dan Pemrograman', 'sks': 3, 'nilai': 'B'},  # Repeat
                ]
            }
        ]
    }

    print("\nStudent data for PDF generation:")
    print(f"  NIM: {student_data['nim']}")
    print(f"  Nama: {student_data['nama']}")
    print(f"  Program Studi: {student_data['program_studi']}")
    print(f"  Angkatan: {student_data['angkatan']}")

    # Try to generate PDF
    try:
        generate_transcript_pdf(student_data, 'sample_transcript.pdf')
    except Exception as e:
        print(f"\nPDF generation failed: {e}")
        print("Note: PDF generation requires WeasyPrint to be properly installed.")

    print("\n=== Demo completed successfully! ===")

if __name__ == '__main__':
    main()
