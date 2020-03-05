from Segmenter import Segmenter
import json
import sys

# from gensim.corpora import Dictionary
from gensim.models.phrases import Phrases

seg = Segmenter()
# vocab = Dictionary()
phrases = Phrases()

text_path = sys.argv[1]

def get_data(text_path):

    for line in open(text_path, "r"):
        line = line.strip()

        if line:
            data = json.loads(line)

            yield data['abstract']

for ind, text in enumerate(get_data(text_path)):
    segments = seg(text, segment_len=1, segment_overlap=0)

    phrases.add_vocab(segments)
    # vocab.add_documents(segments, prune_at=2000000)

    if ind % 10000:
        print(f"\rProcessed:{ind}", end = "")
        break

# vocab.filter_extremes(no_below=5, no_above=0.5, keep_n=2000000)
# vocab.save("academic.dict")

phrases.save("academic.phrases")