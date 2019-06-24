from unittest import TestCase
import pandas as pd
import psycopg2 as psy
from logik import verarbeitungsschicht as bl

con = bl.connection_zu_datenbank_aufbauen()

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
        abfrage="select patient_num, sex_cd, age_in_years_num, language_cd,race_cd from i2b2demodata.patient_dimension"
        df=pd.read_sql_query(abfrage,con)
        return df
        self.assertEqual(bl_neu.hd_abfrage_grundgesamtheit(),abfrage, df)
        con.close()
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
class TestUmwandelnInSQLundHDND(TestCase):
        def testSQLumwandelundHDND(self):
            con= psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
            genaueAbfrage=pd.read_sql_query("select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(P00-P96) Cert~6976\%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",con)
            return genaueAbfrage
            self.assertEqual(bl_neu.umwandeln_in_sql_statement_und_df_hauptdia_nebendia(["Certain conditions originating in the perinatal period (p00-p96) "], []), genaueAbfrage)
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
