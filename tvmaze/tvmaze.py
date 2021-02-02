import urllib.request
from urllib.parse import quote
from jsontraverse.parser import JsonTraverseParser


def search_tv_show(tv_show_name: str):
    """searches for a tvshow with name and returns it's details

    Args:
    -----
        tv_show_name (str): name of the tv show ex: friends

    Returns:
    --------
        tuple: tvmaze_id, imdb_id, name, language, genres, poster_url, summary
    """

    api_url = "http://api.tvmaze.com/search/shows?q={}".format(
        quote(tv_show_name))
    print(api_url)
    with urllib.request.urlopen(api_url) as tv_show_search_results:
        list_of_search_results = eval(tv_show_search_results.read()
                                      .decode().replace(
            "null", "None"))
        tv_show = list_of_search_results[0]
        tvmaze_id = tv_show["show"]["id"]
        name = tv_show["show"]["name"]
        language = tv_show["show"]["language"]
        genres = ";".join(tv_show["show"]["genres"])
        imdb_id = tv_show["show"]["externals"]["imdb"]
        poster_url = tv_show["show"]["image"]["original"]
        summary = tv_show["show"]["summary"].replace(
            "<p>", "").replace("</p>", "")
    return tvmaze_id, imdb_id, name, language, genres, poster_url, summary


def search_episode(tvmaze_id: str, season_number: int, episode_number: int):
    """Searches episode with tvmaze and returns the details of the episode

    Args:
    -----
    - tvmaze_id (str): tv maze id
    - season_number (int): season number
    - episode_number (int): episode number

    Returns:
    --------
        tuple: name, aired_year, poster_url, summary
    """
    api_url = "http://api.tvmaze.com/shows/{tvmaze_id}/episodebynumber?season={season_number}&number={episode_number}".format(
        tvmaze_id=tvmaze_id, season_number=season_number,
        episode_number=episode_number)
    print(api_url)
    with urllib.request.urlopen(api_url) as search_result:
        list_of_search_results = eval(search_result.read().decode().replace(
            "null", "None"))
        episode = list_of_search_results
        name = episode["name"]
        aired_year = episode["airdate"][:4]
        poster_url = episode["image"]["original"]
        summary = episode["summary"].replace(
            "<p>", "").replace("</p>", "")
    return name, aired_year, poster_url, summary


def get_tv_cast(tvmaze_id):
    """returns cast

    Args:
        tvmaze_id ([str]): [description]

    Returns:
        [type]: [description]
    """
    api_url = "http://api.tvmaze.com/shows/" + str(tvmaze_id) + "/cast"
    with urllib.request.urlopen(api_url) as search_result:
        res = JsonTraverseParser(search_result.read().decode())
        cast = res.traverse("person.name")
        cast_images = res.traverse("person.image.original")
    return cast, cast_images


def get_tv_crew(tvmaze_id):
    """[summary]

    Args:
        tvmaze_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    api_url = "http://api.tvmaze.com/shows/" + str(tvmaze_id) + "/crew"
    with urllib.request.urlopen(api_url) as search_result:
        # results = search_result.read().decode().replace(
        #     "null", "None").replace("false", "False").replace("true", "True")
        res = JsonTraverseParser(search_result.read().decode())
        crew = res.traverse("person.name")
        crew_images = res.traverse("person.image.original")
    return crew, crew_images
