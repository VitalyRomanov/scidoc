#%%
import sys 
import bz2
import os
import subprocess
from LanguageTools.nltk_wrapper import NltkWrapper
from nltk.classify.textcat import TextCat
import pickle

from gensim.corpora import Dictionary
from gensim.models.phrases import Phrases, Phraser

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#%%
pdf_paths = "/Users/LTV/Documents/all_pdfs.txt"

files = open(pdf_paths).read().strip().split("\n")

def get_files_content(files):

    for filename in files:
        print("Filename:", filename)
        print("File size: ", os.stat(filename).st_size / (1024 * 1024))
        cp = subprocess.run(["pdftotext", f"{filename}", "-"], stdout=subprocess.PIPE)

        yield (filename, cp.stdout.decode('utf8'))


tc = TextCat()
nlp_en = NltkWrapper("en")
nlp_ru = NltkWrapper("ru")

phrase_voc = Dictionary()
phrases_model = Phrases()

#%%

for loc, filecontent in get_files_content(files):

    full_text = " ".join(filecontent.split("\n"))
    lang_guess = tc.guess_language(full_text[:200])
    print("Language guess:", lang_guess)
    # print("Content:", full_text[:50])

    if lang_guess == "eng":
        nlp = nlp_en
    elif lang_guess == "rus":
        nlp = nlp_ru
    else:
        nlp = None

    # TODO:
    # 1. Create n-gram features for full text similarity search
    #   This will create a problem of two documents being similar 
    #   everything but the subject of research. We want documents 
    #   to be similar in subject of research
    # 2. Need to reliably determine the topic. Seems hard to solve 
    #   this in ad-hoc fashion. Need to train LDA on paper abstracts
    #   first.

    if nlp is not None:
        tokenized = nlp(full_text)

        phrases_model.add_vocab([token for token, pos in s] for s in tokenized)
        phrase_voc.add_documents(nlp.chunks(t) for t in tokenized)

    print("\n")

#%%

pickle.dump(phrases_model, open("gensim_phrase.pkl", "wb"))
pickle.dump(phrase_voc, open("gensim_chunk_dict.pkl", "wb"))

#%%

common_dict = Dictionary()

for loc, filecontent in get_files_content(files):

    full_text = " ".join(filecontent.split("\n"))
    lang_guess = tc.guess_language(full_text[:200])
    print("Language guess:", lang_guess)
    # print("Content:", full_text[:50])

    if lang_guess == "eng":
        nlp = nlp_en
    elif lang_guess == "rus":
        nlp = nlp_ru
    else:
        nlp = None

    if nlp is not None:
        tokenized = nlp(full_text)

        only_tokens = [[token for token, pos in s] for s in tokenized]
        gram_tokens = phrases_model[only_tokens]
        chunks = [nlp.chunks(t) for t in tokenized]

        joined = [gram + ch for gram, ch in zip(gram_tokens, chunks)]

        common_dict.add_documents(joined, prune_at=10000000)
            
#%%

pickle.dump(common_dict, open("gensim_common_dict.pkl", "wb"))

#%%

txt = """
One notable recent argument is to build a differentiable and data-dependent pooling layer with learnable operations or parameters, which has brought a substantial improvement in graph classification tasks. The DiffPool (Ying et al., 2018) proposed a differentiable pooling layer that learns a cluster assignment matrix over the nodes relating to the output of a GNN model. One difficulty of DiffPool is its vast stor- age complexity, which is due to the computation of the soft clustering. The TopKPooling (Cangea et al., 2018; Gao & Ji, 2019; Knyazev et al., 2019) proposed a pooling method that samples a subset of essential nodes by manipulating a trainable projection vector. The Self-Attention Graph Pool- ing (SAGPool) (Lee et al., 2019) proposed an analogous pooling that applied the GCN module to compute the node scores instead of the projection vector in the TopKPooling. These hierarchical pooling methods technically still em- ploy mean/max pooling procedures to aggregate the feature representation of super-nodes. To preserve more edge infor- mation of the graph, EdgePool (Diehl et al., 2019) proposed to incorporate edge contraction. The StructPool (Yuan & Ji, 2020) proposed a graph pooling that employed conditional random fields to represent the relation of different nodes.
"""



# %%
