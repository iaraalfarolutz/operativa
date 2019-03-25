import pandas as pd

#HAY MUCHAS MATERIAS QUE NO ESTAN EN NINGUN PLAN VIEJO CHOTO.

df = pd.read_csv('Resources/ExamenesOriginales.csv')
dfSist = pd.read_csv('Resources/CodigosSistemas.csv')
dfRur = pd.read_csv('Resources/CodigosRural.csv')
dfInd = pd.read_csv('Resources/CodigosIndustrial.csv')

#Agregado de Columnas Necesarias
df['Carrera']=''
df['Recibido'] = 'Ndeah'


list = df

"""for index, row in df.iterrows():
    if(row['materia'] == 435):
        row['Carrera'] = 'Ingenieria industrial'
"""
df.loc[df.materia==435, 'Carrera'] = 'Ingenieria Industrial'
df.loc[df.nota == 'In' , 'nota' ] = 2  #consideramos que In es de Insuficiente y le asignamos un 2

#escritura en ExamenesProcesadosSalida
df.to_csv('Resources/ExamenesProcesadosSalida.csv')

#df.loc[df.materia in  , 'Carrera'] = 'Ingenieria Industrial'



#df['Carrera'] = df['esp']


'''
for row in df:
    if( row['materia'] == 435 ):
        row['Carrera'] = 'Ingeniería industrial'
'''





##print(df.groupby('legajo')['nota'].sum())
'''print(df)'''

#print(df['legajo'].count()) son lo mismo que el de abajo
#print(df.legajo.count())


#print(df.groupby('legajo').nota.sum())

#print(df.groupby('legajo').esp.mean())
#print(df.groupby('legajo').nota.mean())
# no anda porque como hay letras no detecta que sean de tipo numerico, primero vamos a tener que hacer tratamiento de eso, ver que con esp anda.



'''
for row in df:
        if df['nota'] == 'In' | df['nota'] == 'in':
            print('s')
        if df['nota'] == 'Au' | df['nota'] == 'au':
            print('s')
'''