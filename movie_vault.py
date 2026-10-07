import json

MOVIE_FILE = "movies.json"


def load_movies():
    try:
        with open(MOVIE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_movies(movies):
    with open(MOVIE_FILE, "w") as file:
        json.dump(movies, file, indent=4)


def add_movie():
    print("\n--- Add Movie ---")

    title = input("Movie name: ").strip()
    genre = input("Genre: ").strip()

    try:
        year = int(input("Release year: "))
        rating = float(input("Rating (0-10): "))

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

    except ValueError:
        print("Please enter a valid year and rating.")
        return

    movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating,
        "watched": False
    }

    movies = load_movies()
    movies.append(movie)
    save_movies(movies)

    print(f"\n✓ '{title}' added successfully!")


def main():
    print("================================")
    print("       🎬 MOVIEVAULT")
    print("   Movie Watchlist Manager")
    print("================================")

    add_movie()


if __name__ == "__main__":
    main()
