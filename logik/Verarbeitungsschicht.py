#Alle Abfragen beschränken Sich auf die Darstellung der Geschlechts und Altersverteilung
import psycopg2 as psy
import pandas as pd





def connection_zu_datenbank_aufbauen():
    connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.79", port="5432")
    return connection


def abfrage_grundgesamtheit(db_connection):#db_connection als globale finale statische Variable
    grundgesamtheit_data_frame=pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension', con = db_connection)
    return grundgesamtheit_data_frame

#def erstellen_dataframe_altersverteilung_und_dataframe_geschlechtsvertelung(dataframe_abfrage):

    dataframe_altersverteilung=dataframe_abfrage


def abfrage_durchführen(sql_statement,db_connection):#Idee ist ob man db_conmection als finale statische Variable

    query_ergebniss_data_frame=pd.read_sql_query(sql_statement,db_connection)
    print(query_ergebniss_data_frame)
    return query_ergebniss_data_frame

def umwandeln_zu_sql_statement(queryelements):
    sql_statement='SELECT * FROM i2b2demodata.patient_dimension WHERE'#Dieser Code muss noch angepasst werden.
    #Vorallem das Ende mit Joins etc. muss gewährleistet sein.
    for i in queryelements:
        sql_statement='%s %s' % (sql_statement,i)
    return sql_statement




#def umwandeln_tupelliste_zu_pandas_dataframe(tupelliste):
    #tupelliste=pd.DataFrame(tupelliste)
    #return tupelliste

#def erstellen_histogramm_geschlechterverteilung(dataframe_geschlecht):
    #print(dataframe_geschlecht)
    #plt.hist(x=dataframe_geschlecht)
    #plt.show()

#def erstellen_histogramm_altersverteilung(dataframe_alter):
    #print(dataframe_alter)
    #plt.hist(dataframe_alter, bins=100, orientation='horizontal')
    #plt.show()



def query_umwandeln_in_ergebniss_dataframes(db_connection, query=[]):
    if query==[]:
        sql_statement="SELECT patient_num, sex_cd, age_in_years_num from i2b2demodata.patient_dimension"#Frage ob wir bei der Grundgesamtheit andere Informationen als die Standartsattribute wie patient_num, sex-cd und age_in_years_num
    else:
        sql_statement=umwandeln_zu_sql_statement(query)

    query_ergebnis_dataframe=abfrage_durchführen(sql_statement,db_connection=db_connection)
    geschlechter_dataframe=query_ergebnis_dataframe['sex_cd'].value_counts()
    altersverteilung_dataframe=query_ergebnis_dataframe['age_in_years_num']
    patienten_anzahl=query_ergebnis_dataframe['patient_num'].count()
    return patienten_anzahl, geschlechter_dataframe, altersverteilung_dataframe