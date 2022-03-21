import pandas as pd
import numpy as np
import re

# FUNCTION TO CLEAN THE CSV FROM THE GOVERMENT

def pastor_de_guiris(df, ciudades):
    '''
    Separates, organizes and saves the data in pickle format
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

# FUNCTIONS TO CLEAN AND ORGANIZE THE INFORMATION FROM THE REVIEWS OBTAINED IN THE SCRAPING

def revius_separados(revius):
    """
    It organizes the result of the scraping so we can have the reviews as separate elements.
        1. It will join all the separate elements into a single string
        2. It will cut the string by the element that divides the reviews, 
             generating a list of lists, each sublist being one review
        3. It will discard the blank sublists
        4. It will divide each piece of information of the sublists (reviews) 
           into separate strings
    Returns:
        A list of lists, each sublist corresponding to a review
    """
    civitatis = [' '.join(str(i) for i in revius)]
    corte = '\ue9ce\ue9ce\ue9ce\ue9ce\ue9ce\n'
    civitatis_ = civitatis[0].split(corte)
    civitatis_revius = [i for i in civitatis_[2::2]]
    civitatis_revius_limpio = [i.split('\n') for i in civitatis_revius]
    return civitatis_revius_limpio

def pulir(lista):
    """
    It cleans the reviews from the elements that give useless information:
        - Blank strings at the end
        - A string containing the initial letter of the client's name
        - All the strings that contain information from the bottom of 
          the web page, completely unrelated with the reviews
    Arg:
        lista (list): the list of lists to be cleaned
    Returns:
        The list of reviews whithout the undesired elements
    """
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
    """
    Whenever there was a bad review, there will a string containing the answer from the company.
    As we don't need this particular piece of information, this function erase it.
    Arg:
        lista (list): the list to be cleanned from company answers
    Method:
        All the sublists have a length from 2 to 5, except those containing an answer, 
        which measure 6, so we will apply the function to len(sublist) == 6
    Returns:
        The list of reviews without the company answer
    """
    for reviu in lista:
        if len(reviu)==6:
            reviu.pop(-2)
    return lista

def dict_civitatis_completo(lista):
    """
    It creates a dicctionary with the desired information for each review, 
    so we can create a data frame from it.
    Arg:
        lista (list): the list of lists containing the cleanned reviews
    Returns:
        A dictionary containing the elements of each review
    """
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
    """
    It creates a dicctionary with the desired information for each review with 
    its five keys fullfilled, so we can create a data frame from it.
    Arg:
        lista (list): the list of lists containing the cleanned reviews with 
    its five keys fullfilled
    Returns:
        A dictionary containing the elements of each review with 
        its five keys fullfilled
    """
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
    """
    It creates a dicctionary with the desired information for each review with 
    some of its keys in blank, so we can create a data frame from it.
    Arg:
        lista (list): the list of lists containing the cleanned reviews
        with some of its keys in blank
    Returns:
        A dictionary containing the elements of each review with 
        some of its keys in blank
    """
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
    """
    It erases 23.6% of the rows randomly chosen.
    Arg:
        df (pandas DataFrame): the data frame with extra rows
    Returns:
        The original data frame with 23.6% of the rows deleted
    """
    num_remove = int((len(df['fecha']) * 23.6) //100)
    drop_tourist = np.random.choice(df.index, num_remove, replace=False)
    df = df.drop(drop_tourist)
    return df

def values_sin_espacios(df):
    """
    It takes away the extra spaces at the begining and end of the values
    Arg:
        df (pandas DataFrame): a data frame with extra spaces in its values
    Returns:
        The data frame cleaned from undesirable spaces
    """
    for i in df.columns:
        df[i] = df[i].str.strip()
    return df

def date_time(df):
    """
    It transforms the column containing dates into date-time format
    Arg:
        df (pandas DataFrame): a data frame with a date column needed to be clean
    Returns:
        The data frame with the column containing dates into date-time format
    """
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

# FUNCTIONS TO GENERATE DATA FRAMES FOR VISUALIZATION

def total_civitatis_tourists_month(df_civitatis_clean):
    """
    It shows the number of tourists grouped by month and saves it in pickle format
    Arg:
        df_civitatis_clean (pandas DataFrame): The data frame with all the reviews by day
    Returns:
        A data frame with the number of tourist by month
    """
    df_turistas_fecha = df_civitatis_clean.set_index('fecha')
    df_numero_turistas_fecha = df_turistas_fecha.groupby([(df_turistas_fecha.index.year),(df_turistas_fecha.index.month)]).count()
    df_numero_turistas_fecha = df_numero_turistas_fecha.drop(['procedencia', 'opinion', 'viajo_con'], axis=1).rename(columns={'nombre':'numero_turistas'})
    df_turistas_civitatis = df_numero_turistas_fecha.to_pickle(r'C:\Users\mituc\Ironhack\Curso\IronLabs\Proyecto-1\data\numero_turistas_fecha.pkl')
    return df_turistas_civitatis

def admon_cividates(df_turistas_admon):
    """
    It selects the total number of tourists for the dates we'll be analyzing
    Arg:
        df_turistas_admon (pandas DataFrame): the complete dataframe from the goverment
    Returns:
        A data frame with the total number of tourists by month for the desired dates
    """
    df_turistas_admon.reset_index(inplace=True)
    df_admon_select = df_turistas_admon.iloc[1:56]
    d=df_admon_select.sort_values(by=['periodo'])
    d=d.drop(['viajeros_espana', 'viajeros_extranjero',	'pernoctaciones_espana', 'pernoctaciones_extranjero',	'media_pernoc_esp', 'media_pernoc_ext', 'total_pernoctaciones',	'media_total_pernoc'],axis=1)
    df_admon_cividates = d.to_pickle(r'C:\Users\mituc\Ironhack\Curso\IronLabs\Proyecto-1\data\admon_cividates.pkl')
    return df_admon_cividates