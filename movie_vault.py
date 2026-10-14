
import json
import os

MOVIE_FILE = "movies.json"


def load_movies():
    try:
        with open(MOVIE_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: Movie data file is corrupted.")
        return []


def save_movies(movies):
    try:
        with open(MOVIE_FILE, "w") as file:
            json.dump(movies, file, indent=4)
    except OSError as error:
        print(f"Error saving movies: {error}")


def add_movie():
    print("\n--- Add Movie ---")

    title = input("Movie name: ").strip()
    if not title:
        print("Movie name cannot be empty.")
        return

    movies = load_movies()

    if any(m["title"].lower() == title.lower() for m in movies):
        print("This movie already exists!")
        return

    genre = input("Genre: ").strip() or "Unknown"

    try:
        year = int(input("Release year: "))
        rating = float(input("Rating (0-10): "))

        if not 1888 <= year <= 2100:
            print("Invalid release year.")
            return

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

    except ValueError:
        print("Please enter valid numeric values.")
        return

    movies.append({
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating,
        "watched": False
    })

    save_movies(movies)
    print(f"'{title}' added successfully!")


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


def select_movie(movies):
    if not movies:
        print("No movies available.")
        return None

    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie['title']}")

    try:
        choice = int(input("Select movie number: "))

        if 1 <= choice <= len(movies):
            return choice - 1

        print("Invalid movie number.")

    except ValueError:
        print("Enter a valid number.")

    return None


def search_movie():
    movies = load_movies()
    query = input("Enter movie title: ").strip().lower()

    if not query:
        print("Search cannot be empty.")
        return

    results = [
        m for m in movies
        if query in m.get("title", "").lower()
    ]

    if not results:
        print("No matching movies found.")
        return

    for movie in results:
        print(f"{movie['title']} | {movie.get('year')} | {movie.get('rating')}/10")


def toggle_watched():
    movies = load_movies()
    index = select_movie(movies)

    if index is None:
        return

    movies[index]["watched"] = not movies[index].get("watched", False)
    save_movies(movies)

    print(f"Updated status for {movies[index]['title']}!")


def update_rating():
    movies = load_movies()
    index = select_movie(movies)

    if index is None:
        return

    try:
        rating = float(input("Enter new rating (0-10): "))

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

        movies[index]["rating"] = rating
        save_movies(movies)
        print("Rating updated successfully!")

    except ValueError:
        print("Invalid rating.")


def top_rated_movies():
    movies = load_movies()

    if not movies:
        print("No movies available.")
        return

    ranked = sorted(
        movies,
        key=lambda m: float(m.get("rating", 0)),
        reverse=True
    )

    print("\n--- Top Rated Movies ---")

    for index, movie in enumerate(ranked[:10], start=1):
        print(f"{index}. {movie['title']} | {movie.get('rating', 0)}/10")


def show_statistics():
    movies = load_movies()
    total = len(movies)

    watched = sum(1 for m in movies if m.get("watched", False))
    average = (
        sum(float(m.get("rating", 0)) for m in movies) / total
        if total else 0
    )

    print("\n--- MovieVault Statistics ---")
    print(f"Total movies: {total}")
    print(f"Watched: {watched}")
    print(f"Unwatched: {total - watched}")
    print(f"Average rating: {average:.2f}/10")


def filter_genre():
    movies = load_movies()
    genre = input("Enter genre: ").strip().lower()

    results = [
        m for m in movies
        if genre and genre in m.get("genre", "").lower()
    ]

    if not results:
        print("No movies found in this genre.")
        return

    print("\n--- Genre Results ---")

    for movie in results:
        print(f"{movie['title']} | {movie['genre']} | {movie['rating']}/10")


def delete_movie():
    movies = load_movies()
    index = select_movie(movies)

    if index is None:
        return

    title = movies[index]["title"]
    confirm = input(f"Delete '{title}'? (y/n): ").strip().lower()

    if confirm == "y":
        movies.pop(index)
        save_movies(movies)
        print(f"'{title}' deleted successfully!")
    else:
        print("Deletion cancelled.")


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
        print("8. Filter by Genre")
        print("9. Delete Movie")
        print("10. Exit")

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
            filter_genre()
        elif choice == "9":
            delete_movie()
        elif choice == "10":
            print("Thanks for using MovieVault!")
            break
        else:
            print("Invalid choice. Please select 1-10.")


if __name__ == "__main__":
    main()
