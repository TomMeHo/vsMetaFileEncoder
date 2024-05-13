"""
    by oPromessa, 2024

    Example use of vsMetaFileEncoder.
       * Generates vsmeta from seraching on IMDb.
       * Also checks vsmeta file and shows its contents.

    Makes use of modules: click, requests, idmbmovies

    To use, install required modules with pip:
        pip install click
        pip install requests
        pip install imdbmovies
"""
import os
import re

from datetime import date, datetime
import textwrap

import click
import requests

from imdbmovies import IMDB

from vsmetaCodec.vsmetaEncoder import VsMetaMovieEncoder
from vsmetaCodec.vsmetaDecoder import VsMetaDecoder
from vsmetaCodec.vsmetaInfo import VsMetaImageInfo


def write_vsmeta_file(filename: str, content: bytes):
    """ Writes to file in binary mode. Used to write .vsmeta files.
    """
    with open(filename, 'wb') as write_file:
        write_file.write(content)
        write_file.close()


def read_vsmeta_file(filename: str) -> bytes:
    """ Reads from file in binary mode. Used to read .vsmeta files.
    """
    with open(filename, 'rb') as read_file:
        file_content = read_file.read()
        read_file.close()
    return file_content


def lookfor_imdb(movie_title, year=None, tv=False):
    """ Returns movie_info of first movie from year returned by search in IMDb.
    """

    imdb = IMDB()
    results = imdb.search(movie_title, year=year, tv=tv)

    # Filter only movie type entries
    movie_results = [result for result in results["results"]
                     if result["type"] == "movie"]

    print(
        f"Found: [{len(movie_results)}] entries for "
        f"Title: [{movie_title}] Year: [{year}]"
    )

    for cnt, mv in enumerate(movie_results):
        print(
            f"\tEntry: [{cnt}] Name: [{click.style(mv['name'], fg='yellow')}] "
            f"Id: [{mv['id']}] Type: [{mv['type']}]")

    if movie_results:
        movie_info = imdb.get_by_id(movie_results[0]['id'])
        return movie_results[0]['id'], movie_info

    return None, None


def download_poster(url, filename):
    """ Downloads Image from URL into a JPG file.
    """
    http_timeout = 15

    response = requests.get(url, timeout=http_timeout)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)


def find_metadata(title, year, filename, verbose):
    """Search for a movie/Year metada on IMDb.

       If found, downloads to a local .JPG  file the poster
    """
    print(
        f"-------------- : Processing title [{click.style(title, fg='green')}] "
        f"year [{year}] filename [{filename}]")

    vsmeta_filename = None

    year = None if year is None else int(year)

    # Search IMDB for movie information
    movie_id, movie_info = lookfor_imdb(title, year=year)

    if movie_id and movie_info:
        # Download poster
        poster_url = movie_info['poster']
        poster_filename = f'{title.replace(" ", "_")}_poster.jpg'
        download_poster(poster_url, poster_filename)

        # Map IMDB fields to VSMETA
        # and Encode VSMETA
        vsmeta_filename = filename + ".vsmeta"
        map_to_vsmeta(movie_id, movie_info, poster_filename,
                      vsmeta_filename, verbose)
    else:
        print(f"No information found for '{click.style(title, fg='red')}'")

    print(
        f"\tProcessed title [{click.style(title, fg='green')}] year [{year}] "
        f"vsmeta [{vsmeta_filename}]")

    return vsmeta_filename


