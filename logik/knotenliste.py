import knoten as kn
from logik import abfragen as ab
import re
from datenhaltung import connection


def größe_für_Elternknoten_feststellen(Knoten):
    Elternknoten = list(Knoten.ancestors())
    index = -1
    while Elternknoten[index].size == 0 and index * (-1) < len(Elternknoten):
        Elternknoten[index].size = ab.größe_für_einzelnen_Knoten_herausfinden()
        index -= 1


def knotenliste_für_eine_ebene_erstellen(df_ebene):
    knotenliste_ebene = []
    for i in range(len(df_ebene)):
        knotenliste_ebene.append(
            kn.node_with_value(name=df_ebene.iloc[i][0], fullname=df_ebene.iloc[i][1], pfad=df_ebene.iloc[i][2],
                               text=df_ebene.iloc[i][3], shortName=df_ebene.iloc[i][3], basecode=df_ebene.iloc[i][4],
                               shortcode=re.sub("ICD10:|ICD9:", '', str(df_ebene.iloc[i][4])),
                               id=re.sub("ICD10:|ICD9:", '', str(df_ebene.iloc[i][4])),
                               size=int(df_ebene.iloc[i][5])))
    index = 0;
    count_doppelte = 0
    while knotenliste_ebene[index] and index < len(knotenliste_ebene) - 1:
        if knotenliste_ebene[index].fullname == knotenliste_ebene[index + 1].fullname:
            knotenliste_ebene.remove(knotenliste_ebene[index + 1])
            count_doppelte += 1
        else:
            index += 1
    return knotenliste_ebene


def aus_knotenliste_baum_erstellen(knotenliste_gesamt, con):
    for i in range(10, 0, -1):
        for j in range(len(knotenliste_gesamt[i])):
            ebenenindex = 0
            while knotenliste_gesamt[i - 1][ebenenindex].fullname != knotenliste_gesamt[i][j].pfad:
                ebenenindex += 1
            knotenliste_gesamt[i][j].parent = knotenliste_gesamt[i - 1][ebenenindex]
            if knotenliste_gesamt[i][j].size != 0:
                if knotenliste_gesamt[i - 1][ebenenindex].size == 0:
                    knotenliste_gesamt[i - 1][ebenenindex].size = int(ab.größe_für_einzelnen_Knoten_herausfinden(
                        knotenliste_gesamt[i - 1][ebenenindex], con=con))
    return knotenliste_gesamt


def knotenliste_gesamt_erstellen():
    knotenliste_gesamt = []
    for i in range(0, 11, 1):
        df_ebene = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(i, con=connection.create_connection())
        knotenliste_gesamt.append(knotenliste_für_eine_ebene_erstellen(df_ebene))
    knotenliste_gesamt_mit_baum = aus_knotenliste_baum_erstellen(knotenliste_gesamt, con=connection.create_connection())
    return knotenliste_gesamt_mit_baum
