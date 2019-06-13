import datetime
from logik import Verarbeitungsschicht_neu as bl
from logik import querystack as qs
import re

class Kohortenabfrage():

    __x_achse_altersverteilung=['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84', '>=65', '>=85', 'Unknown']


    def __reihenfolge_verknüpfungen(or_positions, and_positions):

        verknüpfungen=[]

        if or_positions ==[] and and_positions==[]:
            return verknüpfungen


        if or_positions != [] and and_positions == [] :
            for i in or_positions:
                verknüpfungen.append('OR')
            return verknüpfungen

        if or_positions==[] and and_positions !=[]:
            for i in and_positions:
                verknüpfungen.append('AND')
            return verknüpfungen

        if or_positions != [] and and_positions != []:
            or_index=0
            and_index = 0

            while  or_index < len(or_positions) and and_index < len(and_positions):
                if (or_positions[or_index] < and_positions[and_index]):
                    verknüpfungen.append('OR')
                    or_index+=1
                else:
                    verknüpfungen.append('AND')
                    and_index+=1

            if or_index < len(or_positions):
                for i in range(or_index,len(or_positions)):
                    verknüpfungen.append('OR')

            if and_index< len(and_positions):
                for i in range(and_index,len(and_positions)):
                    verknüpfungen.append('AND')

            return verknüpfungen

        return verknüpfungen


    def umwandeln_in_fullname(abfrage,baum):






        kriterien = re.split(' AND | OR ',abfrage)

        for i in range(len(kriterien)):
            kriterien[i]=kriterien[i].strip()

        or_positions=[match.start() for match in re.finditer(re.escape(' OR '), abfrage)]
        and_positions=[match.start() for match in re.finditer(re.escape(' AND '), abfrage)]

        verknüpfungen = Kohortenabfrage.__reihenfolge_verknüpfungen(or_positions,and_positions)
        fullnames = []




        #print(abfrage_in_liste)






        #print(kriterien)


        for i in kriterien:
            #print(i)
            found=False
            for j in baum.knotenliste_mit_baum:
                breakflag=False
                #print(j)
                for k in j:
                    #print(k.text)
                    if k.shortcode==i or k.text==i :
                        fullnames.append(k.fullname)
                        breakflag=True
                        found=True
                        break

                if breakflag==True:
                    break

            if found==False:
                raise IndexError

        print(fullnames)
        print(verknüpfungen)

        return Kohortenabfrage(fullnames, verknüpfungen)


    def __init__(self,kriterien,verknüpfungen,flag_push=True):
#    def __init__(self,abfrage,baum):
        self.kriterien = kriterien
        self.verknüpfungen=verknüpfungen

