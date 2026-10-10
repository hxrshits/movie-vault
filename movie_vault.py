
import json

MOVIE_FILE = "movies.json"


def load_movies():
    try:
        with open(MOVIE_FILE, "r") as file:
            movies = json.load(file)
            return movies if isinstance(movies, list) else []
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

        if not 1888 <= year <= 2100:
            print("Please enter a valid release year.")
            return

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

    except ValueError:
        print("Please enter a valid year and rating.")
        return

    movies = load_movies()
    movies.append({
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating,
        "watched": False
    })

    save_movies(movies)
    print(f"Movie '{title}' added successfully!")


def view_movies():
    movies = load_movies()

    print("\n--- Your Movie Collection ---")

    if not movies:
        print("No movies found.")
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
            f"| Rating: {movie.get('rating', 0)}/10"
        )


def select_movie(movies):
    if not movies:
        print("No movies available. Add a movie first.")
        return None

    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie['title']}")

    try:
        choice = int(input("Select movie number: "))
        if 1 <= choice <= len(movies):
            return movies[choice - 1]
        print("Invalid movie number.")
    except ValueError:
        print("Please enter a valid number.")

    return None


def toggle_watched():
    movies = load_movies()
    movie = select_movie(movies)

    if movie is None:
        return

    movie["watched"] = not movie.get("watched", False)
    save_movies(movies)

    status = "Watched" if movie["watched"] else "Not Watched"
    print(f"{movie['title']} marked as {status}!")


def update_rating():
    movies = load_movies()
    movie = select_movie(movies)

    if movie is None:
        return

    try:
        rating = float(input("Enter new rating (0-10): "))

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

        movie["rating"] = rating
        save_movies(movies)
        print(f"Rating updated for {movie['title']}!")

    except ValueError:
        print("Please enter a valid number.")


def top_rated_movies():
    movies = load_movies()

    if not movies:
        print("No movies available.")
        return

    ranked = sorted(
        movies,
        key=lambda movie: float(movie.get("rating", 0)),
        reverse=True
    )

    print("\n--- Top-Rated Movies ---")

    for index, movie in enumerate(ranked[:10], start=1):
        print(
            f"{index}. {movie['title']} "
            f"| Rating: {movie.get('rating', 0)}/10 "
            f"| Year: {movie.get('year', 'Unknown')}"
        )


def show_statistics():
    movies = load_movies()
    total = len(movies)

    watched = sum(
        1 for movie in movies if movie.get("watched", False)
    )
    unwatched = total - watched

    average = (
        sum(float(movie.get("rating", 0)) for movie in movies) / total
        if total else 0
    )

    print("\n--- MovieVault Statistics ---")
    print(f"Total movies: {total}")
    print(f"Watched: {watched}")
    print(f"Unwatched: {unwatched}")
    print(f"Average rating: {average:.2f}/10")


def main():
    while True:
        print("\n================================")
        print("          MOVIEVAULT")
        print("    Movie Watchlist Manager")
        print("================================")
        print("1. Add Movie")
        print("2. View Movies")
        print("3. Search Movie")
        print("4. Mark Watched/Unwatched")
        print("5. Update Rating")
        print("6. Top-Rated Movies")
        print("7. Statistics")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            view_movies()
        elif choice == "3":
            search_movie()
        elif choice == "4":
            toggle_watched()
        elif choice == "5":
            update_rating()
        elif choice == "6":
            top_rated_movies()
        elif choice == "7":
            show_statistics()
        elif choice == "8":
            print("Thanks for using MovieVault!")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()

