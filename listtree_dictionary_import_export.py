import pickle

def treedictionary_in_pickle_exportieren(listGroundLevelDiv ):

    pickle_out=open("tree2.pickle","wb")
    pickle.dump(listGroundLevelDiv, pickle_out)
    pickle_out.close()


def treedictionary_aus_pickle_importieren():
    pickle_in =  open("tree2.pickle","rb")
    listGroundLevelDiv  = pickle.load(pickle_in)
    return listGroundLevelDiv