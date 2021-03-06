import os
import sys
from pathlib import Path

import re
from urllib.request import urlretrieve

from tvmaze.tvmaze import search_tv_show, search_episode
from util.util import get_legal_chars

temp_folder_path: Path = Path("")

if sys.platform == "linux":
    temp_folder_path = Path(os.environ["HOME"] + "/temp")
else:
    temp_folder_path = Path(os.environ["HOMEPATH"] + "/temp")

if not os.path.exists(temp_folder_path):
    os.mkdir(temp_folder_path)

show_folder: Path = Path(
    input("Enter Videos folder path: ").replace("\\", "/"))

if not os.path.exists(show_folder):
    raise NotADirectoryError(show_folder + " doesn't exist")

video_file_extensions = ['.mkv', ".mp4"]

files: list = [file for file in os.listdir(show_folder) if Path(
    file).suffix in video_file_extensions]

if len(files) == 0:
    sys.exit()

tvmaze_id, imdb_id, name, language, genres, poster_url, summary = search_tv_show(
    show_folder.name)

season = 0
episode = 0
season_pattern = r"(s|season)[0-9]."
episode_pattern = r"(e|epiosode)[0-9]."

poster_image_path: Path = show_folder / Path("folder.jpg")

if not os.path.exists(poster_image_path):
    urlretrieve(poster_url, poster_image_path)

for file in files:
    season = int(str(re.search(season_pattern, file.lower()).group()
                     ).replace("season", "").replace("s", "").replace("e", ""))
    episode = int(str(re.search(episode_pattern, file.lower()).group()).replace(
        "episode", "").replace("e", "").replace(".", ""))
    print(show_folder.name, file, season, episode)

    episode_name, aired_year, poster_url, episode_summary = search_episode(
        tvmaze_id, season, episode)

    file_name = Path(file)
    season_info = "S{}E{}-".format(season, episode)

    os.renames(show_folder / file_name,
               show_folder / Path("Season " +
                                  str(season)) / Path(get_legal_chars(season_info + episode_name) + "." + file_name.suffix))
