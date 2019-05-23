import pickle


def treedictionary_in_pickle_exportieren(treedictionary):

    pickle_out=open("tree1.pickle","wb")
    pickle.dump(treedictionary, pickle_out)
    pickle_out.close()


def treedictionary_aus_pickle_importieren():
    pickle_in =  open("tree1.pickle","rb")
    treedictionary = pickle.load(pickle_in)
    return treedictionary