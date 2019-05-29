import psycopg2 as psy
import pandas as pd


def connection_zu_datenbank_aufbauen():
    connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")

    return connection


def abfrage_grundgesamtheit(db_connection):  # db_connection als globale finale statische Variable
    grundgesamtheit_data_frame = pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension', con=db_connection)
    return grundgesamtheit_data_frame

    # def erstellen_dataframe_altersverteilung_und_dataframe_geschlechtsvertelung(dataframe_abfrage):

    dataframe_altersverteilung = dataframe_abfrage


def abfrage_durchführen(sql_statement,
                        con=connection_zu_datenbank_aufbauen()):  # Idee ist ob man db_conmection als finale statische Variable

    query_ergebniss_data_frame = pd.read_sql_query(sql_statement, con)
    return query_ergebniss_data_frame


def umwandeln_in_sql_statement_nebendiagnose(hd_query_mitte, hd_anzahl, and_index):
    query_begin = f"""select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl,
     TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/{hd_anzahl} * 100 , 2) as prozent"""

    query_ende = """join
     (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char
     from i2b2demodata.observation_fact join i2b2demodata.concept_dimension
         on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia
        on (nebendia.patient_num =k0.patient_num)
        where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd)"""

    if (and_index > 0):
        for i in range(1, and_index + 1, 1):
            query_ende = '%s %s' % (query_ende, f"""AND (nebendia.concept_cd != k{i}.concept_cd)""")

    query_ende = '%s %s' % (query_ende, """group by nebendia.name_char
                                        order by Anzahl desc
                                        limit 10""")

    query_gesamt_nebendiagnose = '%s %s %s' % (query_begin, hd_query_mitte, query_ende)

    return query_gesamt_nebendiagnose


def umwandeln_in_sql_statement_und_df_hauptdia_nebendia(kriterien, verknüpfungen):
    verknüpfungen_index = 0
    kriterien_index = 1
    and_index = 0

    hd_query_begin = """select distinct i2b2demodata.patient_dimension.patient_num,
                i2b2demodata.patient_dimension.sex_cd,
                i2b2demodata.patient_dimension.age_in_years_num,
                i2b2demodata.patient_dimension.language_cd,
                i2b2demodata.patient_dimension.race_cd"""

    hd_query_mitte = f"""from
(select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num
    from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd
from i2b2demodata.concept_dimension
where (i2b2demodata.concept_dimension.concept_path like '%{kriterien[0]}%' escape '')"""

    if verknüpfungen is not None:
        while verknüpfungen_index < len(verknüpfungen):

            if (verknüpfungen[verknüpfungen_index] == 'OR'):
                hd_query_mitte = '%s %s' % (hd_query_mitte, f"""OR (i2b2demodata.concept_dimension.concept_path like 
                '%{kriterien[kriterien_index]}%' escape '')""")
                verknüpfungen_index += 1
                kriterien_index += 1

            else:
                hd_query_mitte = '%s %s' % (hd_query_mitte, f""") concept
                                    join i2b2demodata.observation_fact
                                    on concept.concept_cd = i2b2demodata.observation_fact.concept_cd
                                    join i2b2demodata.patient_dimension
                                    on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k{and_index}
                                    {f"on k{and_index - 1}.patient_num = k{and_index}.patient_num" if and_index >= 1 else ""}
                                    join
                                    (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num
                                    from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd
                                    from i2b2demodata.concept_dimension                    
                                    where (i2b2demodata.concept_dimension.concept_path like '%{kriterien[
                    kriterien_index]}%' escape '')""")
                verknüpfungen_index += 1
                kriterien_index += 1
                and_index += 1;

        hd_query_mitte = '%s %s' % (hd_query_mitte, f""") concept
                                    join i2b2demodata.observation_fact
                                    on concept.concept_cd = i2b2demodata.observation_fact.concept_cd
                                    join i2b2demodata.patient_dimension
                                    on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k{and_index}
                                    {f"on k{and_index - 1}.patient_num = k{and_index}.patient_num" if and_index >= 1 else ""}
                                    join i2b2demodata.patient_dimension
                                    on k0.patient_num = i2b2demodata.patient_dimension.patient_num
                                    """)

    hd_query_gesamt = '%s %s' % (hd_query_begin, hd_query_mitte)
    df_hd_query_gesamt = abfrage_durchführen(sql_statement=hd_query_gesamt)

    nd_query_gesamt = umwandeln_in_sql_statement_nebendiagnose(hd_query_mitte, len(df_hd_query_gesamt), and_index)
    df_nd_query_gesamt = abfrage_durchführen(sql_statement=nd_query_gesamt)
    return hd_query_gesamt, nd_query_gesamt, df_hd_query_gesamt, df_nd_query_gesamt
