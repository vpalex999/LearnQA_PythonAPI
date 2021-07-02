

def test_input_phrase():
    phrase = input("Set a phrase:")

    assert len(phrase) <= 15, "A phrase consist more than 15 characters."
