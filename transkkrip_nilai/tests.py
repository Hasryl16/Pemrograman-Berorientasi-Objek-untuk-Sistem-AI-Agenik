import unittest
from main import calculate_ipk

class TestCalculateIPK(unittest.TestCase):

    def test_perfect_grades(self):
        """Test mahasiswa dengan nilai sempurna (semua A)"""
        grades = [
            {'kode': 'MK001', 'nama': 'Matematika', 'sks': 3, 'nilai': 'A'},
            {'kode': 'MK002', 'nama': 'Fisika', 'sks': 3, 'nilai': 'A'},
            {'kode': 'MK003', 'nama': 'Kimia', 'sks': 2, 'nilai': 'A'}
        ]
        self.assertEqual(calculate_ipk(grades), 4.0)

    def test_repeated_course(self):
        """Test mahasiswa dengan MK diulang"""
        grades = [
            {'kode': 'MK001', 'nama': 'Matematika', 'sks': 3, 'nilai': 'C'},
            {'kode': 'MK001', 'nama': 'Matematika', 'sks': 3, 'nilai': 'A'},  # Repeat, take A
            {'kode': 'MK002', 'nama': 'Fisika', 'sks': 3, 'nilai': 'B'}
        ]
        # IPK = (3*4 + 3*3) / (3+3) = 21/6 = 3.5
        self.assertEqual(calculate_ipk(grades), 3.5)

    def test_no_grades(self):
        """Test mahasiswa semester awal (belum ada nilai)"""
        grades = []
        self.assertEqual(calculate_ipk(grades), 0.0)

    def test_failing_grades(self):
        """Test with only failing grades"""
        grades = [
            {'kode': 'MK001', 'nama': 'Matematika', 'sks': 3, 'nilai': 'E'},
            {'kode': 'MK002', 'nama': 'Fisika', 'sks': 3, 'nilai': 'E'}
        ]
        self.assertEqual(calculate_ipk(grades), 0.0)

    def test_mixed_grades(self):
        """Test with mixed passing and failing grades"""
        grades = [
            {'kode': 'MK001', 'nama': 'Matematika', 'sks': 3, 'nilai': 'A'},
            {'kode': 'MK002', 'nama': 'Fisika', 'sks': 3, 'nilai': 'E'},  # Failing, exclude
            {'kode': 'MK003', 'nama': 'Kimia', 'sks': 2, 'nilai': 'B'}
        ]
        # IPK = (3*4 + 2*3) / (3+2) = 18/5 = 3.6
        self.assertEqual(calculate_ipk(grades), 3.6)

if __name__ == '__main__':
    unittest.main()
