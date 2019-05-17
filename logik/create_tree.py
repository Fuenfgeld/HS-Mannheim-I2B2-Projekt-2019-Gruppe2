from anytree import Node
from anytree.exporter import DictExporter
from logik import Verarbeitungsschicht as bl
import pandas as pd
import numpy as np

class node_with_value(Node):
    def __init__(self, name, size,parent=None, children=None,  **kwargs):
        Node.__init__(self, name,parent, children, **kwargs)
        self.size=size



def erstellen_dict_baumstruktur():
    connection = bl.connection_zu_datenbank_aufbauen()
    tabelle_aller_ordner=pd.read_sql_query("select c_fullname, c_path from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' order by c_hlevel limit 100", connection)
    print('erstelle baum')
    knotenliste = []
    for i in range(len(tabelle_aller_ordner)):
        knotenliste.append(node_with_value(tabelle_aller_ordner.iloc[i][0], size=np.random.randint(1,10),parent=None))
        for j in range(i):
            if tabelle_aller_ordner.iloc[i][1] == knotenliste[j].name:
                knotenliste[i].parent = knotenliste[j]
                break

    exporter = DictExporter()

    print(type(exporter.export(knotenliste[0])))
    dict_baum = exporter.export(knotenliste[0])
    return dict_baum

def erstellen_baumstruktur():
    connection = bl.connection_zu_datenbank_aufbauen()
    tabelle_aller_ordner=pd.read_sql_query("select c_fullname, c_path from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' order by c_hlevel limit 100", connection)
    print('erstelle baum')
    knotenliste = []
    for i in range(len(tabelle_aller_ordner)):
        knotenliste.append(node_with_value(tabelle_aller_ordner.iloc[i][0], size=np.random.randint(1,10),parent=None))
        for j in range(i):
            if tabelle_aller_ordner.iloc[i][1] == knotenliste[j].name:
                knotenliste[i].parent = knotenliste[j]


    return knotenliste
