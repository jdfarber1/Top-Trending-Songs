from spotify import get_token, search_for_artist, get_songs_by_artist, print_songs
from boxplot import get_dominant_colors, sort_songs_by_popularity, create_plot_visual, create_plot_simple, \
    plot_top_songs
from PIL import Image
import requests


def main():
    # Ask the user for input
    choice = input(
        "Do you want to search for top trending songs in the US or an artist's top trending songs? Enter 'US' or "
        "'artist': ").lower()

    if choice == 'us':
        # Fetch the US top trending songs
        plot_top_songs()

    elif choice == 'artist':
        # Get artist name from user input
        artist_name = input("Enter the artist name: ")

        # Fetch artist information and songs
        token = get_token()
        result = search_for_artist(token, artist_name)
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)

        # Print top songs
        print_songs(songs)

        # Collect song names, popularity scores, and album cover URLs
        song_names = [song['name'] for song in songs]
        popularity_scores = [song['popularity'] for song in songs]
        album_cover_urls = [song['album']['images'][0]['url'] for song in songs]

        # Download and load album cover images
        album_cover_images = [Image.open(requests.get(url, stream=True).raw) for url in album_cover_urls]

        # Get dominant colors
        dominant_colors = get_dominant_colors(album_cover_images)

        # Sort songs by popularity score
        song_names, popularity_scores, album_cover_images = sort_songs_by_popularity(song_names, popularity_scores,
                                                                                     album_cover_images)

        # Create and display the plots
        create_plot_simple(song_names, popularity_scores, artist_name)
        create_plot_visual(artist_name, song_names, popularity_scores, dominant_colors, album_cover_images)


if __name__ == "__main__":
    main()
