from fastapi import FastAPI, HTTPException
import pandas as pd
from datetime import date
import calendar
import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


app = FastAPI()

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



#crear la api de una funcion para el sistema de recomendacion
def recomendar(titulo: str):
    # Ottieni l'indice del film dato il titolo
    idx = indices[titulo]
    
    # Ottieni il vettore di similarità per il film dato
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordina i film in base al punteggio di similarità
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Ottieni i punteggi delle 5 pellicole più simili
    sim_scores = sim_scores[1:6]
    
    # Ottieni gli indici dei film
    movie_indices = [i[0] for i in sim_scores]
    
    # Restituisci i titoli dei film raccomandati
    recomendacion = df1['title'].iloc[movie_indices].tolist()

    return(recomendacion)
