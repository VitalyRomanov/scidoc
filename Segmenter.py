from LanguageTools.nltk_wrapper import NltkWrapper
from nltk.classify.textcat import TextCat

class Segmenter:
    def __init__(self):
        self.tc = TextCat()
        self.nlp_en = NltkWrapper("en")
        self.nlp_ru = NltkWrapper("ru")

    def __call__(self, full_text, segment_len=5, segment_overlap=2):

        full_text = " ".join(full_text.split("\n"))
        lang_guess = self.tc.guess_language(full_text[:200])

        if lang_guess == "eng":
            nlp = self.nlp_en
        elif lang_guess == "rus":
            nlp = self.nlp_ru
        else:
            nlp = None

        if nlp is None:
            return iter([])

        sentences = nlp(full_text, tagger=False)

        for ind in range(0, len(sentences) - segment_overlap, segment_len - segment_overlap):
            segment_id = f"{ind}/{len(sentences)}_{segment_len}"
            yield segment_id, sentences[ind:ind + segment_len]


