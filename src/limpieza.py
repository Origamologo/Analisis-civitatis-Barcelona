import pandas as pd
import numpy as np
import re

def pastor_de_guiris(df, ciudades):
    '''
    Separate, organize and save data in pickle format
    for the chosen city or cities.
    The dates will be the index and we will have columns for:
        - Number of travelers living in Spain
        - Number of travelers living abroad
        - Number of overnight stays by travelers living in Spain
        - Number of overnight stays by travelers living abroad
        - Average overnight stays of travelers living in Spain
        - Average overnight stays of travelers living abroad
        - The total number of travelers, adding nationals and foreigners
        - The total number of overnight stays, adding those of national travelers
          with those of foreigners
        - The average of the total overnight stays
    Args:
        df (pandas.DataFrame): the data frame containing the data
                               of ALL tourist areas
        ciudades (list): list with the city or cities from which
                         you want to extract the data
    Methods:
        pernocguiris / numguiris: divides the number of overnight stays
                                  between the number of travelers to obtain
                                  the average number of overnight stays
        numguiris_esp + numguiris_ext: sums the national travelers with the
                                       foreigners to get the total number
                                       of tourists
        pernocguiris_esp + pernocguiris_ext: sums national overnight stays
                                             with foreigners to obtain the
                                             total number of tourists
    Return:
        Saves the new data frame in pickle format under the name of the city
        followed by '_guiris_esquilados.pkl'
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
        
        guiris_esquilados.to_pickle(rf'C:\Users\mituc\Ironhack\Curso\IronLabs\Proyecto-1\data\{ciudad}_guiris_esquilados.pkl')
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

def dict_civitatis_completo(lista):
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

def dict_civitatis_5(lista):
    dict_revius = {'fecha' : [],
               'nombre' : [],
               'procedencia' : [],
               'opinion' : [],
               'viajo_con' : []}
    for reviu in lista:
        if len(reviu)==5:
            dict_revius['fecha'].append(reviu[0])
            dict_revius['nombre'].append(reviu[1])
            dict_revius['procedencia'].append(reviu[2])
            dict_revius['opinion'].append(reviu[3])
            dict_revius['viajo_con'].append(reviu[4])
    return dict_revius

def dict_civitatis_2_4(lista):
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
        
    return dict_revius

def drop_tourist(df):
    num_remove = int((len(df['fecha']) * 23.6) //100)
    drop_tourist = np.random.choice(df.index, num_remove, replace=False)
    df = df.drop(drop_tourist)
    return df

def values_sin_espacios(df):
    for i in df.columns:
        df[i] = df[i].str.strip()
    return df

def date_time(df):
    df['fecha'] = df['fecha'].str.replace(' / ', '-')
    df['fecha'] = df['fecha'].str.replace('Ene', '01')
    df['fecha'] = df['fecha'].str.replace('Feb', '02')
    df['fecha'] = df['fecha'].str.replace('Mar', '03')
    df['fecha'] = df['fecha'].str.replace('Abr', '04')
    df['fecha'] = df['fecha'].str.replace('May', '05')
    df['fecha'] = df['fecha'].str.replace('Jun', '06')
    df['fecha'] = df['fecha'].str.replace('Jul', '07')
    df['fecha'] = df['fecha'].str.replace('Ago', '08')
    df['fecha'] = df['fecha'].str.replace('Sep', '09')
    df['fecha'] = df['fecha'].str.replace('Oct', '10')
    df['fecha'] = df['fecha'].str.replace('Nov', '11')
    df['fecha'] = df['fecha'].str.replace('Dic', '12')
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%Y')
    return df