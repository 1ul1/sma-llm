import re

class TextHandler:
    @staticmethod
    def post_process_text(string: str) -> str:
        if not string:
            return ""
        pattern = r"[^a-zA-Z0-9.,?!=+ -]"
        string = re.sub(pattern, "", string)
        string = re.sub(r" +", " ", string)
        string = re.sub(r"""([,.?!`"';:-])\1+""", r"\1", string)
        string = string.rstrip()
        return string
    
    @staticmethod
    def pre_process_text(string: str) -> str:
        if not string:
            return ""
        string = TextHandler.post_process_text(string)
        string = string.lower().lstrip()
        pattern = r"(?<=[.?!])"
        sentences = re.split(pattern, string)
        string = " ".join(sentence.strip().capitalize() for sentence in sentences)
        return string
    
    @staticmethod
    def test_process_text(string: str) -> str:
        print("Pre: " + TextHandler.pre_process_text(string)\
              + "\nPost: " + TextHandler.post_process_text(string))
    
    punctuation_characters = [".", ",", "!"]
    max_sentence_number = 5

    def __init__(self):
        self.sentence_counter = 0
        
    def stop(self, string: str):
        match string:
            case _ if not string:
                return True
            case _ if "?" in string:
                self.sentence_counter = 0
                return True
            case _ if any(character in string for character in TextHandler.punctuation_characters):
                self.sentence_counter += 1
                if self.sentence_counter == TextHandler.max_sentence_number:
                    self.sentence_counter = 0
                    return True
                return False
            case _:
                return False
            
    @staticmethod
    def set_max_sentence_number(var: int) -> None:
        TextHandler.max_sentence_number = var