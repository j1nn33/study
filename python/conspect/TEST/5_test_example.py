import pytest
# 1-st vatiant test case 


class TestStringToBool(object):
    def test_it_detects_lowercase_yes(self):
        assert string_to_bool('yes')
    def test_it_detects_odd_case_yes(self):
        assert string_to_bool('YeS')
    def test_it_detects_uppercase_yes(self):
        assert string_to_bool('YES')
    def test_it_detects_positive_str_integers(self):
        assert string_to_bool('1')
    def test_it_detects_true(self):
        assert string_to_bool('true')
    def test_it_detects_true_with_trailing_spaces(self):
        assert string_to_bool('true ')
    def test_it_detects_true_with_leading_spaces(self):
        assert string_to_bool(' true')

# testing funcktion
valid = {"true": True, "t": True, "1": True, "false": False, "f": False, "0": False}
def string_to_bool(value):
    return valid.get(value, None)  # возвращает None для недопустимых значений

# 2 variant test case
true_values = ['yes', '1', 'Yes', 'TRUE', 'TruE', 'True', 'true']
class TestStrToBool_second(object):
    @pytest.mark.parametrize("value", true_values)
    def test_it_detects_truish_strings(self, value):
        assert string_to_bool(value) is True  # Явная проверка на True




