import pandas as pd

#Leemos los dataset Originales
df = pd.read_csv('Resources/ExamenesOriginales.csv')
dfSist = pd.read_csv('Resources/CodigosSistemas.csv')
dfRur = pd.read_csv('Resources/CodigosRural.csv')
dfInd = pd.read_csv('Resources/CodigosIndustrial.csv')

# Eliminamos duplicados
dfInd = dfInd.drop_duplicates(['plan', 'materia'])
dfRur = dfRur.drop_duplicates(['plan', 'materia'])
dfSist = dfSist.drop_duplicates(['plan', 'materia'])
#Eliminamos materias sin nombre
dfSist = dfSist[dfSist.nombre_de_ != '']
dfRur = dfRur[dfRur.nombre_de_ != '']
dfInd = dfInd[dfInd.nombre_de_ != '']
dfInd=dfInd.dropna(subset=['nombre_de_'])
dfSist=dfSist.dropna(subset=['nombre_de_'])
dfRur=dfRur.dropna(subset=['nombre_de_'])


#Eliminamos los ausentes del dataset original y los guardamos en otro para que no afecte el promedio, y tambien poder sacar metricas de los ausentes
dfAu = df[df.nota == "Au"]
df = df[df.nota != "Au"]
dfAu.to_csv("Resources/Ausentes.csv")

# Agregado de Columnas Necesarias
df['Carrera'] = 'Indeterminado'  # Inicializo con indeterminada a la carrera por si solo ha rendido materias que son compartidas entre las 3.
df['Recibido'] = 'Ndeah'


df.loc[df.nota == 'In', 'nota'] = 2  # consideramos que In es de Insuficiente y le asignamos un 2
df.loc[df.nota == 'Ap', 'nota'] = 4  # Consideramos que Ap sigifica aprobado con 4#
df.loc[df.nota == 'So', 'nota'] = 10  # Consideramos que So sigifica aprobado con 10 por sobresaliente#
df.loc[df.nota == 'Na', 'nota'] = 2  # Consideramos que Na sigifica no aprobado con 2#

#Luego de reemplazar los valores no numéricos, cambiamos el tipo de la columna a numérico para poder usar las funciones de promedio y eso.
df['nota'] = pd.to_numeric(df['nota'])
#print(df['nota'].mean())

#en unas variables auxiliares tomamos en cuenta solo los códigos de materia de cada carrera
materiaRurAUX = dfRur.drop_duplicates(['materia'])
materiaIndAUX = dfInd.drop_duplicates(['materia'])
materiaSistAUX = dfSist.drop_duplicates(['materia'])

#obtenemos los codigos de materias distintivos de cada carrera realizando la intersección de los datasets.
materiaRur = materiaRurAUX.drop(materiaRurAUX[materiaRurAUX['materia'].isin(materiaIndAUX['materia'])].index ) #| materiaRurAUX[materiaRurAUX['materia'].isin(materiaSistAUX['materia'])].index)

#materiaSist = materiaSistAUX.drop(materiaSistAUX[materiaSistAUX['materia'].isin(materiaRurAUX['materia'])].index | materiaSistAUX[materiaSistAUX['materia'].isin(materiaIndAUX['materia'])].index)

materiaInd = materiaIndAUX.drop(materiaIndAUX[materiaIndAUX['materia'].isin(materiaRurAUX['materia'])].index) # | materiaIndAUX[materiaIndAUX['materia'].isin(materiaSistAUX['materia'])].index)


#print (materiaRur)
#print (materiaSist)
#print (materiaInd)

#Usando las materias distintivas asignamos a los alumnos la carrera a la que pertenecen.
cond_industrial = df['materia'].isin(materiaInd['materia']) == True
#cond_sistemas = df['materia'].isin(materiaSist['materia']) == True
cond_rural = df['materia'].isin(materiaRur['materia']) == True
df.loc[cond_industrial, 'Carrera'] = 'Ingenieria Industrial'
#df.loc[cond_sistemas, 'Carrera'] = 'Ingenieria de Sistemas'
df.loc[cond_rural, 'Carrera'] = 'Administracion Rural'

