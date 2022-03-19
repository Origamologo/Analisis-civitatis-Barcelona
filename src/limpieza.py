import pandas as pd
import re

def pastor_de_guiris(df, ciudades):
    '''
    Separa, organiza y guarda en formato pickle los datos 
    de la ciudad o ciudades elegidas.
    Las fechas serán el index y tendremos columnas para:
        - Número de viajeros residentes en Espana
        - Número de viajeros residentes en el extranjero
        - Número de pernoctaciones de los viajeros residentes en Espana
        - Número de pernoctaciones de los viajeros residentes en el extranjero
        - Media de pernoctaciones de los viajeros residentes en Espana
        - Media de pernoctaciones de los viajeros residentes en el extranjero
        - El número total de viajeros, sumando nacionales y extranjeros
        - El número total de pernoctaciones, sumando las de viajeros nacionales
          con las de los extranjeros
        - La media del total de pernoctaciones
    Args:
        df (pandas.DataFrame): el data frame que contiene los datos 
                               de TODAS las zonas turísticas
        ciudades (list): lista con la ciudad o ciudades de las que 
                         se desea extraer los datos
    Methods:
        pernocguiris / numguiris: divide el número de pernoctaciones 
                                  entre el número de viajeros para obtener 
                                  la media de pernoctaciones
        numguiris_esp + numguiris_ext: suma los viajeros nacionales con los 
                                       extranjeros para obtener el número total 
                                       de turistas
        pernocguiris_esp + pernocguiris_ext: suma las pernoctaciones nacionales 
                                             con las extranjeras para obtener el 
                                             número total de turistas
    Return:
        Guarda el nuevo data frame en formato pickle bajo el nombre de la ciudad
        seguido '_guiris_esquilados.pkl'
    '''

    for ciudad in ciudades:
        # Separamos la zona turistica
        df_guiris_zona = df[df['puntos_turisticos'].str.contains(ciudad) == True]
        # Aislamos los viajeros residentes en Espana
        df_numguiris = df_guiris_zona[df_guiris_zona['viajeros_y_pernoctaciones'].str.contains('viajero') == True]
        df_numguiris_esp = df_numguiris[df_numguiris['residencia'].str.contains('residentes_espana') == True]
        # Aislamos a los turistas residentes en el extranjero
        df_numguiris_ext = df_numguiris[df_numguiris['residencia'].str.contains('residentes_en_el_extranjero') == True]
        # Aislamos las pernocctaciones de los viajeros residentes en Espana
        df_pernocguiris = df_guiris_zona[df_guiris_zona['viajeros_y_pernoctaciones'].str.contains('pernoctaciones') == True]
        df_pernocguiris_esp =  df_pernocguiris[df_pernocguiris['residencia'].str.contains('residentes_espana') == True]
        # Aislamos las pernocctaciones de los viajeros residentes en el extranjero
        df_pernocguiris_ext =  df_pernocguiris[df_pernocguiris['residencia'].str.contains('residentes_en_el_extranjero') == True]

        guiris_esquilados = pd.concat([df_numguiris_esp['total'], 
                                    df_numguiris_ext['total'],
                                    df_pernocguiris_esp['total'],
                                    df_pernocguiris_ext['total']], axis=1)

        guiris_esquilados.columns = ['viajeros_espana', 
                                    'viajeros_extranjero',
                                    'pernoctaciones_espana',
                                    'pernoctaciones_extranjero']

        guiris_esquilados['media_pernoc_esp'] = round((df_pernocguiris_esp['total'] / df_numguiris_esp['total']), 1)
        guiris_esquilados['media_pernoc_ext'] = round((df_pernocguiris_ext['total'] / df_numguiris_ext['total']), 1)
        guiris_esquilados['total_viajeros'] = df_numguiris_esp['total'] + df_numguiris_ext['total']
        guiris_esquilados['total_pernoctaciones'] = df_pernocguiris_esp['total'] + df_pernocguiris_ext['total']
        guiris_esquilados['media_total_pernoc'] = round((guiris_esquilados['total_pernoctaciones'] / guiris_esquilados['total_viajeros']), 1)
        
        guiris_esquilados.to_pickle(f'{ciudad}_guiris_esquilados.pkl')
    return

def pulir(lista):
    for reviu in lista:
        reviu.pop()
        reviu.pop(1)
        for i in reviu:
            if i == ' 16195 opiniones':
                del reviu[reviu.index(i): (reviu.index(i)+5)]
            elif i == ' Opinión traducida. Mostrar en idioma original':
                del reviu[reviu.index(i)]
    return  lista

def quitar_respuestas(lista):
    for reviu in lista:
        if len(reviu)==6:
            reviu.pop(-2)
    return lista

def dict_civitatis(lista):
    dict_revius = {'fecha' : [],
               'nombre' : [],
               'procedencia' : [],
               'opinion' : [],
               'viajo_con' : []}
    for reviu in lista:
        if len(reviu)==2:
            dict_revius['fecha'].append(reviu[0])
            dict_revius['nombre'].append(reviu[1])
            dict_revius['procedencia'].append('')
            dict_revius['opinion'].append('')
            dict_revius['viajo_con'].append('')
        elif len(reviu)==3:
            dict_revius['fecha'].append(reviu[0])
            dict_revius['nombre'].append(reviu[1])
            if len(re.findall(' Viajó.*', reviu[2]))>0:
                dict_revius['procedencia'].append('')
                dict_revius['opinion'].append('')
                dict_revius['viajo_con'].append(reviu[2])
            else:
                dict_revius['procedencia'].append(reviu[2])
                dict_revius['opinion'].append('')
                dict_revius['viajo_con'].append('')
        elif len(reviu)==4:
            dict_revius['fecha'].append(reviu[0])
            dict_revius['nombre'].append(reviu[1])
            dict_revius['procedencia'].append(reviu[2])
            if len(re.findall(' Viajó.*', reviu[3]))>0:
                dict_revius['opinion'].append('')
                dict_revius['viajo_con'].append(reviu[3])
            else:
                dict_revius['opinion'].append(reviu[3])
                dict_revius['viajo_con'].append('')
        else:
            dict_revius['fecha'].append(reviu[0])
            dict_revius['nombre'].append(reviu[1])
            dict_revius['procedencia'].append(reviu[2])
            dict_revius['opinion'].append(reviu[3])
            dict_revius['viajo_con'].append(reviu[4])
    return dict_revius