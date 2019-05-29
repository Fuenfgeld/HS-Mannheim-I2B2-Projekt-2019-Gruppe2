from logik import knoten_mit_wert as kn
from logik import abfragen as ab
from logik import verarbeitungsschicht as bl



def knotenliste_für_eine_ebene_erstellen(df_ebene):

        knotenliste_ebene = []
        for i in range(len(df_ebene)):
            knotenliste_ebene.append(
                kn.node_with_value(name=df_ebene.iloc[i][0], fullname=df_ebene.iloc[i][1], pfad=df_ebene.iloc[i][2],
                                   size=df_ebene.iloc[i][4]))
        print('Ebene erstellt')
        #print(knotenliste_ebene)
        #print(type(knotenliste_ebene))
        return knotenliste_ebene

def aus_knotenliste_baum_erstellen(knotenliste_gesamt):
    print(type(knotenliste_gesamt))
    for i in range(1, 11, 1):
    # print(i)

        print(len(knotenliste_gesamt[i]))

    # print(knotenliste_gesamt[i-1][0])
        for j in range(len(knotenliste_gesamt[i])):
            #print(j)
            ebenenindex = 0
            # print(knotenliste_gesamt[i-1][ebenenindex].fullname)
            # print(knotenliste_gesamt[i][ebenenindex].pfad)
            while knotenliste_gesamt[i - 1][ebenenindex].fullname != knotenliste_gesamt[i][j].pfad:
                ebenenindex += 1
            # print(ebenenindex)
            knotenliste_gesamt[i][j].parent = knotenliste_gesamt[i - 1][ebenenindex]
    #print(type(knotenliste_gesamt))
    return knotenliste_gesamt



def knotenliste_gesamt_erstellen():
        con=bl.connection_zu_datenbank_aufbauen()
        knotenliste_gesamt=[]

        for i in range(0,11,1):
            df_ebene=ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(i,con)
            knotenliste_gesamt.append(knotenliste_für_eine_ebene_erstellen(df_ebene))

        #print(knotenliste_gesamt)
        #print(type(knotenliste_gesamt))
        knotenliste_gesamt_mit_baum=aus_knotenliste_baum_erstellen(knotenliste_gesamt)

        return knotenliste_gesamt_mit_baum








