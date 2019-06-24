import pickle

def treedictionary_in_pickle_exportieren(treedictionary,filename):

    pickle_out=open(f"{filename}.pickle","wb")
    pickle.dump(treedictionary, pickle_out)
    pickle_out.close()


def treedictionary_aus_pickle_importieren(filename):
    pickle_in = open(f"{filename}.pickle","rb")
    treedictionary = pickle.load(pickle_in)
    return treedictionary