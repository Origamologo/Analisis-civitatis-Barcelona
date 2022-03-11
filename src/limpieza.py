def pastor_de_guiris(df, ciudad):
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

    guiris_esquilados['media_pernoc_esp'] = df_pernocguiris_esp['total'] / df_numguiris_esp['total']
    guiris_esquilados['media_pernoc_ext'] = df_pernocguiris_ext['total'] / df_numguiris_ext['total']
    guiris_esquilados['total_viajeros'] = df_numguiris_esp['total'] + df_numguiris_ext['total']
    guiris_esquilados['total_pernoctaciones'] = df_pernocguiris_esp['total'] + df_pernocguiris_ext['total']
    guiris_esquilados['media_total_pernoc'] = guiris_esquilados['total_pernoctaciones'] / guiris_esquilados['total_viajeros']

    guiris_esquilados.to_pickle(f'{ciudad}_guiris_esquilados.pkl')
    return guiris_esquilados