"""
El siguiente archivo almacena las funciones utilizadas en el archivo main
"""



def ajustar_long(x):
    if str(x)[1:2]=='9' or str(x)[1:2]=='8':
        return float(str(x)[:3]+'.'+str(x)[3:])
    elif str(x)[1:2]=='1':
        return float(str(x)[:4]+'.'+str(x)[4:])
    else:
        return(-1)

##Es necesaria la correccion ya que es nuestro identificador
##en el mapa con ayuda de plotly
def corregir_nombre_estados(x):
    if x=='MichoacÃ¡n':
        return 'Michoacán'
    elif x=='Distrito Federal':
        return 'Ciudad de México'
    elif x=='MÃ©xico':
        return 'México'
    elif x=='Nuevo LeÃ³n':
        return 'Nuevo León'
    elif x=='San Luis PotosÃ\xad':
        return 'San Luis Potosí'
    elif x=='YucatÃ¡n':
        return 'Yucatán'
    elif x=='QuerÃ©taro':
        return 'Querétaro'
    else:
        return x
