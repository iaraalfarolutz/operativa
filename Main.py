import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Leemos los dataset Originales
df = pd.read_csv('Resources/ExamenesOriginales.csv')
#dfSist = pd.read_csv('Resources/CodigosSistemas.csv')
dfRur = pd.read_csv('Resources/CodigosRural.csv')
dfInd = pd.read_csv('Resources/CodigosIndustrial.csv')

# Eliminamos duplicados
dfInd = dfInd.drop_duplicates(['plan', 'materia'])
dfRur = dfRur.drop_duplicates(['plan', 'materia'])
#dfSist = dfSist.drop_duplicates(['plan', 'materia'])
#Eliminamos materias sin nombre
#dfSist = dfSist[dfSist.nombre_de_ != '']
dfRur = dfRur[dfRur.nombre_de_ != '']
dfInd = dfInd[dfInd.nombre_de_ != '']
dfInd=dfInd.dropna(subset=['nombre_de_'])
#dfSist=dfSist.dropna(subset=['nombre_de_'])
dfRur=dfRur.dropna(subset=['nombre_de_'])

#Saco optativas de la tabla general para poder ver mas claro cuales estan recibidos
dfElec = df[df['nombre_de_'].str.contains("Elec.", regex=False) | df['nombre_de_'].str.contains("electiva", regex=False) | df['nombre_de_'].str.contains("elect.", regex=False)]
cond = df['nombre_de_'].isin(dfElec['nombre_de_'])==True
df.drop(df[cond].index)
#Deberiamos dejar la df limpia? Osea con las optativas, y tratar con otra tabla

#Eliminamos los ausentes del dataset original y los guardamos en otro para que no afecte el promedio, y tambien poder sacar metricas de los ausentes
dfAu = df[df.nota == "Au"]
df = df[df.nota != "Au"]
dfAu.to_csv("Resources/Ausentes.csv")

# Agregado de Columnas Necesarias
df['Carrera'] = 'Indeterminado'  # Inicializo con indeterminada a la carrera por si solo ha rendido materias que son compartidas entre las 3.
df['Recibido'] = False

df.loc[df.nota == 'In', 'nota'] = 2  # consideramos que In es de Insuficiente y le asignamos un 2
df.loc[df.nota == 'Ap', 'nota'] = 4  # Consideramos que Ap sigifica aprobado con 4#
df.loc[df.nota == 'So', 'nota'] = 10  # Consideramos que So sigifica aprobado con 10 por sobresaliente#
df.loc[df.nota == 'Na', 'nota'] = 2  # Consideramos que Na sigifica no aprobado con 2#


#Luego de reemplazar los valores no numéricos, cambiamos el tipo de la columna a numérico para poder usar las funciones de promedio y eso.
df['nota'] = pd.to_numeric(df['nota'])

#en unas variables auxiliares tomamos en cuenta solo los códigos de materia de cada carrera
materiaRurAUX = dfRur.drop_duplicates(['materia'])
materiaIndAUX = dfInd.drop_duplicates(['materia'])
#materiaSistAUX = dfSist.drop_duplicates(['materia'])

#obtenemos los codigos de materias distintivos de cada carrera realizando la intersección de los datasets.
materiaRur = materiaRurAUX.drop(materiaRurAUX[materiaRurAUX['materia'].isin(materiaIndAUX['materia'])].index ) #| materiaRurAUX[materiaRurAUX['materia'].isin(materiaSistAUX['materia'])].index)

#materiaSist = materiaSistAUX.drop(materiaSistAUX[materiaSistAUX['materia'].isin(materiaRurAUX['materia'])].index | materiaSistAUX[materiaSistAUX['materia'].isin(materiaIndAUX['materia'])].index)

materiaInd = materiaIndAUX.drop(materiaIndAUX[materiaIndAUX['materia'].isin(materiaRurAUX['materia'])].index) # | materiaIndAUX[materiaIndAUX['materia'].isin(materiaSistAUX['materia'])].index)

