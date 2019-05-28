from unittest import TestCase
import psycopg2 as psy
import pandas as pd
import Verarbeitungsschicht as bl
import Knotenliste as kl
import Abfragen as ab

con = bl.connection_zu_datenbank_aufbauen()




# Abfragen
class TestDataframe_ebene_finden(TestCase):

    def test_dataframe_ebene_finden0(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=0", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(0,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden1(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=1", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(1,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden2(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=2", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(2,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden3(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=3", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(3,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden4(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=4", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(4,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden5(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=5", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(5,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden6(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=6", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(6,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden7(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=7", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(7,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden8(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=8", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(8,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden9(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=9", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(9,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden10(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=10", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(10,con)
    df.equals(df_2)

class TestDataframe_knoten_mit_größe_in_einer_ebene_finden(TestCase):

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden0(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=0",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(0, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden1(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=1", con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(1, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden2(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=2",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(2, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden3(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=3",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(3, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden4(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=4",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(4, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden5(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=5",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(5, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden6(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=6",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(6, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden7(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=7",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(7, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden8(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=8",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(8, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden9(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=9",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(9, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden10(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=10",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(10, con)
        df.equals(df_2)

# Verarbeitungsschicht
class TestConnection_zu_datenbank_aufbauen(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection
        self.assertEqual(connection_zu_datenbank_aufbauen(), connection)


class TestAbfrage_grundgesamtheit(TestCase):
    def test_abfrage_grundgesamtheit(self):
        from Verarbeitungsschicht import abfrage_grundgesamtheit
        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen
        pd.testing.assert_frame_equal(abfrage_grundgesamtheit(db_connection=connection_zu_datenbank_aufbauen()),
                                      pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension',
                                                        con=psy.connect(database="i2b2", user="i2b2",
                                                                        password="demouser", host="129.206.7.75",
                                                                        port="5432")))


class TestAbfrage_durchführen(TestCase):
    def test_abfrage_durchführen(self):
        from Verarbeitungsschicht import abfrage_durchführen
        df=pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension', con=con)
        abfrage='SELECT * from i2b2demodata.patient_dimension'
        df_2= abfrage_durchführen(abfrage,con)
        print(df.equals(df_2))



class TestUmwandeln_zu_sql_statement(TestCase):
    def test_umwandeln_zu_sql_statement(self):
        elementliste=['a','b','c']
        sql_statement='SELECT * FROM i2b2demodata.patient_dimension WHERE a b c'
        print(sql_statement)

        from Verarbeitungsschicht import umwandeln_zu_sql_statement
        print(umwandeln_zu_sql_statement(elementliste))

        self.assertEqual(umwandeln_zu_sql_statement(elementliste), sql_statement)



class TestQuery_umwandeln_in_ergebniss_dataframes(TestCase):
    def test_query_umwandeln_in_ergebniss_dataframes(self):
         df=pd.read_sql_query("SELECT patient_num, sex_cd, age_in_years_num from i2b2demodata.patient_dimension where age_in_years_num =19", con=con)
         df_geschlecht= df['sex_cd']
         df_alter=df['age_in_years_num']
         df_patient_Anzahl=df['patient_num'].count()
         from Verarbeitungsschicht import query_umwandeln_in_ergebniss_dataframes
         alles=query_umwandeln_in_ergebniss_dataframes(con,[])
         allesAnzahl=alles[0]
         allesAlter=alles[2]
         allesGeschlecht=alles[1]
         allesAnzahl==df_patient_Anzahl
         allesAlter.equals(df_alter)
         allesGeschlecht.equals(df_geschlecht)


# Knotenliste
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
        from Knotenliste import knotenliste_gesamt_erstellen, aus_knotenliste_baum_erstellen
        knoten=knotenliste_gesamt_erstellen()
        baum=aus_knotenliste_baum_erstellen()
        baum==knotenliste_gesamt_erstellen()
    def knotenlistegesamterstellen(self):
        from Knotenliste import knotenliste_für_eine_ebene_erstellen
        con=bl.connection_zu_datenbank_aufbauen()
        knotenliste_gesamt=[]

        for i in range(0,11,1):
            df_ebene=ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(i,con)
            knotenliste_gesamt.append(knotenliste_für_eine_ebene_erstellen(df_ebene))
        return knotenliste_gesamt


class TestKnotenliste_für_eine_ebene_erstellen(TestCase):
    def test_knotenliste_für_eine_ebene_erstellen(self):
        dict_ebene = {'name': ['Knoten1', 'Knoten2'], 'fullname': ['Fullname1', 'Fullname2'],
                      'Pfad': ['Pfad1', 'Pfad2'],
                      'Symbol': ['Symbol1', 'Symbol2'], 'Size': [0, 1]}
        df_ebene = pd.DataFrame(data=dict_ebene)

        # print(df_ebene)

        from KnotenMitWert import node_with_value
        knotenliste = [
            node_with_value(name='Knoten1', fullname='Fullname1', pfad='Pfad1', size=0),
            node_with_value(name='Knoten2', fullname='Fullname2', pfad='Pfad2', size=1)]
        from Knotenliste import knotenliste_für_eine_ebene_erstellen
        # self.assertEqual(knotenliste_für_eine_ebene_erstellen(dataframe_ebene), knotenliste)
        self.assertEqual(knotenliste_für_eine_ebene_erstellen(df_ebene), knotenliste)


class TestKnotenliste_gesamt_erstellen(TestCase):
    def test_knotenliste_gesamt_erstellen(self):

        from Knotenliste import knotenliste_gesamt_erstellen
        from treedictionary_in_pickle_exportieren import treedictionary_aus_pickle_importieren
        baum=treedictionary_aus_pickle_importieren('baum_mit_var_text')
        baum_Methode=knotenliste_gesamt_erstellen()
        baum.equals(baum_Methode)




