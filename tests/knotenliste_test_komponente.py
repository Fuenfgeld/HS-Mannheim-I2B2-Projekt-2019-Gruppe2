from logik import verarbeitungsschicht as bl
from logik import abfragen as ab
from unittest import TestCase
from logik import knotenliste as kl
import pandas as pd


def Hilfe_Knotenliste():
    con = bl.connection_zu_datenbank_aufbauen()
    knotenliste_gesamt = []
    df_ebene = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(4, con)
    knotenliste_gesamt.append(kl.knotenliste_für_eine_ebene_erstellen(df_ebene))
    return knotenliste_gesamt

def test_knotenliste():
    liste = Hilfe_Knotenliste()
    erwarteteliste = Hilfe_Knotenliste()
    assert type(liste) == list


class TestAus_knotenliste_baum_erstellen(TestCase):
    def test_aus_knotenliste_baum_erstellen(self):
        con = bl.connection_zu_datenbank_aufbauen()
        from logik.knotenliste import knotenliste_gesamt_erstellen, aus_knotenliste_baum_erstellen
        knoten = knotenliste_gesamt_erstellen()
        baum = aus_knotenliste_baum_erstellen(knoten, con)
        baum == knotenliste_gesamt_erstellen()

    def knotenlistegesamterstellen(self):
        from logik.knotenliste import knotenliste_für_eine_ebene_erstellen
        con = bl.connection_zu_datenbank_aufbauen()
        knotenliste_gesamt = []
        for i in range(0, 11, 1):
            df_ebene = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(i, con)
            knotenliste_gesamt.append(knotenliste_für_eine_ebene_erstellen(df_ebene))
        return knotenliste_gesamt

class TestKnotenliste_für_eine_ebene_erstellen(TestCase):
    def test_knotenliste_für_eine_ebene_erstellen(self):
        dict_ebene = {'name': ['Knoten1', 'Knoten2'], 'fullname': ['Fullname1', 'Fullname2'],
                      'Pfad': ['Pfad1', 'Pfad2'],
                      'Symbol': ['Symbol1', 'Symbol2'], 'Size': [0, 1]}
        df_ebene = pd.DataFrame(data=dict_ebene)
        from knoten import node_with_value
        knotenliste = [
            node_with_value(name='Knoten1', fullname='Fullname1', pfad='Pfad1', size=0),
            node_with_value(name='Knoten2', fullname='Fullname2', pfad='Pfad2', size=1)]
        from logik.knotenliste import knotenliste_für_eine_ebene_erstellen
        knotenliste_für_eine_ebene_erstellen(df_ebene) == knotenliste

class TestKnotenliste_gesamt_erstellen(TestCase):
    def test_knotenliste_gesamt_erstellen(self):
        from logik.knotenliste import knotenliste_gesamt_erstellen
        from logik.tree_dictionary_import_export import treedictionary_aus_pickle_importieren
        baum = treedictionary_aus_pickle_importieren('baum_mit_titten')
        baum_Methode = knotenliste_gesamt_erstellen()
        baum == baum_Methode
