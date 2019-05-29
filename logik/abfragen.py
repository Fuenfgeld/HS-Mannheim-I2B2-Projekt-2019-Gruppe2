import psycopg2 as psy
import pandas as pd
from logik import verarbeitungsschicht as bl


def dataframe_ebene_finden(ebene,con):
    df_ebene = pd.read_sql_query(f"""SELECT c_symbol, c_fullname, c_path, c_name  
                from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel={ebene}""", con=con)
    return df_ebene


def dataframe_knoten_mit_größe_in_einer_ebene_finden(ebene, con):
    df_ebene = pd.read_sql_query(f"""SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0)
             from i2b2metadata.icd10_icd9

LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path
    from i2b2demodata.observation_fact join i2b2demodata.concept_dimension
        on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd
group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo
    on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path
where c_tablename='concept_dimension' and c_hlevel={ebene}""", con=con)

    return df_ebene
