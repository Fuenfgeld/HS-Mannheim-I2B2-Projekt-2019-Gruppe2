from logik import tree_dictionary_import_export as tie

baum1 = tie.treedictionary_aus_pickle_importieren('baum_pickle')
wurzel = baum1.knotenliste_mit_baum[0][0]
wurzel.shortcode = 'Diagnoses'
wurzel.id='Diagnoses'

def create_data_from_node(path):
    if (path == []):
        data = {
            'name': wurzel.shortcode,
            'children': [{
                'name': i.shortcode,
                'size': i.size,
                # 'children':[{
                #   'name' : j.text,
                #   'size' : j.size
                #  }for j in i.children] #Dieser Bereich koennte einen weiteren aeußeren Ring hinzufuegen
            } for i in wurzel.children]
        }

    else:
        index = 0
        while baum1.knotenliste_mit_baum[len(path)][index].shortcode != path[-1]:
            index += 1;
        zwischenwurzel = baum1.knotenliste_mit_baum[len(path)][index]
        if not zwischenwurzel.children:
            data = {
                'name': zwischenwurzel.shortcode,
                'size': zwischenwurzel.size

            }
        else:
            data = {
                'name': zwischenwurzel.shortcode,
                'children': [{
                    'name': i.shortcode,
                    'size': i.size,
                    # 'children': [{
                    #   'name': j.text,
                    #    'size': j.size
                    # }for j in i.children] #Dieser Bereich koennte einen weiteren aeußeren Ring hinzufuegen
                } for i in zwischenwurzel.children]
            }
    for name in reversed(path[:-1]):
        data = {
            'name': name,
            'children': [data]
        }
    if len(path):
        data = {
            'name': wurzel.shortcode,
            'children': [data]
        }
    return data