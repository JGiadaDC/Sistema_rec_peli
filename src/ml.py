import pandas as pd
import calendar
import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


df1 = pd.read_csv('data/movie_rec.csv')

# Vectorizzazione TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df1['title'])

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df1['production_companies'])

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df1['genres'])

df1['overview'].fillna('', inplace=True)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df1['overview'])

X = df1.drop(columns = ['title'])
y = df1['title']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) #random


cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Creare una serie con gli indici dei titoli dei film
indices = pd.Series(df1.index, index=df1['title']).drop_duplicates()
indices = {row['title'].lower(): idx for idx, row in df1.iterrows()}


#crear la api de una funcion para el sistema de recomendacion
def recomendar(titulo: str):
    titulo_lower = titulo.lower()
    # Obtener el index
    idx = indices[titulo]
    
    # Obtener vector de similaridad
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordenar peliculas con el score de similaridad
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener puntaje peliculas similares
    sim_scores = sim_scores[1:6]
    
    # Obtener indices
    movie_indices = [i[0] for i in sim_scores]
    
    # Restituir titulos
    recomendacion = df1['title'].iloc[movie_indices].tolist()

    return(recomendacion)
