# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:05:29 2022

@author: VicBoxMS
"""
from funciones import *
import numpy as np
import pandas as pd
import string

ruta = 'C:\\Users\\Victor\\Documents\\18semestre\\Entrevistas de Trabajo\\AplicacionBANORTE\\'
df = pd.read_excel(ruta+'indicadores_geo.xlsx')

#Corregir el nombre de los estados
df['entidad_federativa'] = df['entidad_federativa'].apply(corregir_nombre_estados)

#
df['lat']=df['lat'].apply(lambda x: str(x).replace('.',''))
df['long']=df['long'].apply(lambda x: str(x).replace('.',''))

df['lat']=df['lat'].apply(lambda x: float(str(x)[:2]+'.'+str(x)[2:]))



df['long']=df['long'].apply(ajustar_long)
df.to_excel(ruta+'doc_procesado.xlsx')

rubro_pobreza = ['pobreza','pobreza_e','pobreza_m']
rubro_carencias = ['vul_car','vul_ing','carencias','carencias3',
                   'plb','plbm']
rubro_salud = ['ic_asalud','ic_segsoc']
rubro_educación = ['ic_rezedu']
rubro_vivienda = ['ic_cv','ic_sbv','ic_ali']

##Pca de SKLEARN
X_rubro_pobreza = df[rubro_pobreza]

from sklearn.decomposition import PCA
pca = PCA(n_components=1)
pca.fit(X_rubro_pobreza)
entidades = pd.DataFrame(df['entidad_federativa'])
primer_componente = pd.DataFrame(pca.transform(X_rubro_pobreza))
df_r_pobreza = pd.concat([entidades,primer_componente],axis=1)
df_r_pobreza = df_r_pobreza.groupby(by='entidad_federativa').median()
###Mapas
##Mapa con plotly-express
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import requests
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import requests

pio.renderers.default='browser'
repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
#Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()

###For para obtener los diferentes mapas
#,
rubros = [rubro_pobreza,rubro_carencias,rubro_salud, rubro_vivienda,rubro_educación]


nombres = ['<b>Indice asociado al rubro pobreza</b>',
           '<b>Indice asociado al rubro Social y Economico</b>',
           '<b>Indice asociado al rubro salud</b>',
           '<b>Indice asociado al rubro vivienda</b>',
           '<b>Indice asociado al rubro educación</b>']

colores = ["Blues","Oranges","ylorbr","turbid","Greys"]
#Darkmint

from PIL import Image
imagenes =[ruta+'moneda.jpg',
           ruta+'moneda.jpg',
           ruta+'salud.png',
           ruta+'vivienda.png',
           ruta+'educacion.png']

pio.renderers.default='browser'
repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
#Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()

for contador, i in enumerate(rubros):
    X_rubro_pobreza = df[i]
    pca = PCA(n_components=1)
    entidades = pd.DataFrame(df['entidad_federativa'])
    primer_componente = pd.DataFrame(pca.fit_transform(X_rubro_pobreza))
    primer_componente = X_rubro_pobreza@pca.components_.T
    if np.sum(pca.components_<0)==len(i):
        primer_componente *= -1
        print(pca.components_*-1)
    else:
        print(pca.components_)
    primer_componente_escalado = 100*((primer_componente)/np.max(primer_componente))
    df_r_pobreza = pd.concat([entidades,primer_componente_escalado],axis=1)
    df_r_pobreza = df_r_pobreza.groupby(by='entidad_federativa').median()
    df_r_pobreza = df_r_pobreza.rename(columns={0:'Porcentaje'})
    ###Mapas
    ##Mapa con plotly-express
    fig = px.choropleth(data_frame=df_r_pobreza,
                        geojson=mx_regions_geo,
                        locations=df_r_pobreza.index, # nombre de la columna del Dataframe
                        featureidkey='properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                        color=df_r_pobreza['Porcentaje'], #El color depende de las cantidades
                        color_continuous_scale=colores[contador],
                       )
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    if contador>0:
        pyLogo = Image.open(imagenes[contador])
        fig.add_layout_image(
            dict(
                source=pyLogo,
                xref="paper", yref="paper",
                x=0.25, y=0.1,
                sizex=0.3, sizey=0.3,
                xanchor="right", yanchor="bottom"
            ))
#    fig.update_layout(
#                title={
#                'text' : nombres[contador],
#                'x':0.5,
#                'xanchor': 'center'
#            })
    fig.update_layout(
        title=dict(
            text=nombres[contador],
            x=0.5,
            y=0.95,
            font=dict(
                family="Arial",
                size=33,
                color='#000000'
            )))
    fig.show()


#Todos los rubros

todos = (rubro_pobreza+rubro_carencias+rubro_salud +
        rubro_vivienda+rubro_educación)
X_rubro_pobreza = df[todos]
pca = PCA(n_components=1)
entidades = pd.DataFrame(df['entidad_federativa'])
primer_componente = pd.DataFrame(pca.fit_transform(X_rubro_pobreza))
primer_componente = X_rubro_pobreza@pca.components_.T
primer_componente = 100*primer_componente/np.max(primer_componente)
df_r_pobreza = pd.concat([entidades,primer_componente],axis=1)
df_r_pobreza = df_r_pobreza.groupby(by='entidad_federativa').median()
print(pca.components_)
###Mapas
##Mapa con plotly-express
pio.renderers.default='browser'
repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
#Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()


fig = px.choropleth(data_frame=df_r_pobreza,
                    geojson=mx_regions_geo,
                    locations=df_r_pobreza.index, # nombre de la columna del Dataframe
                    featureidkey='properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    color=df_r_pobreza[0], #El color depende de las cantidades
                    color_continuous_scale="Darkmint",
                   )
fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
        xref="paper", yref="paper",
        x=1, y=0.99,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom"
    ))

fig.update_layout(
    title=dict(
        text='<b>Indice a partir de la metodología PCA utilizando todas todas las variables</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='#000000'
        )))
fig.show()


#De nuestro analisis de componentes principales, tenemos que las dos
#variables que no van en el mismo sentido que las demas son
#
#al analizarlas detenidamente nos damos cuenta que si las graficamos y
#hacemos una tabla independiente de ella, se comporta de manera diferente,
# puesto que indica que en los estados como '', tienen el menor numero






todos = (rubro_pobreza+rubro_carencias+rubro_salud +
        rubro_vivienda+rubro_educación)
X_rubro_pobreza = df[todos]
pca = PCA(n_components=1)
entidades = pd.DataFrame(df['entidad_federativa'])
primer_componente = pd.DataFrame(pca.fit_transform(X_rubro_pobreza))
primer_componente = X_rubro_pobreza@pca.components_.T
primer_componente = 100*primer_componente/np.max(primer_componente)
df_r_pobreza = pd.concat([entidades,primer_componente],axis=1)
df_r_pobreza = df_r_pobreza.groupby(by='entidad_federativa').median()



#3    vul_car
#4    vul_ing
#9  ic_asalud

total_ic_asalud = df[['entidad_federativa','ic_asalud']].groupby(by='entidad_federativa').median()
total_vul_car = df[['entidad_federativa','vul_car']].groupby(by='entidad_federativa').median()
total_vul_ing = df[['entidad_federativa','vul_ing']].groupby(by='entidad_federativa').median()

total_ic_asalud
total_vul_car
total_vul_ing


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

matriz_correlacion = df[todos].corr()

plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(matriz_correlacion.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12);# save heatmap as .png file
# dpi - sets the resolution of the saved image in dots/inches
# bbox_inches - when set to 'tight' - does not allow the labels to be cropped

plt.figure(figsize=(14, 6))
mask = np.triu(np.ones_like(matriz_correlacion.corr(), dtype=np.bool))
heatmap = sns.heatmap(matriz_correlacion.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Triangulo de Correlación', fontdict={'fontsize':18}, pad=16);






total_ic_asalud_reset = total_ic_asalud.reset_index()
total_vul_car_reset = total_vul_car.reset_index()
total_vul_ing_reset = total_vul_ing.reset_index()

total_ic_asalud_reset = total_ic_asalud_reset.rename(columns={'ic_asalud':'ic'})
total_vul_car_reset = total_vul_car_reset.rename(columns={'vul_car':'ic'})
total_vul_ing_reset = total_vul_ing_reset.rename(columns={'vul_ing':'ic'})



df_barplot= pd.concat([total_ic_asalud_reset,total_vul_car_reset,total_vul_ing_reset],axis=0,ignore_index=True)
hu = pd.DataFrame(np.repeat(['ic_asalud','vul_car','vul_ing'],32))
df_barplot_hue = pd.concat([df_barplot,hu],axis=1)
ranks = df_barplot_hue.groupby('entidad_federativa')['ic'].sum().fillna(0).sort_values()[::-1].index

a4_dims = (7, 7.5)
fig, ax = plt.subplots(figsize=a4_dims)
sns.set_theme(style="whitegrid")
ax = sns.barplot(x="ic", y="entidad_federativa", hue=0, data=df_barplot_hue,order =ranks)
ax.set(xlabel='Porcentaje', ylabel='Entidad Federativa')
plt.title("Porcentaje Reportado Para Las Variables ic_asalud, vul_car y vul_ing")
