from logik import knotenliste as kl
from anytree.exporter import DictExporter
import tree_dictionary_import_export as tie
import pickle
class Baum:

    def __init__(self,name):
        self.name=name
        self.knotenliste_mit_baum=kl.knotenliste_gesamt_erstellen()
        #print(self.knotenliste_mit_baum)
        exporter=DictExporter()
        self.dict_baum=exporter.export(self.knotenliste_mit_baum[0][0])
        tie.treedictionary_in_pickle_exportieren(self,filename=name)


