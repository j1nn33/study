import pytest 
def idfn(v):
    if isinstance(v, int):
        return f"vid={v}"
    if isinstance(v, dict):
        return f'{v["name"]}:{v["role"]}'
    return repr(v)

@pytest.mark.parametrize("val", [
    1,
    4094,
    {"name": "alice", "role": "admin"},
], ids=idfn)

def test_example_case(val):
    assert val is not None