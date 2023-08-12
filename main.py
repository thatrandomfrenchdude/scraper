import os
from scraper import Scraper

# create one scraper per job and perform scrape

# vars
OUTDIR = 'outputs'
jobs = [
    'https://google.com'
]

def boot():
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

def main() -> None:
    target_url = "sample.html"
    s = Scraper()
    s.scrape(target_url, OUTDIR)


if __name__ == '__main__':
    boot()
    main()