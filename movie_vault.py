
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
    if not title:
        print("Movie name cannot be empty.")
        return

    genre = input("Genre: ").strip()

    try:
        year = int(input("Release year: "))
        rating = float(input("Rating (0-10): "))

        if year < 1888 or year > 2100:
            print("Please enter a valid release year.")
            return

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

    except ValueError:
        print("Please enter a valid year and rating.")
        return

    movies = load_movies()

    movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating,
        "watched": False
    }

    movies.append(movie)
    save_movies(movies)
    print(f"\nMovie '{title}' added successfully!")


def view_movies():
    movies = load_movies()

    print("\n--- Your Movie Collection ---")

    if not movies:
        print("No movies found. Add a movie first.")
        return

    for index, movie in enumerate(movies, start=1):
        status = "Watched" if movie.get("watched", False) else "Not Watched"

        print(f"\n{index}. {movie['title']}")
        print(f"   Genre: {movie.get('genre', 'Unknown')}")
        print(f"   Year: {movie.get('year', 'Unknown')}")
        print(f"   Rating: {movie.get('rating', 0)}/10")
        print(f"   Status: {status}")


def search_movie():
    movies = load_movies()
    query = input("\nEnter movie title to search: ").strip().lower()

    if not query:
        print("Please enter a movie title.")
        return

    results = [
        movie for movie in movies
        if query in movie.get("title", "").lower()
    ]

    if not results:
        print("No matching movies found.")
        return

    print("\n--- Search Results ---")

    for movie in results:
        print(
            f"{movie['title']} ({movie.get('year', 'Unknown')}) "
            f"| {movie.get('genre', 'Unknown')} "
            f"| Rating: {movie.get('rating', 0)}/10"
        )


def main():
    while True:
        print("\n================================")
        print("          MOVIEVAULT")
        print("    Movie Watchlist Manager")
        print("================================")
        print("1. Add Movie")
        print("2. View Movies")
        print("3. Search Movie")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            view_movies()
        elif choice == "3":
            search_movie()
        elif choice == "4":
            print("Thanks for using MovieVault!")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()

