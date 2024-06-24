from project import int_converter,check_link,write_to_file,fetch_comments
import pytest
def test_int_converter():
    assert int_converter("2.4K") == 2400
    assert int_converter("5.1K") == 5100
    assert int_converter("1.0K") == 1000
    assert int_converter("20.4K") == 20400
    assert int_converter("51") == 51
    assert int_converter("322") == 322

def test_check_link():
    assert check_link("cat") == False
    assert check_link("https://www.youtube.com/watch?v=ARHlPxVeTGg&ab_channel=Ahmet") == True
    assert check_link("dfasff") == False

def test_fetch_comments():
    assert fetch_comments("For test") == 0
    with pytest.raises(TypeError):
        assert fetch_comments("that just... why ?")
def test_write_to_file():
    with pytest.raises(TypeError):
        assert write_to_file("why i have to test this")
        assert write_to_file("that is not something that can testable like that")