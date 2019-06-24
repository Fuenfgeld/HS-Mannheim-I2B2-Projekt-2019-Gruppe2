import pandas as pd
from datenhaltung import connection


def connection_zu_datenbank_schließen(con):
    con.close()


def hd_abfrage_grundgesamtheit(
        con=connection.create_connection()):  # db_connection als globale finale statische Variable
    sql_statement = """select patient_num, sex_cd, age_in_years_num, language_cd,
                                                        race_cd from i2b2demodata.patient_dimension"""
    hd_grundgesamtheit_data_frame = pd.read_sql_query(sql_statement, con=con)
    return sql_statement, hd_grundgesamtheit_data_frame


def nd_abfrage_grundgesamtheit(hd_grundgesamtheit_anzahl, con=connection.create_connection()):
    sql_statement = f"""select i2b2demodata.concept_dimension.name_char diagnose, count(distinct i2b2demodata.observation_fact.patient_num) Anzahl,
       TRUNC((count(distinct i2b2demodata.observation_fact.patient_num)*1.0)/{hd_grundgesamtheit_anzahl} * 100 , 2) as prozent
from i2b2demodata.observation_fact
    join i2b2demodata.concept_dimension
        ON i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd
where i2b2demodata.concept_dimension.concept_cd like 'ICD%'
group by i2b2demodata.observation_fact.concept_cd,i2b2demodata.concept_dimension.name_char
order by Anzahl desc, i2b2demodata.observation_fact.concept_cd limit 10;"""
    nd_grundgesamtheit_data_frame = pd.read_sql_query(sql_statement, con=con)
    return sql_statement, nd_grundgesamtheit_data_frame


def abfrage_durchführen(sql_statement,
                        con=connection.create_connection()):  # Idee ist ob man db_conmection als finale statische Variable
    query_ergebniss_data_frame = pd.read_sql_query(sql_statement, con)
    return query_ergebniss_data_frame


def hauptdia_nebendia_grundgesamtheit():
    hd_query_grundgesamtheit, df_hd_query_grundgesamtheit = hd_abfrage_grundgesamtheit()
    nd_query_grundgesamtheit, df_nd_query_grundgesamtheit = nd_abfrage_grundgesamtheit(
        hd_grundgesamtheit_anzahl=len(df_hd_query_grundgesamtheit))

    return hd_query_grundgesamtheit, nd_query_grundgesamtheit, df_hd_query_grundgesamtheit, df_nd_query_grundgesamtheit


def umwandeln_in_sql_statement_und_df_hauptdia_nebendia_neu(kriterien, verknüpfungen):
    if not (kriterien == [] and verknüpfungen == []):

        hd_query = f'''
        
        select distinct i2b2demodata.patient_dimension.patient_num,
       i2b2demodata.patient_dimension.sex_cd,
       i2b2demodata.patient_dimension.age_in_years_num,
       i2b2demodata.patient_dimension.language_cd,
       i2b2demodata.patient_dimension.race_cd

from i2b2demodata.patient_dimension

where i2b2demodata.patient_dimension.patient_num {kriterien[0][0]} in (

    select i2b2demodata.observation_fact.patient_num
      from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd

            from i2b2demodata.concept_dimension
            where (i2b2demodata.concept_dimension.concept_path like '{kriterien[0][1]}%' escape
                   '')) concept
               join i2b2demodata.observation_fact
                    on concept.concept_cd = i2b2demodata.observation_fact.concept_cd

               join i2b2demodata.patient_dimension
                    on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num


    )
        
        
        '''

        for i in range(len(verknüpfungen)):
            hd_query = '%s %s' % (hd_query, f'''
        {verknüpfungen[i]} i2b2demodata.patient_dimension.patient_num {kriterien[i + 1][0]} in (

    select i2b2demodata.observation_fact.patient_num
      from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd

            from i2b2demodata.concept_dimension
            where (i2b2demodata.concept_dimension.concept_path like '{kriterien[i + 1][1]}%' escape
                   '')) concept
               join i2b2demodata.observation_fact
                    on concept.concept_cd = i2b2demodata.observation_fact.concept_cd

               join i2b2demodata.patient_dimension
                    on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num


    )
        
        
        ''')

        df_hd_query = abfrage_durchführen(sql_statement=hd_query)

        nd_query = umwandeln_in_sql_statement_nebendiagnose_neu(kriterien=kriterien, hd_query=hd_query,
                                                                hd_anzahl=len(df_hd_query))

        df_nd_query = abfrage_durchführen(sql_statement=nd_query)

        print(df_nd_query)

        return hd_query, nd_query, df_hd_query, df_nd_query

    else:

        hd_query_gesamt, df_hd_query_gesamt = hd_abfrage_grundgesamtheit()
        nd_query_gesamt, df_nd_query_gesamt = nd_abfrage_grundgesamtheit(len(df_hd_query_gesamt))
        return hd_query_gesamt, nd_query_gesamt, df_hd_query_gesamt, df_nd_query_gesamt


def umwandeln_in_sql_statement_nebendiagnose_neu(kriterien, hd_query, hd_anzahl):
    nd_query_begin = f'''
        select nebendia.name_char as diagnose,
       count(distinct nebendia.patient_num) as anzahl,
       TRUNC((count(distinct nebendia.patient_num) * 1.0) / {hd_anzahl} * 100, 2) as prozent
    from
    '''

    nd_query_mitte = f''' ({hd_query}) hauptdiagnose

join

(select i2b2demodata.observation_fact.patient_num,
        i2b2demodata.observation_fact.concept_cd,
        i2b2demodata.concept_dimension.concept_path,
        i2b2demodata.concept_dimension.name_char
    from i2b2demodata.observation_fact
        join i2b2demodata.concept_dimension
            on i2b2demodata.observation_fact.concept_cd = i2b2demodata.concept_dimension.concept_cd

    where i2b2demodata.concept_dimension.concept_cd like 'ICD%'

    )nebendia

on hauptdiagnose.patient_num = nebendia.patient_num 
where nebendia.concept_path not like '{kriterien[0][1]}%' '''

    for i in range(1, len(kriterien), 1):
        nd_query_mitte = '%s %s' % (nd_query_mitte, f'''
            and nebendia.concept_path not like '{kriterien[i][1]}%' 
        ''')

    nd_query_ende = '''group by nebendia.name_char
order by Anzahl desc
limit 10'''

    nd_query_gesamt = '%s %s %s' % (nd_query_begin, nd_query_mitte, nd_query_ende)

    return nd_query_gesamt
