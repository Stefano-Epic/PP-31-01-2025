"""
PROVA SCRITTA DI PROGRAMMING PRINCIPLES

Candidato: Stefano Ranzato
Matricola: S00009724

Note:
- Ho implementato e testato tutti gli esercizi richiesti.
- Ho aggiunto un errore personalizzato "MovieAlreadyExistsError" per gestire il caso in cui si tenta di aggiungere un film già esistente.
- Ho aggiunto, dopo aver scritto il codice, una sua alternativa più semplice senza l'uso di list comprehension e funzioni lambda.
- Nell'idecisione fra l'uso di return o l'uso di raise per la gestione di un'eccezione dopo un try, ho scelto di utilizzare raise per attenermi alla alla prassi comune in python.
- Questa mia decisione è stata presa dopo una rapida ricerca, dalla quale è emerso che è più comune sollevare un'eccezione con raise o gestirla piuttosto che ritornarla.
- Ho aggiunto alcuni controlli non richiesti per gestire casi particolari come ad esempio la gestione dell'assenza di film.
"""

import os
import json


class MovieLibrary:
    # ECCEZIONE PERSONALIZZATA
    class MovieAlreadyExistsError(Exception):
        """
        - Eccezione personalizzato per gestire il caso in cui si tenta di aggiungere un film già esistente.
        - Eredita da "Exception".
        """
        def __init__(self, message):
            super().__init__(message)

    # ESERCIZIO 18
    class MovieNotFoundError(Exception):
        """
        - Eccezione personalizzato per gestire il caso in cui un film non è stato trovato.
        - Eredita da "Exception".
        """
        def __init__(self, message):
            super().__init__(message)

    # COSTRUTTORE
    def __init__(self, directory: str):
        """
        - Salvo il percorso del file JSON in "self.directory".
        - Controllo se il file esiste, altrimenti sollevo un'eccezione "FileNotFoundError".
        - Carico i dati dal file JSON.
        - Sollevo un'eccezione "ValueError" se il file JSON non è valido.
        - Sollevo un'eccezione "IOError" se si verificano errori durante la lettura del file.
        """
        self.directory = directory

        # ESERCIZIO 18
        if not os.path.isfile(self.directory):
            raise FileNotFoundError(f"File not found: {self.directory}")

        try:
            with open(self.directory, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON file: {e}")
        except Exception as e:
            raise IOError(f"Error while reading the file: {e}")

    # FUNZIONE DI SUPPORTO PER AGGIORNARE IL FILE JSON
    def __update_json_file(self):
        """
        - Apro il file JSON in modalità scrittura.
        - Uso la funzione "json.dump()" per aggiornare il file JSON.
        """
        with open(self.directory, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4)

    # FUNZIONE DI SUPPORTO PER VALIDARE I DATI DEL FILM
    def __validate_movie_data(self, title: str = None, director: str = None, year: int = None, genres: list[str] = None):
        """
        - Uso una serie di "if" per validare i dati del film.
        - Sollevo un'eccezione "TypeError" se i dati non sono validi.
        """
        if title is not None and not isinstance(title, str):
            raise TypeError("Title must be a string.")
        if director is not None and not isinstance(director, str):
            raise TypeError("Director must be a string.")
        if year is not None and not isinstance(year, int):
            raise TypeError("Year must be an integer.")
        if (genres is not None and (not isinstance(genres, list) or not all(isinstance(g, str) for g in genres))):
            raise TypeError("Genres must be a list of strings.")

    # ESERCIZIO 1
    def get_movies(self):
        """
        - Ritorno la lista di film.
        """
        return self.movies

    # ESERCIZIO 2
    def add_movie(self, title: str, director: str, year: int, genres: list[str]):
        """
        - Uso la funzione "__validate_movie_data()" in un "try" per validare i dati del film.
        - Sollevo e ritorno un'eccezione se i dati non sono validi.
        - Uso la funzione "get_movie_by_title()" per verificare se il film esiste già.
        - Sollevo e ritorno un'eccezione se il film esiste già.
        - Aggiungo il film alla lista.
        - Aggiorno il file JSON.
        """
        try:
            self.__validate_movie_data(title, director, year, genres)
        except Exception as e:
            raise e

        try:
            if self.get_movie_by_title(title):
                raise self.MovieAlreadyExistsError("Movie already exists")
        except Exception as e:
            raise e

        self.movies.append({"title": title, "director": director, "year": year, "genres": genres})
        self.__update_json_file()

    # ESERCIZIO 3
    def remove_movie(self, title: str):
        """
        - Uso una list comprehension per ottenere il film da rimuovere.
        - Uso "movie["title"].casefold() == title.casefold()" come criterio (filtro) per la list comprehension.
        - Uso la funzione "next()" per ottenere il primo film che soddisfa il criterio specificando di ritornare "None" se non viene trovato nessun film.
        - Se il film è stato trovato lo rimuovo dalla lista, aggiorno il file JSON e lo ritorno.
        - Se il film non è stato trovato, sollevo un'eccezione "MovieNotFoundError".
        """
        removed_movie = next((movie for movie in self.movies if movie["title"].casefold() == title.casefold()), None)

        if removed_movie:
            self.movies.remove(removed_movie)
            self.__update_json_file()
            return removed_movie

        # ESERCIZIO 18
        raise self.MovieNotFoundError("Movie was not found")

        # Codice senza l'uso di list comprehension
        """
        removed_movie = None
        for movie in self.movies:
            if movie["title"].casefold() == title.casefold():
                removed_movie = movie
                self.movies.remove(movie)
                self.__update_json_file()
                return removed_movie

        # ESERCIZIO 18
        raise self.MovieNotFoundError("Movie was not found")
        """

    # ESERCIZIO 4
    def update_movie(self, title: str, director: str = None, year: int = None, genres: list[str] = None):
        """
        - Uso la funzione "__validate_movie_data()" in un "try" per validare i dati del film.
        - Sollevo e ritorno un'eccezione se i dati non sono validi.
        - Modifico, se specificati, i dati del film.
        - Aggiorno il file JSON.
        """
        try:
            self.__validate_movie_data(title, director, year, genres)
        except Exception as e:
            raise e

        # Aggiorno i dati del film
        for movie in self.movies:
            if movie["title"].casefold() == title.casefold():
                if director is not None:
                    movie["director"] = director
                if year is not None:
                    movie["year"] = year
                if genres is not None:
                    movie["genres"] = genres
                self.__update_json_file()
                return movie

        # ESERCIZIO 18
        raise self.MovieNotFoundError("Movie was not found")

    # ESERCIZIO 5
    def get_movie_titles(self):
        """
        - Uso una list comprehension per ottenere una lista di titoli dei film.
        - Ritorno la lista di titoli dei film.
        """
        return [movie["title"] for movie in self.movies]

        # Codice senza l'uso di list comprehension
        """
        self.titles = []
        for movie in self.movies:
            self.titles.append(movie["title"])

        return self.titles
        """

    # ESERCIZIO 6
    def count_movies(self):
        """
        - Uso len() per ottenere il numero di film nella lista.
        - Ritorno il numero di film.
        """
        return len(self.movies)

    # ESERCIZIO 7
    def get_movie_by_title(self, title: str):
        """
        - Uso una string comprehension per ottenere il film con il titolo specificato.
        - Uso "movie["title"].casefold() == title.casefold()" come criterio (filtro) per la list comprehension.
        - Ritorno il film con il titolo specificato.
        """
        return next((movie for movie in self.movies if movie["title"].casefold() == title.casefold()), None)

        # Codice senza l'uso di list comprehension
        """
        for movie in self.movies:
            if movie["title"].casefold() == title.casefold():
                return movie
        return None
        """

    # ESERCIZIO 8
    def get_movies_by_title_substring(self, substring: str):
        """
        - Uso una list comprehension per ottenere una lista di film.
        - Uso "substring.casefold() in movie["title"].casefold()" come criterio (filtro) per la list comprehension.
        - Ritorno la lista di film con il titolo che contiene il testo specificato per la ricerca.
        """
        return [movie for movie in self.movies if substring.casefold() in movie["title"].casefold()]

        # Codice senza l'uso di list comprehension
        """
        movies = []
        for movie in self.movies:
            if substring.casefold() in movie["title"].casefold():
                movies.append(movie)
        return movies
        """

    # ESERCIZIO 9
    def get_movies_by_year(self, year: int):
        """
        - Uso una list comprehension per ottenere una lista di film.
        - Uso "movie["year"] == year" come criterio (filtro) per la list comprehension.
        - Ritorno la lista di film.
        """
        return [movie for movie in self.movies if movie["year"] == year]

        # Codice senza l'uso di list comprehension
        """
        movies = []
        for movie in self.movies:
            if movie["year"] == year:
                movies.append(movie)
        return movies
        """

    # ESERCIZIO 10
    def count_movies_by_director(self, director: str):
        """
        - Uso una list comprehension per ottenere il numero di film.
        - Uso "movie["director"].casefold() == director.casefold()" come criterio (filtro) per la list comprehension.
        - Uso la funzione "len()" per ottenere il numero di film.
        - Ritorno il numero di film con il regista specificato.
        """
        return len([movie for movie in self.movies if movie["director"].casefold() == director.casefold()])

        # Codice senza l'uso di list comprehension
        """
        count = 0
        for movie in self.movies:
            if movie["director"].casefold() == director.casefold():
                count += 1
        return count
        """

    # ESERCIZIO 11
    def get_movies_by_genre(self, genre: str):
        """
        - Uso una list comprehension per ottenere una lista di film.
        - Uso "any(g.casefold() == genre.casefold() for g in movie["genres"])" come criterio (filtro) per la list comprehension.
        - All'intero del criterio uso una list comprehension per verificare se il genere specificato è presente nella lista di generi del film.
        - Ritorno la lista di film con il genere specificato.
        """
        return [movie for movie in self.movies if any(g.casefold() == genre.casefold() for g in movie["genres"])]

        # Codice senza l'uso di list comprehension
        """
        movies = []
        for movie in self.movies:
            for g in movie["genres"]:
                if g.casefold() == genre.casefold():
                    movies.append(movie)
                    break
        return movies
        """

    # ESERCIZIO 12
    def get_oldest_movie_title(self):
        """
        - Uso la funzione "min()" per ottenere il film più vecchio.
        - Uso una funzione lambda come criterio per la funzione "min()".
        - Nella funzione lambda, uso "movie["year"]" per ottenere l'anno del film.
        - Aggiungo ["title"] dopo la funzione "min()" perottenere solo il titolo del film.
        - Ritorno il titolo del film più vecchio o "None" se non ci sono film.
        """
        return min(self.movies, key=lambda movie: movie["year"])["title"] if self.movies else None

        # Codice senza l'uso funzioni lambda
        """
        oldest_movie = None
        min_year = float('inf')  # Un valore iniziale molto grande

        for movie in self.movies:
            if movie["year"] < min_year:
                min_year = movie["year"]
                oldest_movie = movie

        return oldest_movie["title"] if oldest_movie else None
        """

    # ESERCIZIO 13
    def get_average_release_year(self):
        """
        - Uso una list comprehension per ottenere la somma degli anni dei film.
        - Uso la funzione "sum()" per ottenere la somma degli anni.
        - Uso la funzione "len()" per ottenere il numero di film.
        - Divido la somma degli anni per il numero di film.
        - Uso "round()" per arrotondare il risultato a una cifra decimale.
        - Non eseguo ulteriori controlli sul tipo di dato tornato in quanto in Pyhton il risultato di una divisione sarà sempre un float.
        - Ritorno la media degli anni o "None" se non ci sono film.
        """
        return round(sum(movie["year"] for movie in self.movies) / len(self.movies), 1) if self.movies else None

        # Codice senza l'uso di list comprehension
        """
        total_years = 0
        movie_count = 0

        for movie in self.movies:
            total_years += movie["year"]
            movie_count += 1

        if movie_count == 0:
            return None  # Gestione del caso in cui non ci siano film

        return round(total_years / movie_count, 1)
        """

    # ESERCIZIO 14
    def get_longest_title(self):
        """
        - Uso la funzione "max()" per ottenere il film con il titolo più lungo.
        - Uso una funzione lambda come criterio per la funzione "max()".
        - Nella funzione lambda, uso "len(movie["title"])" per ottenere la lunghezza del titolo del film.
        - Aggiungo ["title"] dopo la funzione "max()" per ottenere solo il titolo del film.
        - Ritorno il titolo più lungo o "None" se non ci sono film.
        """
        return max(self.movies, key=lambda movie: len(movie["title"]))["title"] if self.movies else None

        # Codice senza l'uso di list comprehension e funzioni lambda
        """
        max_length = 0
        longest_movie = None

        for movie in self.movies:
            title_length = len(movie["title"])
            if title_length > max_length:
                max_length = title_length
                longest_movie = movie

        return longest_movie["title"] if longest_movie else None
        """

    # ESERCIZIO 15
    def get_titles_between_years(self, start_year: int, end_year: int):
        """
        - Uso una list comprehension per ottenere una lista di titoli dei film.
        - Uso "start_year <= movie["year"] <= end_year" come criterio (filtro) per la list comprehension.
        - Ritorno la lista di titoli dei film.
        """
        return [movie["title"] for movie in self.movies if start_year <= movie["year"] <= end_year]

        # Codice senza l'uso di list comprehension
        """
        movies_title = []
        for movie in self.movies:
            if start_year <= movie["year"] <= end_year:
                movies_title.append(movie["title"])
        return movies_title
        """

    # ESERCIZIO 16
    def get_most_common_year(self):
        """
        - Uso una list comprehension per ottenere una lista contenente tutti gli anni dei film.
        - Uso la funzione "set()" per ottenere un insieme di anni unici e ottimizzare il calcolo (funzionerebbe anche senza).
        - Uso "key=years.count" come criterio per la funzione "max()".
        - Uso la funzione "max()" per ottenere l'anno più comune.
        - Ritorno l'anno più comune o "None" se non ci sono film.
        """
        years = [movie["year"] for movie in self.movies]
        return max(set(years), key=years.count) if self.movies else None

        # Codice maggiormente compresso ma con un costo computazionale maggiore
        """
        return max(set(movie["year"] for movie in self.movies), key=[movie["year"] for movie in self.movies].count)
        """

        # Codice senza l'uso di list comprehension
        """
        year_count = {}
        for movie in self.movies:
            y = movie["year"]
            year_count[y] = year_count.get(y, 0) + 1

        return max(year_count, key=year_count.get)
        """







#################
### TEST ZONE ###
#################

# Rimuovere il commento per eseguire il test

"""
# Recupero il percorso assoluto del file JSON
path_to_json = os.path.join(os.path.dirname(__file__), "movies.json")

# Creo un'istanza della classe MovieLibrary
library = MovieLibrary(path_to_json)

# ESERCIZIO 1
print("ESERCIZIO 1:")
print(library.get_movies())
# ESERCIZIO 2
print("\n\nESERCIZIO 2:")
library.add_movie("Avatar", "James Cameron", 2009, ["Action", "Adventure"])
print(library.get_movies())
# ESERCIZIO 3
print("\n\nESERCIZIO 3:")
library.remove_movie("Avatar")
print(library.get_movies())
# ESERCIZIO 4
print("\n\nESERCIZIO 4:")
library.add_movie("Avatar", "James Cameron", 2009, ["Action", "Adventure"])
print(library.get_movies())
library.update_movie("Avatar", "James Cameron", None, ["Action", "Adventure", "Fantasy"])
print(library.get_movies())
library.remove_movie("Avatar")
# ESERCIZIO 5
print("\n\nESERCIZIO 5:")
print(library.get_movie_titles())
# ESERCIZIO 6
print("\n\nESERCIZIO 6:")
print(library.count_movies())
# ESERCIZIO 7
print("\n\nESERCIZIO 7:")
print(library.get_movie_by_title("Forrest Gump"))
# ESERCIZIO 8
print("\n\nESERCIZIO 8:")
print(library.get_movies_by_title_substring("The"))
# ESERCIZIO 9
print("\n\nESERCIZIO 9:")
print(library.get_movies_by_year(1994))
# ESERCIZIO 10
print("\n\nESERCIZIO 10:")
print(library.count_movies_by_director("Christopher Nolan"))
# ESERCIZIO 11
print("\n\nESERCIZIO 11:")
print(library.get_movies_by_genre("Crime"))
# ESERCIZIO 12
print("\n\nESERCIZIO 12:")
print(library.get_oldest_movie_title())
# ESERCIZIO 13
print("\n\nESERCIZIO 13:")
print(library.get_average_release_year())
# ESERCIZIO 14
print("\n\nESERCIZIO 14:")
print(library.get_longest_title())
# ESERCIZIO 15
print("\n\nESERCIZIO 15:")
print(library.get_titles_between_years(1970, 1999))
# ESERCIZIO 16
print("\n\nESERCIZIO 16:")
print(library.get_most_common_year())
"""
