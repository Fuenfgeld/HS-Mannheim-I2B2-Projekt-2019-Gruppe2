import pandas as pd
from unittest import TestCase
from logik import verarbeitungsschicht as bl
from logik import abfragen as ab

con = bl.connection_zu_datenbank_aufbauen()


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
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=1",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(1, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden2(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=2",
            con=conn,
        )

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(2, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden3(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=3",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(3, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden4(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=4",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(4, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden5(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=5",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(5, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden6(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=6",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(6, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden7(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=7",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(7, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden8(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=8",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(8, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden9(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=9",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(9, conn)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden10(self):
        conn = bl.connection_zu_datenbank_aufbauen()
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name,c_basecode, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=10",
            con=conn)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(10, conn)
        df.equals(df_2)
