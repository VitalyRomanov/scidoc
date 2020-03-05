from Indexer import Indexer
from FeatureExtractor import FeatureExtractor
from Segmenter import Segmenter
from PendingIterator import PendingIterator
from PDFExtractor import PDFExtractor as PDF
from params import index_store
import sys

pending = PendingIterator(index_store)
segm = Segmenter()
# https: // docs.python.org / 3 / library / sqlite3.html

for p in pending:

    segments = segm(PDF.read(p))
    for s_id, s in segments:
        print(s_id, s)