#Aca tenemos un problema, los codigo de materia no son todos iguales

#print (materiaRur)
#print (materiaSist)
#print (materiaInd)

#Usando las materias distintivas asignamos a los alumnos la carrera a la que pertenecen.
cond_industrial = df['nombre_de_'].isin(materiaInd['nombre_de_']) == True
#cond_sistemas = df['materia'].isin(materiaSist['materia']) == True
cond_rural = df['nombre_de_'].isin(materiaRur['nombre_de_']) == True
df.loc[cond_rural, 'Carrera'] = 'Administracion Rural'
df.loc[cond_industrial, 'Carrera'] = 'Ingenieria Industrial'
#df.loc[cond_sistemas, 'Carrera'] = 'Ingenieria de Sistemas'


#usando las carreras asignadas para el alumno en cada fila del alumno le asignamos la carrera
#(esto tiene sentido para saber cuantas filas nos quedaron sin carrera y para mas adelante)
dfCarreraAsignada = df[df.Carrera != "Indeterminado"]
dfCarreraAsignada = dfCarreraAsignada.drop_duplicates(['legajo']) # Esto hace cagada porque hay varios con distintas carreras
for index, row in dfCarreraAsignada.iterrows():
    df.loc[df['legajo'] == row['legajo'], 'Carrera'] = row['Carrera']
#Revisar lo de arriba porque si lo comentamos da en algunas una carrera y en otras otras
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
dfRur95 = dfRur95.drop(dfRur95[cond].index)
cond = dfRur03['nombre_de_'].isin(dfRur03Elec['nombre_de_'])==True
dfRur03 = dfRur03.drop(dfRur03[cond].index)

#Busco optativas de Industrial
dfInd95 = dfInd[dfInd.plan == 95]
dfInd03 = dfInd[dfInd.plan == 2003]
dfInd07 = dfInd[dfInd.plan == 2007]

dfInd95Elec = dfInd95[dfInd95['nombre_de_'].str.contains("Elec.", regex=False) | dfInd95['nombre_de_'].str.contains("electiva", regex=False)]
dfInd03Elec = dfInd03[dfInd03['nombre_de_'].str.contains("Elec.", regex=False) | dfInd03['nombre_de_'].str.contains("electiva", regex=False)]
dfInd07Elec = dfInd07[dfInd07['nombre_de_'].str.contains("Elec.", regex=False) | dfInd07['nombre_de_'].str.contains("electiva", regex=False)]

#Dejo en industrial solo las obligatorias

cond = dfInd95['nombre_de_'].isin(dfInd95Elec['nombre_de_'])==True
dfInd95 = dfInd95.drop(dfInd95[cond].index)
cond = dfInd03['nombre_de_'].isin(dfInd03Elec['nombre_de_'])==True
dfInd03 = dfInd03.drop(dfInd03[cond].index)
cond = dfInd07['nombre_de_'].isin(dfInd07Elec['nombre_de_'])==True
dfInd07 = dfInd07.drop(dfInd07[cond].index)



df['plan'] = 0

df.loc[df['ingr'] < 2003, 'plan'] = 1995
df.loc[df['ingr'] >= 2003, 'plan'] = 2003
cond = ((df['ingr'] >= 2007) & (df['Carrera']=="Ingenieria Industrial"))
df.loc[cond, 'plan'] = 2007

dfNMat = df.groupby('legajo').agg({'nota': 'count',
                                   'plan': 'mean',
                                   'Carrera': 'first',
                                   'ingr': 'first'})

dfNNMat = df[df.nota >= 4].groupby('legajo').agg({'nombre_de_': 'count'})
#Arreglar variables
#Esto anda, hace el join que da como resultado una tabla con el alumno, la cantidad de materias que rindio, y la cantidad que aprobo
dfJMat = pd.merge(dfNMat, dfNNMat, on='legajo', how='outer')

