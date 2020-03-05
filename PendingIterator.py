from os.path import isfile, join

class PendingIterator:
    def __init__(self, index_store):
        self.index_store = index_store

    def __iter__(self):
        pending_path = join(self.index_store, "pending.txt")

        if not isfile(pending_path):
            return iter([])

        with open(pending_path) as pfile:
            pending = pfile.read().strip().split("\n")

            return iter(pending)