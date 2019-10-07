import sys, os, pickle

FNAME = ".save"

def save(object):
    # Serialises and writes the object to a savefile.
    try:
        outfile = open(FNAME, "wb+")
    except pickle.PickleError:
        print("Unable to write save.")
        raise
    pickle.dump(object, outfile)
    outfile.close()

def load():
    # Gets savefile, deserialises it and returns the object.
    try:
        infile = open(FNAME, "rb")
        board = pickle.load(infile, encoding='bytes')
        infile.close()
        return board
    except FileNotFoundError:
        print("No save file yet.")
        return False
    except pickle.UnpicklingError:
        print("Unable to read save.")
        return False

def destroy():
    try:
        os.remove(FNAME)
    except FileNotFoundError:
        pass


