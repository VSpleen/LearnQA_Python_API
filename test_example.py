class TestExample:
    def  test_length(self):
        phrase = input("Set a phrase: ")
        wordLen = len(phrase)
        assert wordLen<15, f"Длинна слова = {wordLen}"