#Eliminamos los indeterminados
cond = dfJMat['Carrera'].str.contains("Indeterminado", regex=False)
dfJMat = dfJMat.drop(dfJMat[cond].index)

#Guardamos en variables la cantidad de materias obligatorias de cada plan
cantRur95 = len(dfRur95)
cantRur03 = len(dfRur03)
cantInd95 = len(dfInd95)
cantInd03 = len(dfInd03)
cantInd07 = len(dfInd07)

print([cantInd95, cantInd03,cantInd07, cantRur95, cantRur03])
#print(dfJMat)
#creo columna recibido y elimino los nan
dfJMat['recibido'] = False
dfJMat.fillna(0, inplace=True)

dfJMat.rename(columns = {'nombre_de_': 'aprobados',
                         'nota': 'total'},
                          inplace=True)

def aprobados(x):
    if x['Carrera'] == "Ingenieria Industrial":
        if x['plan'] == 1995:
            if x['aprobados'] == cantInd95:
                return True
            else:
                return False
        else:
            if x['aprobados'] == cantInd03:
                return True
            else:
                return False
    else:
        if x['plan'] == 1995:
            if x['aprobados'] == cantRur95:
                return True
            else:
                return False
        else:
            if x['aprobados'] == cantRur03:
                return True
            else:
                return False

#dfJMat['recibido'] = dfJMat.apply(aprobados, axis=1)

df_alumnos_recibidos = df[(df['nombre_de_']== "Proyecto Final") | (df['nombre_de_']== "Seminario Final" )]
df.loc[df['legajo'].isin(df_alumnos_recibidos['legajo']), 'Recibido'] = True
alumnos_recibidos_count = len(df[df['nombre_de_'] == "Proyecto Final"].groupby('legajo').count())

#print(alumnos_recibidos_count)

#Promedio por alumno
df_avg_alumnos = df.groupby('legajo').agg({'nota': 'mean',
                                        'Recibido': 'first'})

dfJMat = pd.merge(dfJMat, df_avg_alumnos, on='legajo', how='inner')
dfJMat.rename(columns = {'nota': 'promedio'}, inplace=True)
########################### PARA HACER EL DE MATERIA

#dfMatMean = df.groupby('nombre_de_').agg({'nombre_de_' : 'first',
#                                          'nota': 'mean',
#                                          'plan': 'mean',
#                                          'Carrera': 'first'})

#dfMatMean.rename(columns = {'nombre_de_': 'Materia',
#                         'nota': 'promedio'},
#                          inplace=True)
#print(dfMatMean)

#cond = dfMatMean['Carrera'].str.contains("Indeterminado", regex=False)
#dfMatMean = dfMatMean.drop(dfMatMean[cond].index)

#sns.relplot(x='promedio', y='Materia', data=dfMatMean, hue="Carrera", size="plan")



dfTotal = df[df.Carrera != "Indeterminado"]
#cond = dfTotal['Carrera'].str.contains("Indeterminado", regex=False)
#dfTotal = dfTotal.drop(dfTotal[cond].index)

dfTotal = dfTotal.groupby('nombre_de_').agg({'nota': 'mean',
                                        'plan': 'first',
                                        'nombre_de_': 'first',
                                        'Carrera': 'first'})
dfTotal = dfTotal.sort_values(by=['nota'])
dfTotal = dfTotal.head(20)
print(dfTotal)

sns.relplot(x="nota", y="nombre_de_", hue="Carrera", data=dfTotal, size="plan")

plt.show()











#Intento de grafico de dispersion usando seaborn carrera notas en tiempo
#sns.set(style="darkgrid")
#sns.relplot(x='aprobados', y='promedio', data=dfJMat, hue="Carrera", style="Recibido", size="plan")

#plt.show()

#sns.relplot(x='aprobados', y='ingr', data=dfJMat, hue="Carrera", style="Recibido", size="plan")

#plt.show()

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