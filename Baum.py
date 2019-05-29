import Knotenliste as kl
from anytree.exporter import DictExporter
import tree_dictionary_import_export as tie
import pickle
class Baum:

    __instance = None

    @staticmethod
    def instance(self):
        if Baum.__instance == None:
            Baum()
        return Baum.__instance


    def __init__(self,name):
        """virtual private konstruktor"""
        if Baum.__instance != None:
            raise Exception
        else:
            self.name=name
            self.knotenliste_mit_baum=kl.knotenliste_gesamt_erstellen()
            #print(self.knotenliste_mit_baum)
            exporter=DictExporter()
            self.dict_baum=exporter.export(self.knotenliste_mit_baum[0][0])
            tie.treedictionary_in_pickle_exportieren(self,filename=name)




