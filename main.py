from fastapi import FastAPI, HTTPException
import pandas as pd
from datetime import date
import calendar
import logging
import numpy as np
from src.ml import recomendar


app = FastAPI()

df = pd.read_csv('data/clean_movies.csv')
    
#hay que poner el autosave en vsc code para que se pueda ejecutar la API!!!!

#http://127.0.0.1:5000/
# http://127.0.0.1:8000

@app.get("/mes/{mes}")
def cantidad_filmaciones_mes(mes:str):
    df['release_date']= pd.to_datetime(df['release_date'],format= '%Y-%m-%d')
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
    if mes.lower() not in meses:
        raise ValueError("El mes proporcionado no es válido")
    mes_numero = meses[mes.lower()]
    filmaciones_mes = df[df['release_date'].dt.month == mes_numero]
    return f'{len(filmaciones_mes)} cantidad de películas fueron estrenadas en el mes de {mes}'


@app.get("/dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    try:
        # Mappiamo i nomi dei giorni in spagnolo ai nomi dei giorni in inglese
        dias = {
            'lunes': 'Monday', 
            'martes': 'Tuesday', 
            'miércoles': 'Wednesday', 
            'jueves': 'Thursday', 
            'viernes': 'Friday', 
            'sábado': 'Saturday', 
            'domingo': 'Sunday' 
        }

        # Controlliamo se il giorno inserito è presente nel dizionario
        if dia.lower() not in dias:
            raise HTTPException(status_code=400, detail=f"Día '{dia}' no reconocido. Por favor, ingrese un día válido en español.")
        
        # Convertiamo la colonna 'release_date' in tipo datetime
        df['release_date'] = pd.to_datetime(df['release_date'])
        
        # Troviamo il numero di film usciti il giorno specificato
        day_of_week = dias[dia.lower()]
        filmaciones_dia = df[df['release_date'].dt.day_name() == day_of_week]

        # Costruiamo e restituiamo il messaggio di ritorno
        return {
            "message": f"En total, {len(filmaciones_dia)} películas fueron estrenadas en el día {dia}"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@app.get("/titulo/{titulo}")
def score_titulo(titulo_de_la_filmación):
    # Cerca il film nel DataFrame
    movie = df[df['title'].str.lower() == titulo_de_la_filmación.lower()]
    
    if movie.empty:
        return f"No se encontró ninguna película con el título '{titulo_de_la_filmación}'."
    
    # Estrae le informazioni dal DataFrame
    movie_info = movie.iloc[0]
    titulo = movie_info['title']
    año_estreno = movie_info['release_year']
    score = movie_info['vote_average']
    
    # Costruisce il messaggio di ritorno
    mensaje = f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score/popularidad de {score}."
    return mensaje

@app.get("/votos/{titulo}")
def votos_titulo(titulo: str):
    # Cerca il film nel DataFrame
    movie = df[df['title'].str.lower() == titulo.lower()]
    
    if movie.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró ninguna película con el título '{titulo}'.")

    # Estrae le informazioni dal DataFrame
    movie_info = movie.iloc[0]
    titulo = movie_info['title']
    vote_count = movie_info['vote_count']
    vote_average = movie_info['vote_average']
    
    # Verifica se ci sono almeno 2000 valoraciones
    if vote_count < 2000:
        return f"La película '{titulo}' no cumple con la condición de tener al menos 2000 valoraciones."
    
    # Costruisce il messaggio di ritorno
    mensaje = f"La película '{titulo}' fue estrenada en el año {movie_info['release_year']}. " \
              f"La misma cuenta con un total de {vote_count} valoraciones, con un promedio de {vote_average}."
    return mensaje


@app.get("/actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    #convertimos el nombre en minuscolas
    nombre_actor_lower = nombre_actor.lower()
    # Lista para guardar las peli donde el actor participo
    filmaciones_actor = []

    # Cerca l'attore nel DataFrame
    for idx, row in df.iterrows():
        #convertimos los nombres de la lisat in minuscolas
        cast_lower = [actor.strip().lower() for actor in row['cast'].split(',')]
        if nombre_actor_lower in cast_lower:
            filmaciones_actor.append(row)

    if not filmaciones_actor:
        raise HTTPException(status_code=404, detail=f"No se encontró al actor '{nombre_actor}' en ninguna película.")

    # Calcola il numero di film in cui ha partecipato l'attore
    cantidad_filmaciones = len(filmaciones_actor)
    
    # Calcola il ritorno totale e medio per film
    total_return = sum([film['return'] for film in filmaciones_actor])
    promedio_return = total_return / cantidad_filmaciones if cantidad_filmaciones > 0 else 0

    # Costruisce il messaggio di ritorno
    mensaje = f"El actor '{nombre_actor}' ha participado en {cantidad_filmaciones} filmaciones. " \
              f"Ha conseguido un retorno total de {total_return} con un promedio de {promedio_return} por filmación."
    
    return {"mensaje": mensaje}


@app.get("/director/{nombre_director}")
def get_director(nombre_director: str):
    # Filtra il DataFrame per trovare i film diretti dal regista specificato
    director_movies = df[df['crew_clean'].str.contains(nombre_director, case=False, na=False)]
    
    if director_movies.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró al director '{nombre_director}' en ninguna película.")
    
    # Calcola il ritorno totale e medio
    total_return = director_movies['return'].sum()
    total_movies = len(director_movies)
    
    # Costruisci la risposta con le informazioni dettagliate per ogni film
    movies_info = []
    for _, row in director_movies.iterrows():
        movie_info = {
            'title': row['title'],
            'release_date': row['release_date'].strftime('%Y-%m-%d'),
            'return': row['return'],
            'budget': row['budget'],
            'revenue': row['revenue'],
            'profit': row['revenue'] - row['budget']
        }
        movies_info.append(movie_info)
    
    response = {
        'director': nombre_director,
        'total_return': total_return,
        'average_return': total_return / total_movies if total_movies > 0 else 0,
        'movies': movies_info
    }
    
    return response


@app.get("/recomendacion/{titulo}", response_model=list[str])
def get_recomendacion(titulo: str):
    recomendacion = recomendar(titulo)
    return(recomendacion)

