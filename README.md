# Sistema de recomendaciones de Peliculas

## Proyecto individual de Machine Learning 

### Descripcion 
Este proyecto tiene como objetivo desarrollar un modelo de ML que consista en un sistema de recomendaciones de peliculas. El modelo sugerirà a los usuarios peliculas similares a las que buscaron.

- Descripcion 
- Instalación y Requisitos
- Estructura del Proyecto
- Uso y Ejecución
- Datos y Fuentes
- Metodología
- Resultados y Conclusiones
- Contribución y Colaboración
- Licencia

### Instalación y Requisitos
##### Requisitos
- Python
- pandas
- numpy
- scikit-learn
- seaborn
- matplotlib
- wordcloud
- ast 
- datetime
- warnings
- missingno
- autoviz
- DataWrangler
- Counter
- fastapi
- uvicorn

##### Instalación
Instalaremos un ambiente virtual para tener un entorno seguro y facil de usar para los demas usuarios: 
Crear el entorno: 

    python -m venv venv
Activar el entorno:

    venv\Scripts\activate**

Instalar las dependencias

	pip install -r requirements.txt

### Estructura del Proyecto
**data/** : Contiene los archivos de datos utilizados en el proyecto.
**notebooks/** : Incluye los notebooks de Jupyter con el análisis y modelos.
**src/** : Código fuente del proyecto, incluyendo scripts y módulos.
**reports/** : Guarda los informes y visualizaciones generados.
**README.md** : Archivo de documentación del proyecto.
**requirements.txt** : librerias e instalaciones

### Datos y Fuentes
Los datos utilizados provienen de dos csv proporcionados por el proyecto, que no se han incluido en el GitHub por motivos de memoria y almacenamiento. En cambio se subieron los csv limpios(transformados) con los que se pasaron las info al sistema de recomendacion. 
Estos se encuentran en la carpeta **data/**.

### Metodologia
Arrancamos con una fase explorativa de los datos para analizar el dataset considerando nuestro contexto .

A seguir la fase de **ETL** , durante la cual se hicieron las transformaciones necesarias para limpiar los datos y guardarlos en un nuevo CSV mas lejible.

Despues de las adecuadas transformaciones se crearon las funciones para los endpoints que se consuman en la API a traves de FastApi, y se guardaron en un file llamado **main.py**, cada una con su decorador  **(@app.get(‘/’))**.

Una vez todo funcione en FastApi, seguimos con la fase de deployment en la cual se suben los archivos a Render para que la API pueda ser consumida desde la web.
> > ***Mas info sobre Render*** ..
1. Crear una cuenta en Render
2. Elegir la opción *Web Service*
3. Ir al apartado que se encuentra abajo de Public Git repository. Copiar y pegar el enlace del repositorio (tiene que ser público).
4. Llenar los campos necesarios. En branch seleccionar main. 
Runtime tiene que ser Python 3.
5. En Build Command y Start command, respectivamente, poner:

      pip install -r requirements.txt 
	  uvicorn main:app --host 0.0.0.0 --port 10000

> Seleccionar la opción Create Web Service
- Una vez terminados los pasos anteriores, se va a comenzar a cargar nuestra aplicación. Puede tardar unos minutos.




Con el nuevo dataset se procediò a la fase exploratoria **EDA** .
Esta etapa incluyo:
- descripción de las estadísticas básicas.
- revisión de los tipos de datos y valores faltantes
-  identificaciòn de outliers
- distribución de las variables
- relaciones entre variables
- patrones y tendencias
- análisis de texto (como nubes de palabras) para títulos u otros campos textuales.

Al final del EDA, se uso tambien la visualización automatizada como comprobacion y suporte en la eleccion de los graficos mas significativos.
Terminando esta fase, se decidiò crear un nuevo dataset contenente solo las columnas necesarias para hacer funcionar nuestro modelo.

En la ultima fase se creo un nuevo file.py, donde se uso el metodo 

    train_test_split

para entrenar nuestro modelo con los datos a disposicion (despues de vectorizar las variables) y se aplicò la funcion coseno para encontrar las similitudes entre las peliculas.
Finalmente se creò la funcion para la api del sistema de recomendacion. 

> En el archivo main.py, guardamos solo los endpoints, mientras que las funciones seran importadas desde sus files.py (exactamente como hariamos al importar una libreria: 

    from nombre_file.py import nombre_funcion)

Despues de deployar esta ultima API  se puede comprobar que todo funcione correctamente.

### Resultados y Conclusiones
- Nuestro modelo de recomendacion està listo para consumirse en la web: al inserir el titulo de una pelicula que estè presente en nuestro dataset, nos devuelve una lista de 5 peliculas basadas en un score de similaridad.
Esto podria ayudar el usuario a elegir  las peliculas basandose en sus intereses.

### Autores:
Este proyecto fue realizado por:
**Giada De Carlo** 
