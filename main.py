
import os 

ALL_CATEGORY= {"politig" :"https://www.wolof-online.com/?cat=4",
          "nekkin": "https://www.wolof-online.com/?cat=12",
          "diine":"https://www.wolof-online.com/?cat=15",
          "caada":"https://www.wolof-online.com/?cat=6",
          "tàggat-yaram":"https://www.wolof-online.com/?cat=14",
          "koom-koom":"https://www.wolof-online.com/?cat=20",
          "taantaan":"https://www.wolof-online.com/?cat=13",
          "xamtéef":"https://www.wolof-online.com/?cat=16",
          "cosaan":"https://www.wolof-online.com/?cat=18",
          "wer-gu-yaram":"https://www.wolof-online.com/?cat=22",
          "lëkkale":"https://www.wolof-online.com/?cat=21",
          "jotaayu-xale-yi":"https://www.wolof-online.com/?cat=24",
          "mbindu-fent":"https://www.wolof-online.com/?cat=27"
}



for key in list(ALL_CATEGORY.keys()):
    os.system(f"python src/wol_scrapper.py --url {ALL_CATEGORY[key]} --category {key}")

