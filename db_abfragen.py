import pandas.io.sql as psql
import psycopg2 as psy

connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")





def get_icd_level_query_df(icdLevel):
    dfICDLevel = psql.read_sql_query(f"""
                        select c_hlevel as level, c_name as name, c_basecode as ICDcode
                        from i2b2.i2b2metadata.icd10_icd9
                        where c_fullname like '%Diagnoses%' and c_basecode like 'ICD10%' 
                        and c_hlevel = {icdLevel} 
                        order by c_basecode""",
                                     con=connection)

    return dfICDLevel


def get_next_level_codes(icdLevel, icdCode):
    dfICDLevel = psql.read_sql_query(f"""
                        select c_hlevel as level, c_name as name, c_basecode as ICDcode, c_tooltip as pathSimple
                        from i2b2.i2b2metadata.icd10_icd9
                        where c_fullname like '%Diagnoses%' and c_basecode like 'ICD10:{icdCode}%' 
                        and c_hlevel = {icdLevel}
                        order by c_basecode""",
                                     con=connection)
    return dfICDLevel  # returns the query as dataframe