#        self.kriterien, self.verknüpfungen = self.umwandeln_in_fullname(abfrage,baum=baum)


        self.zeitpunkt = datetime.datetime.now()


        print('Abfrage gestartet')
        self.hd_sql_statement ,self.nd_sql_statement,\
        self.df_hauptdia,self.df_nebendia=bl.umwandeln_in_sql_statement_und_df_hauptdia_nebendia(self.kriterien, self.verknüpfungen)


        self.kohortengröße =len(self.df_hauptdia)
        #self.kohortengröße_prozent = round(((self.kohortengröße/133) *100),2)
        print(self.kohortengröße)

        self.df_alter = self.df_hauptdia['age_in_years_num']
        self.x_achse_altersverteilung=Kohortenabfrage.__x_achse_altersverteilung
        self.y_achse_altersverteilung=self.__altersverteilung_y_achse(df_alter=self.df_alter)

        self.df_geschlecht = self.df_hauptdia['sex_cd']
        self.geschlecht_value_counts=self.df_geschlecht.value_counts()

        self.df_sprache = self.df_hauptdia['language_cd']
        self.sprache_value_counts=self.df_sprache.value_counts()
        self.sprachex = self.sprache_value_counts.keys().tolist()
        self.sprachey = self.sprache_value_counts.tolist()



        self.df_rasse = self.df_hauptdia['race_cd'] #könnte aber auch noch aussoritert werden
        self.rasse_value_counts= self.df_rasse.value_counts()#könnte mit df_rasse aussortiert
        self.racex = self.rasse_value_counts.keys().tolist()
        self.racey = self.rasse_value_counts.tolist()





        self.nd_df_diagnose=self.df_nebendia['diagnose']
        self.nd_diagnose_value_list = self.nd_df_diagnose.values.tolist()

        self.nd_df_anzahl = self.df_nebendia['anzahl']
        self.nd_anzahl_value_list = self.nd_df_anzahl.values.tolist()

        self.nd_df_prozent = self.df_nebendia['prozent']
        self.nd_prozent_value_list = self.nd_df_prozent.values.tolist()


        if (flag_push==True):
            querystack = qs.Querystack.getInstance()
            self.kohortengröße_prozent = round(((self.kohortengröße / querystack.bottom().kohortengröße) * 100), 2)
            print(self.kohortengröße_prozent)
            querystack.push(self)
        else:
            self.kohortengröße_prozent = 100



    def __altersverteilung_y_achse(self,df_alter):

        df_alter.fillna(value='-')
        x_not_recorded = ((df_alter).eq('-')).sum()

        x_bis_9 = ((df_alter).lt(9)).sum()
        x_bis_17 = (((df_alter).ge(10)) & ((df_alter).le(17))).sum()
        x_bis_34 = (((df_alter).ge(18)) & ((df_alter).le(34))).sum()
        x_bis_44 = (((df_alter).ge(35)) & ((df_alter).le(44))).sum()
        x_bis_54 = (((df_alter).ge(45)) & ((df_alter).le(54))).sum()
        x_bis_64 = (((df_alter).ge(55)) & ((df_alter).le(64))).sum()
        x_bis_74 = (((df_alter).ge(65)) & ((df_alter).le(74))).sum()
        x_bis_84 = (((df_alter).ge(75)) & ((df_alter).le(84))).sum()
        x_gr_gl_65 = ((df_alter).ge(65)).sum()
        x_gr_gl_85 = ((df_alter).ge(85)).sum()

        y_achse=[x_bis_9,x_bis_17,x_bis_34,x_bis_44,x_bis_54,x_bis_64,x_bis_74,x_bis_84,x_gr_gl_65,x_gr_gl_85,x_not_recorded]

        return y_achse



#frage1=Kohortenabfrage(kriterien=["\Diagnoses"],  #["\Diagnoses\(I00-I99) Dise~3w8h","\Diagnoses\(Q00-Q99) Cong~t96i","\Diagnoses\(K00-K94) Dise~rl1r","\Diagnoses\(A00-B99) Cert~ugmm"],
#                       verknüpfungen=[])#['AND','AND','OR'])

#frage2=Kohortenabfrage(kriterien=["\Diagnoses\(I00-I99) Dise~3w8h","\Diagnoses\(Q00-Q99) Cong~t96i","\Diagnoses\(K00-K94) Dise~rl1r","\Diagnoses\(A00-B99) Cert~ugmm"],
#                       verknüpfungen=['AND','AND','OR'])


#querystack=qs.Querystack.instance()

#querypeek=querystack.peek()

#print(querypeek)
#print(querystack.peek())




#print(frage1.hd_sql_statement)



#print(frage1.df_hauptdia)
#print(frage1.df_nebendia)
#print(frage1.df_alter)
#print(frage1.df_geschlecht)
#print(frage1.zeitpunkt)
#print(frage_test.df_sprache)
#print(frage_test.df_rasse)
#print(frage1.geschlecht_value_counts)
#print(frage1.x_achse_altersverteilung)
#print(frage1.y_achse_altersverteilung)
#print(frage1.nd_diagnose_value_list)
#print(frage1.nd_anzahl_value_list)
#print(frage1.nd_prozent_value_list)