from unittest import TestCase
from logik import querystack as qs
from datenhaltung import connection as conn
import psycopg2 as psy
from logik import verarbeitungsschicht as bl
from logik import abfragen as ab
from logik import tree_dictionary_import_export as tie
s = qs.Querystack()
#QueryStack
class testQuery(TestCase):
    def test_stack_init(self):

        self.assertEqual(s.size(),9)

    def test_push1_size(self):
        item = 5
        print(s.push(item))
        self.assertEqual(s.push(item),None)

    def test_push2_size(self):
            s.push(5)
            s.push(6)
            self.assertEqual(s.size(), 9)

    def test_push2_pop1_size(self):
            s.push(5)
            s.push(6)
            s.pop()
            self.assertEqual(s.size(), 6)

    def test_push2_pop1_value(self):
            s.push(8)
            s.push(9)
            self.assertEqual(s.pop(), 9)

    def test_push2_pop2_size(self):
        s.push("Glob")
        s.push("Blob")
        s.pop()
        s.pop()
        self.assertEqual(s.size(), 7)

    def test_push2_pop2_value(self):
        s.push("Glob")
        s.push("Blob")
        s.pop()
        self.assertEqual(s.pop(), "Glob")

    def test_peek_push1(self):
        s.push(88)
        self.assertEqual(s.peek(),88)

    def test_peek_push3_pop1(self):
        s.push(7)
        s.push(889)
        s.push(3)
        s.pop()
        self.assertEqual(s.peek(),889)

    def test_pop_empty(self):
        self.assertEqual(s.pop(),None)

    def test_pop_empty(self):
       self.assertNotEqual(s.pop(),[])
    def test_peek_empty(self):
        self.assertNotEqual(s.peek(),None)
    def test_bottom(self):
        self.assertNotEquals(s.bottom(),None)
class TestQueryStackSingleton(TestCase):

    def testQueryStackerstInstanzDannKonstruktor(self):
        from logik import querystack
        import pytest
        with pytest.raises(Exception):
            qIK = querystack.getInstance()
            print(qIK)
            qIK2 = querystack.queryStack()
            self.assertEqual(qIK,qIK2)

    def testQueryStackerstKonstruktorDannKonstruktor(self):
        from logik import querystack
        import pytest
        with pytest.raises(Exception):
            q1K = querystack.queryStack()
            q2K = querystack.queryStack()
            self.assertEqual(q1K,q2K)
    def testQueryStackerstInstanzDannInstanz(self):
        from logik import querystack
        q1 = querystack.Querystack.getInstance()
        print(q1)
        q2 = querystack.Querystack.getInstance()
        print(q2)
        self.assertEqual(q1,q2)

con = bl.connection_zu_datenbank_aufbauen()
#Verarbeitungsschicht
class TestConnection_zu_datenbank_aufbauen(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection
        self.assertEqual(connection_zu_datenbank_aufbauen(), connection)


class TestAbfrage_grundgesamtheit(TestCase):
    def test_abfrage_grundgesamtheit(self):
        from logik.verarbeitungsschicht import abfrage_grundgesamtheit
        from logik.verarbeitungsschicht import connection_zu_datenbank_aufbauen
        pd.testing.assert_frame_equal(abfrage_grundgesamtheit(db_connection=connection_zu_datenbank_aufbauen()),
                                      pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension',
                                                        con=psy.connect(database="i2b2", user="i2b2",
                                                                        password="demouser", host="129.206.7.75",
                                                                        port="5432")))


class TestAbfrage_durchführen(TestCase):
    def test_abfrage_durchführen(self):
        from logik.verarbeitungsschicht import abfrage_durchführen
        df=pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension', con=con)
        abfrage='SELECT * from i2b2demodata.patient_dimension'
        df_2= abfrage_durchführen(abfrage,con)
        df.equals(df_2)



class TestUmwandeln_zu_sql_statement(TestCase):
    def test_umwandeln_zu_sql_statement(self):
        elementliste=['a','b','c']
        sql_statement='SELECT * FROM i2b2demodata.patient_dimension WHERE a b c'
        sql_statement

        from logik.verarbeitungsschicht import umwandeln_zu_sql_statement
        umwandeln_zu_sql_statement(elementliste)

        self.assertEqual(umwandeln_zu_sql_statement(elementliste), sql_statement)



