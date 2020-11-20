#!/usr/bin/python3

import sys
import requests
from pyfiglet import figlet_format
from termcolor import colored, cprint

apikey = "YOUR_APIKEY"


def get_episodes(title, season, episode):
    episode_list = []

    if season != '':
        path = "http://omdbapi.com/?apikey=" + apikey + \
            "&type=series&t=" + title + "&season=" + season
        r = requests.get(path)
        data = r.json()
        if data["totalSeasons"] == "N/A":
            print(title + "is not in our database!")
            exit(1)
        for ep in data["Episodes"]:
            if ep["imdbRating"] == "N/A":
                continue
            episode_data = {
                "season": season,
                "episode_number": ep["Episode"],
                "title": ep["Title"],
                "rating": float(ep["imdbRating"]),
                "date": ep["Released"],
            }
            episode_list.append(episode_data)
        if episode == '':
            episode_list = sorted(
                episode_list, key=lambda i: i["rating"], reverse=True
            )
            return episode_list
        else:
            episode_list = [episode_list[int(episode) - 1]]
            return episode_list

    path = "http://omdbapi.com/?apikey="+apikey+"&type=series&t=" + title
    r = requests.get(path)
    data = r.json()
    if data["totalSeasons"] == "N/A":
        print(title + "is not in our database!")
        exit(1)
    season_count = int(data["totalSeasons"])
    for i in range(1, season_count+1):
        new_path = path + "&season=" + str(i)
        ep_r = requests.get(new_path)
        new_data = ep_r.json()
        for ep in new_data["Episodes"]:
            if ep["imdbRating"] == "N/A":
                continue
            episode_data = {
                "season": str(i),
                "episode_number": ep["Episode"],
                "title": ep["Title"],
                "rating": float(ep["imdbRating"]),
                "date": ep["Released"],
            }
            episode_list.append(episode_data)
    episode_list = sorted(
        episode_list, key=lambda i: i["rating"], reverse=True
    )
    return episode_list


def print_episodes(episode_list, n):
    i = 1
    if n == 1:
        print(colored("%3d" % i, 'cyan') + colored(") Season: ", 'cyan') + colored(episode_list[0]["season"], 'yellow') + colored("\tEpisode: ", 'cyan') + colored(episode_list[0]["episode_number"], 'yellow') + colored(
            "\tIMDB Rating: ", 'cyan') + colored(str(episode_list[0]["rating"]), 'yellow') + colored("\tDate: ", 'cyan') + colored(episode_list[0]["date"], 'yellow') + colored("\tTitle: ", 'cyan') + colored(episode_list[0]["title"], 'yellow'))
        return
    for episode in episode_list[:n]:
        print(colored("%3d" % i, 'cyan') + colored(") Season: ", 'cyan') + colored(episode["season"], 'yellow') + colored("\tEpisode: ", 'cyan') +
              colored(episode["episode_number"], 'yellow') + colored("\tIMDB Rating: ", 'cyan') + colored(str(episode["rating"]), 'yellow') + colored("\tDate: ", 'cyan') + colored(episode["date"], 'yellow') + colored("\tTitle: ", 'cyan') + colored(episode["title"], 'yellow'))
        i += 1


def option_handling(arguments):
    episode_count = 0
    title = ""
    episode = ""
    season = ""
    if len(arguments) == 1:
        print("Usage: top_episodes [-t|--title TITLE]\n")
        print("Use -h|--help to get more help!")
        exit(1)
    for i in range(1, len(arguments), 1):
        if arguments[i] == "-t" or arguments[i] == "--title":
            i += 1
            while i < len(arguments) and arguments[i][0] != "-":
                title += arguments[i] + " "
                i += 1
        elif arguments[i] == "-n" or arguments[i] == "--number":
            episode_count = int(arguments[i+1])
            i += 1
        elif arguments[i] == "-e" or arguments[i] == "--episode":
            episode = arguments[i+1]
            i += 1
        elif arguments[i] == "-s" or arguments[i] == "--season":
            season = arguments[i+1]
            i += 1
        elif arguments[i] == "-h" or arguments[i] == "--help":
            print("Usage: top_episodes [-t|--title TITLE]\n")
            print("Optional:")
            print("\t-n|--number:\tNumber of top episodes to show")
            print("\t-s|--season:\tTo choose a season")
            print("\t-e|--episode:\tTo choose an episode")
            print("\t-h|--help:\tTo get detailed help")
            exit(1)
        elif title == "":
            print("Usage: top_episodes [-t|--title TITLE]\n")
            print("Use -h|--help to get more help!")
            exit(1)
    return title, episode_count, episode, season


if __name__ == "__main__":

    cprint(figlet_format('Top Episodes', font='graffiti',
                         justify='center'), 'red', attrs=['bold'])

    title, episode_count, episode, season = option_handling(sys.argv)
    if title == "":
        print("Usage: top_episodes [-t TITLE]\n")
        print("Use -h|--help to get more help!")
        exit(1)
    episodes = get_episodes(title, season, episode)
    if episode_count == 0:
        print_episodes(episodes, len(episodes))
    else:
        print_episodes(episodes, episode_count)
