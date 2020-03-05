import subprocess
from os.path import isdir, isfile, join
from os import mkdir

from params import index_store, index_locations


def load_file_list(index_store_path):
    file_list_path = join(index_store, "files.txt")
    if not isfile(file_list_path):
        # with open(file_list_path, "w") as flist:
        #     pass
        file_list = set()
    else:
        with open(file_list_path, "w") as flist:
            file_list = set(flist.read().strip().split("\n"))
    return file_list


if __name__ == "__main__":

    if not isdir(index_store):
        mkdir(index_store)

    file_list = load_file_list(index_store)

    for_indexing = []

    for location in index_locations:
        if isdir(location):
            cp = subprocess.run(["find", f"{location}", "-name", "*.pdf"], stdout=subprocess.PIPE)
            new_files = [path for path in cp.stdout.decode('utf8').strip().split("\n") if path not in file_list]

            for_indexing += new_files
        else:
            print(f"Skipping '{location}' - does not exist")

    with open(join(index_store, "pending.txt"), "w") as fi:
        [fi.write(f"{fl}\n") for fl in for_indexing]