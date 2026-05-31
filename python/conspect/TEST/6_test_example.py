import pytest

# Расширенный словарь с поддержкой 'yes' и других вариантов
valid = {
    "true": True, "t": True, "1": True, "yes": True,
    "false": False, "f": False, "0": False
}

def string_to_bool(value):
    """Преобразует строку в булево значение, возвращает None для недопустимых."""
    return valid.get(value.lower(), None)

true_values = ['yes', '1', 'Yes', 'TRUE', 'TruE', 'True', 'true']

class TestStrToBool_:
    @pytest.mark.parametrize("value", true_values)
    def test_it_detects_truish_strings(self, value):
        assert string_to_bool(value) is True  # Явная проверка на True