def map_to_vsmeta(imdb_id, imdb_info, poster_file, vsmeta_filename, verbose):
    """Encodes a .VSMETA file based on imdb_info and poster_file """

    # vsmetaMovieEncoder
    vsmeta_writer = VsMetaMovieEncoder()

    # Build up vsmeta info
    info = vsmeta_writer.info

    # Title
    info.showTitle = imdb_info['name']
    info.showTitle2 = imdb_info['name']
    # Tag line
    info.episodeTitle = f"{imdb_info['name']}"

    # Publishing Date
    info.setEpisodeDate(date(
        int(imdb_info['datePublished'][:4]),
        int(imdb_info['datePublished'][5:7]),
        int(imdb_info['datePublished'][8:])))

    # Set to 0 for Movies: season and episode
    info.season = 0
    info.episode = 0

    # Not used. Set to 1900-01-01
    info.tvshowReleaseDate = date(1900, 1, 1)

    # Locked = False
    info.episodeLocked = False

    info.timestamp = int(datetime.now().timestamp())

    # Classification
    # A classification of None would crash the reading of .vsmeta file with error
    info.classification = "" if imdb_info['contentRating'] is None else imdb_info['contentRating']

    # Rating
    info.rating = imdb_info['rating']['ratingValue']

    # Summary
    info.chapterSummary = imdb_info['description']

    # Cast
    info.list.cast = []
    for actor in imdb_info['actor']:
        info.list.cast.append(actor['name'])

    # Director
    info.list.director = []
    for director in imdb_info['director']:
        info.list.director.append(director['name'])

    # Writer
    info.list.writer = []
    for creator in imdb_info['creator']:
        info.list.writer.append(creator['name'])

    # Genre
    info.list.genre = imdb_info['genre']

    # Read JPG images for Poster and Background
    with open(poster_file, "rb") as image:
        f = image.read()

    # Poster (of Movie)
    episode_img = VsMetaImageInfo()
    episode_img.image = f
    info.episodeImageInfo.append(episode_img)

    # Background (of Movie)
    # Use Posters file for Backdrop also
    info.backdropImageInfo.image = f

    # Not used. Set to VsImageIfnfo()
    info.posterImageInfo = episode_img

    if verbose:
        print("\t---------------: ---------------")
        print(f"\tIMDB id        : {imdb_id}")
        print(f"\tTitle          : {info.showTitle}")
        print(f"\tTitle2         : {info.showTitle2}")
        print(f"\tEpisode title  : {info.episodeTitle}")
        print(f"\tEpisode year   : {info.year}")
        print(f"\tEpisode date   : {info.episodeReleaseDate}")
        print(f"\tEpisode locked : {info.episodeLocked}")
        print(f"\tTimeStamp      : {info.timestamp}")
        print(f"\tClassification : {info.classification}")
        print(f"\tRating         : {info.rating:1.1f}")
        wrap_text = "\n\t                 ".join(
            textwrap.wrap(info.chapterSummary, 150))
        print(f"\tSummary        : {wrap_text}")
        print(
            f"\tCast           : {''.join([f'{name}, ' for name in info.list.cast])}")
        print(
            f"\tDirector       : {''.join([f'{name}, ' for name in info.list.director])}")
        print(
            f"\tWriter         : {''.join([f'{name}, ' for name in info.list.writer])}")
        print(
            f"\tGenre          : {''.join([f'{name}, ' for name in info.list.genre])}")
        print("\t---------------: ---------------")

    write_vsmeta_file(vsmeta_filename, vsmeta_writer.encode(info))

    return True


def find_files(root_dir, valid_ext=(".mp4", ".mkv", ".avi", ".mpg")):
    """ Returns files with extension in valid_ext list
    """

    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(file.casefold().endswith(ext) for ext in valid_ext) and \
               not os.path.isdir(os.path.join(root, file)):
                yield os.path.join(root, file)


def extract_info(file_path):
    """ Convert file_path into dirname and from basename extract
        movie_tile and year. Expecting filename format 'movie title name (1999)'
    """
    dirname = os.path.dirname(file_path)
    basename = os.path.basename(file_path)

    # filtered_value = re.search(r'\D*(\d{4})', basename)
    filtered_value = re.search(r'^(.*?)(\d{4})(.*)$', basename)
    filtered_title = None
    filtered_year = None
    if filtered_value:
        filtered_title = filtered_value.group(1)
        filtered_year = filtered_value.group(2)
    else:
        filtered_title = basename

    filtered_title = filtered_title.replace('.', ' ').strip()

    return dirname, basename, filtered_title, filtered_year


def check_file(file_path):
    """Read .vsmeta file and print it's contents.

    Images within .vsmeta are saved as image_back_drop.jpg and image_poster_NN.jpg
    When checking multiple files, these files are overwritten.
    """

    vsmeta_bytes = read_vsmeta_file(file_path)
    reader = VsMetaDecoder()
    reader.decode(vsmeta_bytes)

    reader.info.printInfo('.', prefix=os.path.basename(file_path))


@click.command()
@click.option('--search',
              type=click.Path(exists=True,
                              file_okay=False,
                              dir_okay=True,
                              resolve_path=True),
              help="Folder to recursively search for media  files to be processed into .vsmeta.")
@click.option("--check",
              type=click.Path(exists=True,
                              file_okay=True,
                              dir_okay=True,
                              resolve_path=True),
              help="Check .vsmeta files. Show info. "
              "Exclusive with --search option.")
@click.option('-v', '--verbose', is_flag=True,
              help="Shows info found on IMDB.")
def main(search, check, verbose):
    """Searches on a folder for Movie Titles and generates .vsmeta files.
       You can then copy them over to your Library.
    """

    if not (check or search) or (check and search):
        raise SystemExit(
            "Must specify at least one (and exclusively) option "
            "--search or --check. Use --help for additional help.")

    if check:
        if os.path.isfile(check) and check.endswith(".vsmeta"):
            print(f"-------------- : Checking file [{check}]")
            check_file(check)
        elif os.path.isdir(check):
            for found_file in find_files(check, valid_ext=('.vsmeta', )):
                print(f"-------------- : Checking file [{check}]")
                check_file(found_file)
        else:
            raise print(
                "Invalid check path or file name. "
                "sPlease provide a valid directory or .vsmeta file.")

    if search:
        print(f"Processing folder: [{search}].")

        # Iterate over the matching files
        for found_file in find_files(search):
            # print(f"Found file: [{found_file}]")
            _, basename, title, year = extract_info(found_file)
            find_metadata(title, year, basename, verbose)


if __name__ == "__main__":
    main()
