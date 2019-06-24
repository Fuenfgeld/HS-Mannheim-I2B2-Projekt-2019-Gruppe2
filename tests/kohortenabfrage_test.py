from logik import kohortenabfrage as kab
from unittest import TestCase
from logik import verarbeitungsschicht as bl
from logik import tree_dictionary_import_export as tie
import pytest

baum = tie.treedictionary_aus_pickle_importieren('baum_mit_allem')
connection = bl.connection_zu_datenbank_aufbauen()


class TestKohortenAbfrage(TestCase):
    def testKohortenabfrageEinKritieren(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\Diagnoses\(A00-B99) Cert~ugmm"]],
                                                verknüpfungen=[]
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse)

    def testKohortenabfrageZweiKritierenAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\Diagnoses\(A00-B99) Cert~ugmm"],
                                                           ['', "\Diagnoses\(I00-I99) Dise~3w8h"]],
                                                verknüpfungen=['OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF

        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse)

    def testKohortenabfrageZweiKritierenAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\Diagnoses\(A00-B99) Cert~ugmm"],
                                                           ['', "\Diagnoses\(I00-I99) Dise~3w8h"]],
                                                verknüpfungen=['AND']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse)

    def testKohortenabfrageDreiKritierenOrOr(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['', "\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['', "\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['OR', 'OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKritierenOrAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['', "\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['', "\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['OR', 'AND']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKritierenAndAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['', "\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['', "\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['AND', 'AND']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKriterienAndOR(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['', "\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['', "\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['', "\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['AND', 'OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKritierenNOTOrOr(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['NOT', "\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['', "\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['', "\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['OR', 'OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKritierenNOTANDOr(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['NOT', "\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['', "\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['', "\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['AND', 'OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage, kab.Kohortenabfrage.kohortengröße, kab.Kohortenabfrage.df_alter,
                         kab.Kohortenabfrage.df_geschlecht, kab.Kohortenabfrage.df_sprache,
                         kab.Kohortenabfrage.df_rasse
                         )


class ReihenfolgeTesten(TestCase):
    def testReihenfolgeLeer(self):
        test = []
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], []), test)

    def testReihenfolgeORda(self):
        test = ['OR']
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen(['OR'], []), test)

    def testReihenfolgeANDda(self):
        test = ['AND']
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], ['AND']), test)

    def testReihenFOlGEANDundORda(self):
        test = ['AND', 'OR']
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen(['OR'], ['AND']), test)

    def testExceptionReihenFolgeLeerObwohlAND(self):
        with pytest.raises(Exception):
            test = []
            self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], ['AND']), test)

    def testExceptionReihenFolgeLeerObwohlANDOR(self):
        with pytest.raises(Exception):
            test = []
            self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen(['OR'], ['AND']), test)

    def testExceptionReihenFolgeBefülltObwohlleer(self):
        with pytest.raises(Exception):
            test = ['AND', 'OR']
            self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], []), test)

    def testFullNameUmwandelnAND(self):
        abfrage = "External causes of morbidity (v00-y99)  AND Certain conditions originating in the perinatal period (p00-p96)"

        test1 = (['\\Diagnoses\\(V00-Y99) Exte~2k58\\', '\\Diagnoses\\(P00-P96) Cert~6976\\'], ['AND'])
        self.assertNotEqual(kab.Kohortenabfrage.umwandeln_in_fullname(abfrage, baum), test1)

    def testFullNameUmwandelnOR(self):
        abfrage = "External causes of morbidity (v00-y99)  OR Certain conditions originating in the perinatal period (p00-p96)"
        test1 = (['\\Diagnoses\\(V00-Y99) Exte~2k58\\', '\\Diagnoses\\(P00-P96) Cert~6976\\'], ['OR'])
        self.assertNotEqual(kab.Kohortenabfrage.umwandeln_in_fullname(abfrage, baum), test1)

    def testFullNameUmwandeln(self):
        abfrage = "External causes of morbidity (v00-y99)"
        test1 = (['\\Diagnoses\\(V00-Y99) Exte~2k58\\'], [])
        self.assertNotEqual(kab.Kohortenabfrage.umwandeln_in_fullname(abfrage, baum), test1)