class TestQuery_umwandeln_in_ergebniss_dataframes(TestCase):
    def test_query_umwandeln_in_ergebniss_dataframes(self):
         df=pd.read_sql_query("SELECT patient_num, sex_cd, age_in_years_num from i2b2demodata.patient_dimension where age_in_years_num =19", con=con)
         df_geschlecht= df['sex_cd']
         df_alter=df['age_in_years_num']
         df_patient_Anzahl=df['patient_num'].count()
         from logik.verarbeitungsschicht import query_umwandeln_in_ergebniss_dataframes
         alles=query_umwandeln_in_ergebniss_dataframes(con,[])
         allesAnzahl=alles[0]
         allesAlter=alles[2]
         allesGeschlecht=alles[1]
         allesAnzahl==df_patient_Anzahl
         allesAlter.equals(df_alter)
         allesGeschlecht.equals(df_geschlecht)

con = bl.connection_zu_datenbank_aufbauen()

#Abfrage


class TestDataframe_knoten_mit_größe_in_einer_ebene_finden(TestCase):

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden0(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=0",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(0, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden1(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=1",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(1, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden2(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=2",con=conn,
            )

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(2, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden3(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=3",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(3, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden4(self):

        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=4",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(4, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden5(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
                        "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=5",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(5, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden6(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
                                    "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=6",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(6, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden7(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
                                    "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=7",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(7, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden8(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
                                    "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=8",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(8, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden9(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
                                    "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=9",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(9, conn)
        df.equals(df_2)
    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden10(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
                                    "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=10",con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(10, conn)
        df.equals(df_2)



baum=tie.treedictionary_aus_pickle_importieren('baum_mit_allem')
connection = bl.connection_zu_datenbank_aufbauen()

#KohortenAbfrage
from logik import kohortenabfrage as kab
import pandas as pd
from unittest import TestCase
from logik import verarbeitungsschicht as bl
import pytest
from logik import tree_dictionary_import_export as tie

baum=tie.treedictionary_aus_pickle_importieren('baum_mit_allem')
connection = bl.connection_zu_datenbank_aufbauen()

class TestKohortenAbfrage(TestCase):
    def testKohortenabfrageEinKritieren(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\Diagnoses\(A00-B99) Cert~ugmm"]],
                                            verknüpfungen=[]
                                            )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF,KlasseRasseDF,KlasseSpracheDF,KlasseGeschlechtDF,KlasseKohortengröße,KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse)

    def testKohortenabfrageZweiKritierenAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\Diagnoses\(A00-B99) Cert~ugmm"],
                                                           ['',"\Diagnoses\(I00-I99) Dise~3w8h"]],
                                                    verknüpfungen=['OR']
                                                    )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF= zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF

        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse)

    def testKohortenabfrageZweiKritierenAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\Diagnoses\(A00-B99) Cert~ugmm"],
                                                           ['',"\Diagnoses\(I00-I99) Dise~3w8h"]],
                                                verknüpfungen=['AND']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse)

    def testKohortenabfrageDreiKritierenOrOr(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['',"\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['',"\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['OR', 'OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse
                                                )

    def testKohortenabfrageDreiKritierenOrAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['',"\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['',"\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['OR', 'AND']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF=zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKritierenAndAnd(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['',"\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['',"\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['AND', 'AND']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF=zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse
                         )

    def testKohortenabfrageDreiKriterienAndOR(self):
        zutestendeAbfrage = kab.Kohortenabfrage(kriterien=[['',"\\Diagnoses\\(A00-B99) Cert~ugmm"],
                                                           ['',"\\Diagnoses\\(I00-I99) Dise~3w8h"],
                                                           ['',"\\Diagnoses\\(Q00-Q99) Cong~t96i"]],
                                                verknüpfungen=['AND', 'OR']
                                                )
        KlasseKohortengröße = zutestendeAbfrage.kohortengröße
        KlasseAlterDF = zutestendeAbfrage.df_alter
        KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
        KlasseSpracheDF = zutestendeAbfrage.df_sprache
        KlasseRasseDF = zutestendeAbfrage.df_rasse
        KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
        return KlasseAlterDF, KlasseRasseDF, KlasseSpracheDF, KlasseGeschlechtDF, KlasseKohortengröße, KlasseNebendiaDF
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
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
            self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
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
        self.assertEqual(zutestendeAbfrage,kab.Kohortenabfrage.kohortengröße,kab.Kohortenabfrage.df_alter ,
                         kab.Kohortenabfrage.df_geschlecht,kab.Kohortenabfrage.df_sprache,
        kab.Kohortenabfrage.df_rasse
                         )
class ReihenfolgeTesten(TestCase):
    def testReihenfolgeLeer(self):
        test=[]
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([],[]),test)

    def testReihenfolgeORda(self):
        test=['OR']
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen(['OR'], []), test)

    def testReihenfolgeANDda(self):
        test = ['AND']
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], ['AND']), test)

    def testReihenFOlGEANDundORda(self):
        test= ['AND', 'OR']
        self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen(['OR'], ['AND']), test)

    def testExceptionReihenFolgeLeerObwohlAND(self):
        with pytest.raises(Exception):
            test= []
            self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], ['AND']), test)

    def testExceptionReihenFolgeLeerObwohlANDOR(self):
        with pytest.raises(Exception):
            test = []
            self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen(['OR'], ['AND']), test)

    def testExceptionReihenFolgeBefülltObwohlleer(self):
        with pytest.raises(Exception):
            test = ['AND','OR']
            self.assertEqual(kab.Kohortenabfrage.reihenfolge_verknüpfungen([], []), test)

    def testFullNameUmwandelnAND(self):
        abfrage="External causes of morbidity (v00-y99)  AND Certain conditions originating in the perinatal period (p00-p96)"

        test1=(['\\Diagnoses\\(V00-Y99) Exte~2k58\\', '\\Diagnoses\\(P00-P96) Cert~6976\\'],['AND'])
        self.assertNotEqual(kab.Kohortenabfrage.umwandeln_in_fullname(abfrage,baum),test1)
    def testFullNameUmwandelnOR(self):
        abfrage="External causes of morbidity (v00-y99)  OR Certain conditions originating in the perinatal period (p00-p96)"
        test1=(['\\Diagnoses\\(V00-Y99) Exte~2k58\\', '\\Diagnoses\\(P00-P96) Cert~6976\\'],['OR'])
        self.assertNotEqual(kab.Kohortenabfrage.umwandeln_in_fullname(abfrage, baum), test1)
    def testFullNameUmwandeln(self):
        abfrage="External causes of morbidity (v00-y99)"
        test1=(['\\Diagnoses\\(V00-Y99) Exte~2k58\\'],[])
        self.assertNotEqual(kab.Kohortenabfrage.umwandeln_in_fullname(abfrage, baum), test1)


#Verarbeitungsschicht Neu
class TestConnection_zu_datenbank_aufbauen(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection
        self.assertEqual(bl_neu.connection_zu_datenbank_aufbauen(), connection)
class TestConnection_zu_datenbank_schließen(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection.close()
        self.assertEqual(bl_neu.connection_zu_datenbank_schließen(), connection.close())
class TestHDGrundgesamtheit(TestCase):
    def test_HDGrundgesamtheit(self):
        con= psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        df=pd.read_sql_query("select patient_num, sex_cd, age_in_years_num, language_cd,race_cd from i2b2demodata.patient_dimension",con)
        return df
        self.assertEqual(bl_neu.hd_abfrage_grundgesamtheit(), df)
class TestNDGrundgesamtheit(TestCase):
    def test_NDGrundgesamtheit(self):
        con= psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        df=pd.read_sql_query("select i2b2demodata.concept_dimension.name_char diagnose, count(distinct i2b2demodata.observation_fact.patient_num) Anzahl,TRUNC((count(distinct i2b2demodata.observation_fact.patient_num)*1.0)/134 * 100 , 2) as prozent from i2b2demodata.observation_fact join i2b2demodata.concept_dimension ON i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd where i2b2demodata.concept_dimension.concept_cd like 'ICD%' group by i2b2demodata.observation_fact.concept_cd,i2b2demodata.concept_dimension.name_char order by Anzahl desc, i2b2demodata.observation_fact.concept_cd limit 10;",con)
        return df

        self.assertEqual(bl_neu.nd_abfrage_grundgesamtheit(134, con), df)
class TestAbfragedurchführen(TestCase):
    def test_Abfragedurchführen(self):
        con= psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        df=pd.read_sql_query("select patient_num, sex_cd, age_in_years_num, language_cd,race_cd from i2b2demodata.patient_dimension",con)
        return df
        self.assertEqual(bl_neu.abfrage_durchführen(sql_statement="select patient_num, sex_cd, age_in_years_num, language_cd,race_cd from i2b2demodata.patient_dimension"), df)
class TestUmwandelnInSQLND(TestCase):
        def testSQLumwandelnND(self):
            con= psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
            genaueAbfrage=pd.read_sql_query("select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(P00-P96) Cert~6976\%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",con)
            return genaueAbfrage
            self.assertEqual(bl_neu.umwandeln_in_sql_statement_und_df_hauptdia_nebendia(["Certain conditions originating in the perinatal period (p00-p96) "], []), genaueAbfrage)
#connection
class TestConnection_zu_datenbank_aufbauenConnection(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection
        self.assertEqual(conn.create_connection(), connection)