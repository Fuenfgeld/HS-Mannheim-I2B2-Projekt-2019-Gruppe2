from logik import knotenliste as kl
from logik import tree_dictionary_import_export as tie
from anytree.exporter import DictExporter, JsonExporter


class Baum:

    def __init__(self, name):
        self.name = name
        self.knotenliste_mit_baum = kl.knotenliste_gesamt_erstellen()
        self.wurzel = self.knotenliste_mit_baum[0][0]
        self.wurzel.shortcode = 'Diagnoses'
        self.wurzel.id = 'Diagnoses'
        exporter = DictExporter()
        self.dict_baum = exporter.export(self.knotenliste_mit_baum[0][0])
        tie.treedictionary_in_pickle_exportieren(self, filename=name)
