import tree_dictionary_import_export as tie

baum1 = tie.treedictionary_aus_pickle_importieren('baum_mit_var_text')

wurzel=baum1.knotenliste_mit_baum[0][0]

def create_data_from_node(path):

    if (path==[]) :
        data = {
            'name' : wurzel.text,
            'children' : [{
                'name' : i.text,
                'size' : i.size,
               # 'children':[{
                #   'name' : j.text,
                #   'size' : j.size
              #  }for j in i.children] #Dieser Bereich könnte einen weiteren äußeren Ring hinzufürgen
            }for i in wurzel.children]
        }

    else :
        index=0
        #print('Angeklickt' +str(path[-1]))
        #print(len(path))
        while baum1.knotenliste_mit_baum[len(path)][index].text != path[-1]:
        #    print(baum.knotenliste_mit_baum[len(path)][index].text)

            index+=1;
        zwischenwurzel=baum1.knotenliste_mit_baum[len(path)][index]


        if not zwischenwurzel.children:

            data = {
                'name' : zwischenwurzel.text,
                'size' : zwischenwurzel.size

            }

        else:
            data = {
                'name' : zwischenwurzel.text,
                'children' : [{
                    'name' : i.text,
                    'size' : i.size,
                   # 'children': [{
                    #   'name': j.text,
                    #    'size': j.size
                   # }for j in i.children]#Dieser Bereich könnte eine zweiten äußeren Ring realisieren

                }for i in zwischenwurzel.children]
            }


    for name in reversed(path[:-1]):
        data = {
            'name': name,
            'children': [data]
        }
    if len(path):

        data = {
            'name': wurzel.text,
            'children': [data]
        }

    return data
