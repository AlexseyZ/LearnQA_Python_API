a = input("Введите фразу длина которой короче 15 символов - ")
t = len(a)
class TestNw10:
    def test_check_len(self):
        assert len(a) < 15, f"Длина введённого значения - {t}, что > 15 символов"