#usando las carreras asignadas para el alumno en cada fila del alumno le asignamos la carrera
#(esto tiene sentido para saber cuantas filas nos quedaron sin carrera y para mas adelante)
dfCarreraAsignada = df[df.Carrera != "Indeterminado"]
dfCarreraAsignada = dfCarreraAsignada.drop_duplicates(['legajo'])
for index, row in dfCarreraAsignada.iterrows():
    df.loc[df['legajo'] == row['legajo'], 'Carrera'] = row['Carrera']

dfindet = df[df.Carrera == "Indeterminado"]

#print (dfindet)
dfindet.to_csv("Resources/Indeterminados.csv")

#Busco optativas de Rural

dfRur95 = dfRur[dfRur.plan == 95]
dfRur03 = dfRur[dfRur.plan == 2003]

dfRur95Elec = dfRur95[dfRur95['nombre_de_'].str.contains("Elec.", regex=False) | dfRur95['nombre_de_'].str.contains("elect.", regex=False)]
dfRur03Elec = dfRur03[dfRur03['nombre_de_'].str.contains("Elec.", regex=False) | dfRur03['nombre_de_'].str.contains("elect.", regex=False)]

#Dejo en rural solo las obligatorias

cond = dfRur95['nombre_de_'].isin(dfRur95Elec['nombre_de_'])==True
dfRur95.drop(dfRur95[cond].index)
cond = dfRur03['nombre_de_'].isin(dfRur03Elec['nombre_de_'])==True
dfRur03.drop(dfRur03[cond].index)

#Busco optativas de Industrial
dfInd95 = dfInd[dfInd.plan == 95]
dfInd03 = dfInd[dfInd.plan == 2003]

dfInd95Elec = dfInd95[dfInd95['nombre_de_'].str.contains("Elec.", regex=False) | dfInd95['nombre_de_'].str.contains("electiva", regex=False)]
dfInd03Elec = dfInd03[dfInd03['nombre_de_'].str.contains("Elec.", regex=False) | dfInd03['nombre_de_'].str.contains("electiva", regex=False)]

#Dejo en industrial solo las obligatorias
cond = dfInd95['nombre_de_'].isin(dfInd95Elec['nombre_de_'])==True
dfInd95.drop(dfInd95[cond].index)
cond = dfInd03['nombre_de_'].isin(dfInd03Elec['nombre_de_'])==True
dfInd03.drop(dfInd03[cond].index)

#Saco optativas de la tabla general para poder ver mas claro cuales estan recibidos
dfElec = df[df['nombre_de_'].str.contains("Elec.", regex=False) | df['nombre_de_'].str.contains("electiva", regex=False) | df['nombre_de_'].str.contains("elect.", regex=False)]
cond = df['nombre_de_'].isin(dfElec['nombre_de_'])==True
df.drop(df[cond].index)


dfNMat = df.groupby('legajo').agg({'nota': 'count'})

dfNNMat = df[df.nota > 3].groupby('legajo').agg({'nombre_de_': 'count'})

#Esto anda, hace el join que da como resultado una tabla con el alumno, la cantidad de materias que rindio, y la cantidad que aprobo
dfNNNMat = pd.merge(dfNMat, dfNNMat, on='legajo', how='outer')
#print(dfNNNMat)

# df.loc[df['legajo'] == row['legajo'], 'Carrera'] = row['Carrera']

#print(df)

#escritura en ExamenesProcesadosSalida
df.to_csv('Resources/ExamenesProcesadosSalida.csv')


'''
Casi 4000 filas son indeterminado, vamos a tener que analizar por que:
hay filas de materias mal cargadas (materias que viendo su nombre sabemos que materia es pero que si numero de materia no existe en ningun plan.) dijo que las saquemos
Fisica con número 1
HAY 2 MATERIAS CON EL MISMO CODIGO PERO QUE SON DISTINTAS ?? 
MATERIA 125 EN INDUSTRIAL ES INFORMATICA Y EN SISTEMAS ES SISTEMAS Y ORGANIZACIONES
228 tambien està en sistemas y agronomìa
123 sistemas y agronomia
230 sistemas y agronomía

Posible opcion: ver que materias coinciden en número pero que son distintas y a alguna de las dos asignarle otro numero, tener cuidado y cambiar
tambien en el plan de estudios.


127 no está en ningun plan
Cualquier materia que empiece con 2000 algo no esta en ningín plan, que les hacemos ?
209 no esta


cualquier materia que no este en ningun plan la volamos porque pueden ser de tecnicaturas o otra cosa
'''