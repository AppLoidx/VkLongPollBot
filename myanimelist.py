import requests
import bs4


class Myanimelist:

    @staticmethod
    def get_top(count: int=5, by: str="") -> dict:
        types = ["", "airing", "upcoming", "tv", "movie", "ova", "special", "bypopularity", "favorite"]
        if by not in types:
            return {"error: ": "Неизвестный тип!"}
        html = requests.get("https://myanimelist.net/topanime.php?type="+by)
        soup = bs4.BeautifulSoup(html.text, "html.parser")

        res = {}

        for anime in soup.select(".ranking-list", limit=count):

            url = anime.select(".hoverinfo_trigger")[0]['href']
            anime = anime.select(".hoverinfo_trigger")[0].findAll("img")[0]
            name = anime['alt'].split(":")[1].strip(" ")
            res[name] = url

        return res


