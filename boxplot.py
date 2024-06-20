import os
import tempfile
from colorthief import ColorThief
import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd


def fetch_spotify_chart():
    url = 'https://charts-spotify-com-service.spotify.com/public/v0/charts'
    response = requests.get(url)
    chart = []
    for entry in response.json()['chartEntryViewResponses'][0]['entries']:
        chart.append({
            "Rank": entry['chartEntryData']['currentRank'],
            "Artist": ', '.join([artist['name'] for artist in entry['trackMetadata']['artists']]),
            "TrackName": entry['trackMetadata']['trackName']
        })
    return pd.DataFrame(chart)


def get_dominant_colors(album_cover_images):
    dominant_colors = []
    temp_dir = tempfile.mkdtemp()

    for i, img in enumerate(album_cover_images):
        img_path = os.path.join(temp_dir, f"album_cover_{i}.jpg")
        img.save(img_path, format='JPEG')

        color_thief = ColorThief(img_path)
        rgb_color = color_thief.get_color(quality=1)
        dominant_colors.append('#%02x%02x%02x' % rgb_color)

        os.remove(img_path)

    return dominant_colors


def sort_songs_by_popularity(song_names, popularity_scores, album_cover_images):
    sorted_indices = np.argsort(popularity_scores)[::-1]
    song_names = [song_names[i] for i in sorted_indices]
    popularity_scores = [popularity_scores[i] for i in sorted_indices]
    album_cover_images = [album_cover_images[i] for i in sorted_indices]
    return song_names, popularity_scores, album_cover_images


def create_plot_simple(song_names, popularity_scores, artist_name):
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.barh(song_names, popularity_scores, color='skyblue')
    plt.xlabel('Popularity Score')
    plt.ylabel('Song Name')
    plt.title(f'Top Trending Songs by {artist_name}')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest popularity on top

    # Adding popularity values on the bars
    for index, value in enumerate(popularity_scores):
        plt.text(value, index, str(value))

    plt.tight_layout()
    plt.show()


def create_plot_visual(artist_name, song_names, popularity_scores, dominant_colors, album_cover_images):
    fig, axs = plt.subplots(len(song_names), 2, figsize=(10, 0.5 * len(song_names)),
                            gridspec_kw={'width_ratios': [0.2, 0.8]})

    for i, (name, score, color, img) in enumerate(
            zip(song_names, popularity_scores, dominant_colors, album_cover_images)):
        ax_img = axs[i, 0]
        ax_img.imshow(img)
        ax_img.axis('off')
        ax_img.text(0, -71, name, fontsize=7, verticalalignment='center')

        ax_bar = axs[i, 1]
        ax_bar.barh(0, score, color=color)
        ax_bar.text(score + 5, 0, str(score), va='center')
        ax_bar.axis('off')

    axs[0, 1].set_title('Popularity Scores')
    plt.suptitle(f'Top Tending Songs by {artist_name}', fontsize=16)
    plt.tight_layout(rect=[0, 3, 1, 0.9])
    plt.show()


def plot_top_songs():
    spotify_chart_df = fetch_spotify_chart()

    # Filter the top 15 songs and reverse the order
    top_15 = spotify_chart_df.head(15)[::-1]

    # Create a vertical bar chart
    plt.figure(figsize=(10, 8))
    plt.bar(top_15['Artist'] + ' - ' + top_15['TrackName'], 16 - top_15['Rank'], color='skyblue')  # Invert the rank
    plt.xlabel('Artist - Song')
    plt.ylabel('Rank')
    plt.title('Top 15 Songs on Spotify')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

    # Set y-axis ticks to go from 1 to 15
    plt.yticks(range(1, 16))

    plt.tight_layout()

    plt.show()
