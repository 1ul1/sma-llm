import re

class TextHandler:
    def __new__(cls):
        raise TypeError("")
    
    def __init__(self):
        pass

    @staticmethod
    def post_process_text(string):
        if not string:
            return ""
        pattern = r"[^a-zA-Z0-9.,?!=+ -]"
        string = re.sub(pattern, "", string)
        string = re.sub(r" +", " ", string)
        string = re.sub(r"""([,.?!`"';:-])\1+""", r"\1", string)
        string = string.rstrip()
        return string
    
    @staticmethod
    def pre_process_text(string):
        if not string:
            return ""
        string = TextHandler.post_process_text(string)
        string = string.lower().lstrip()
        pattern = r"(?<=[.?!])"
        sentences = re.split(pattern, string)
        string = " ".join(sentence.strip().capitalize() for sentence in sentences)
        return string
    
    @staticmethod
    def test_process_text(string):
        print("Pre: " + TextHandler.pre_process_text(string)\
              + "\nPost: " + TextHandler.post_process_text(string))
    
    sentence_counter = 0
    punctuation_characters = [".", ",", "!"]
    @staticmethod
    def stop(string):
        match string:
            case _ if not string:
                return True
            case _ if "?" in string:
                TextHandler.sentence_counter = 0
                return True
            case _ if any(character in string for character in TextHandler.punctuation_characters):
                TextHandler.sentence_counter += 1
                if TextHandler.sentence_counter == 4:
                    TextHandler.sentence_counter = 0
                    return True
                return False
            case _:
                return False