import pandas as pd
import tree_dictionary_import_export as tie

baum1 = tie.treedictionary_aus_pickle_importieren('baum_mit_shortcode')
wurzel = baum1.knotenliste_mit_baum[0][0]

def create_table_from_node(path):
    df_tabelle=pd.DataFrame(data=[],columns=['Shortcode','Text'])

    if path==[]:
        for i in wurzel.children:
            if i.size>0:
                df_tabelle=df_tabelle.append({'Shortcode':i.shortcode,'Text':i.text},ignore_index=True)

    else:
        index = 0
        while baum1.knotenliste_mit_baum[len(path)][index].shortcode != path[-1]:
            #    print(baum.knotenliste_mit_baum[len(path)][index].text)
            index += 1;
        zwischenwurzel = baum1.knotenliste_mit_baum[len(path)][index]
        df_tabelle=df_tabelle.append({'Shortcode':zwischenwurzel.shortcode,'Text':zwischenwurzel.text},ignore_index=True)
        for i in zwischenwurzel.children:
            if i.size>0:
                df_tabelle=df_tabelle.append({'Shortcode':i.shortcode,'Text':i.text},ignore_index=True)

    df_tabelle=df_tabelle.sort_values(by=['Shortcode'])

    dict_tabelle=df_tabelle.to_dict()
    print(dict_tabelle)
    print(df_tabelle)

    dict_tabelle=df_tabelle.to_dict('records')
    print(dict_tabelle)
    return dict_tabelle
