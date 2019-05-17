import Knoten as kn


class Knotenliste:


    def knotenliste_für_eine_ebene_erstellen(df_ebene):
     knotenliste_ebene = []
     for i in range(len(df_ebene)):
            knotenliste_ebene.append(
            kn.node_with_value(name=df_ebene.iloc[i][0], fullname=df_ebene.iloc[i][1], pfad=df_ebene.iloc[i][2],
                            size=df_ebene.iloc[i][4]))
     print('Ebene erstellt')

     return knotenliste_ebene