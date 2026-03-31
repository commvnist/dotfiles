#!/usr/bin/env python3
"""Create an Obsidian movie entry from a TMDB URL or interactive search."""

import sys
import re
import os
import urllib.request
import urllib.parse
from datetime import date

MAX_SEARCH_RESULTS = 10


def fetch_html(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='replace')


def search_tmdb(query):
    """Search TMDB and return a list of (title, year, description, url) tuples."""
    encoded = urllib.parse.quote(query)
    search_url = f'https://www.themoviedb.org/search?query={encoded}'
    print(f'Searching {search_url} ...', file=sys.stderr)
    html = fetch_html(search_url)

    # Extract the movie results section
    movie_sec_match = re.search(
        r'<div class="search_results movie[^"]*">\s*<div class="results flex">(.*?)<div class="pagination_wrapper">',
        html, re.DOTALL
    )
    if not movie_sec_match:
        return []

    section = movie_sec_match.group(1)

    results = []
    # Split on card div boundaries (ids are hex strings assigned by TMDB)
    card_chunks = re.split(r'(?=<div id="[0-9a-f]+" class="card v4 tight")', section)

    for chunk in card_chunks:
        if not chunk.strip():
            continue

        href_match = re.search(r'href="(/movie/[^"]+)"', chunk)
        if not href_match:
            continue
        href = href_match.group(1)
        full_url = f'https://www.themoviedb.org{href}'

        title_match = re.search(r'<h2[^>]*>\s*<span>([^<]+)</span>', chunk)
        title = title_match.group(1).strip() if title_match else 'Unknown'

        year_match = re.search(r'<span class="release_date">[^<]*?(\d{4})[^<]*</span>', chunk)
        year = year_match.group(1) if year_match else ''

        desc_match = re.search(r'<div class="overview">\s*<p>(.*?)</p>', chunk, re.DOTALL)
        description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else '(No description)'

        results.append((title, year, description, full_url))
        if len(results) >= MAX_SEARCH_RESULTS:
            break

    return results


def prompt_search():
    """Interactive search and selection. Returns the selected TMDB movie URL."""
    query = input('Search TMDB: ').strip()
    if not query:
        print('No query entered.', file=sys.stderr)
        sys.exit(1)

    try:
        results = search_tmdb(query)
    except Exception as e:
        print(f'Error searching: {e}', file=sys.stderr)
        sys.exit(1)

    if not results:
        print('No results found.', file=sys.stderr)
        sys.exit(1)

    print()
    for i, (title, year, desc, _url) in enumerate(results, 1):
        label = f'{title} ({year})' if year else title
        short_desc = (desc[:120] + '...') if len(desc) > 120 else desc
        print(f'{i}. {label}')
        print(f'   {short_desc}')
        print()

    while True:
        choice = input(f'Select a movie (1-{len(results)}): ').strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                break
        except ValueError:
            pass
        print(f'Please enter a number between 1 and {len(results)}.')

    return results[idx][3]


def prompt_rating():
    return input('Rating (e.g. 8/10, or leave blank): ').strip()


def prompt_watched_date():
    val = input('When did you watch it? (YYYY/MM/DD, blank = today, "no" = leave blank): ').strip()
    if val == '':
        return date.today().strftime('%Y-%m-%d')
    elif val.lower() == 'no':
        return ''
    else:
        # Accept YYYY/MM/DD and normalise to YYYY-MM-DD
        return val.replace('/', '-')


def parse_tmdb(html):
    # Title: <h2 ...><a href="...">Title</a> <span class="tag release_date">(YEAR)</span></h2>
    title_match = re.search(
        r'<h2[^>]*>\s*<a[^>]*>([^<]+)</a>\s*<span class="tag release_date">',
        html
    )
    title = title_match.group(1).strip() if title_match else 'Unknown'

    # Year: (YYYY) in release_date span
    year_match = re.search(r'<span class="tag release_date">\((\d{4})\)</span>', html)
    year = year_match.group(1) if year_match else 'Unknown'

    # Genres: <span class="genres"><a ...>Genre</a>, ...</span>
    genres_match = re.search(r'<span class="genres">(.*?)</span>', html, re.DOTALL)
    genres = []
    if genres_match:
        genres = [
            g.strip().lower()
            for g in re.findall(r'<a[^>]*>([^<]+)</a>', genres_match.group(1))
        ]

    # Directors: from <ol class="people no_image"> where character == "Director"
    crew_match = re.search(r'<ol class="people no_image">(.*?)</ol>', html, re.DOTALL)
    directors = []
    if crew_match:
        for profile in re.findall(r'<li class="profile">(.*?)</li>', crew_match.group(1), re.DOTALL):
            char_match = re.search(r'<p class="character">([^<]+)</p>', profile)
            name_match = re.search(r'<p>\s*<a[^>]*>([^<]+)</a>\s*</p>', profile)
            if char_match and name_match and 'Director' in [r.strip() for r in char_match.group(1).split(',')]:
                directors.append(name_match.group(1).strip())

    # Top 5 cast: from <ol class="people scroller"> (top-billed cast section)
    cast = []
    cast_match = re.search(r'<ol class="people scroller">(.*?)</ol>', html, re.DOTALL)
    if cast_match:
        for card in re.findall(r'<li class="card">(.*?)</li>', cast_match.group(1), re.DOTALL):
            name_match = re.search(r'<p>\s*<a[^>]*>([^<]+)</a>\s*</p>', card)
            if name_match:
                cast.append(name_match.group(1).strip())
            if len(cast) >= 5:
                break

    # Fallback: try alternate cast section pattern
    if not cast:
        cast_section = re.search(
            r'Top Billed Cast.*?<ol[^>]*>(.*?)</ol>',
            html, re.DOTALL
        )
        if cast_section:
            for card in re.findall(r'<li[^>]*>(.*?)</li>', cast_section.group(1), re.DOTALL):
                name_match = re.search(r'<p>\s*<a[^>]*>([^<]+)</a>\s*</p>', card)
                if name_match:
                    cast.append(name_match.group(1).strip())
                if len(cast) >= 5:
                    break

    return title, year, genres, directors, cast


def build_entry(title, year, genres, directors, cast, rating='', finished=''):
    lines = [
        '---',
        f'year: {year}',
        f'finished: {finished}',
        'genre:',
    ]
    for g in genres:
        lines.append(f'  - {g}')
    lines.append('directors:')
    for d in directors:
        lines.append(f'  - {d}')
    lines.append('cast:')
    for c in cast:
        lines.append(f'  - {c}')
    lines += [
        f'rating: {rating}',
        'tags:',
        '  - movie',
        '---',
    ]
    return '\n'.join(lines) + '\n'


def sanitize_filename(title):
    name = re.sub(r'[<>:"/\\|?*]', '', title)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


MOVIES_DIR = os.environ.get('OBSIDIAN_MOVIES_DIR', os.path.expanduser('~/Documents/naek/movies'))


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        # Search mode: no URL provided
        url = prompt_search()
        rating = prompt_rating()
        finished = prompt_watched_date()
    else:
        url = sys.argv[1]
        rating = ''
        finished = date.today().strftime('%Y-%m-%d')

    print(f'Fetching {url} ...', file=sys.stderr)

    try:
        html = fetch_html(url)
    except Exception as e:
        print(f'Error fetching URL: {e}', file=sys.stderr)
        sys.exit(1)

    title, year, genres, directors, cast = parse_tmdb(html)

    print(f'Title    : {title} ({year})', file=sys.stderr)
    print(f'Genres   : {", ".join(genres) or "(none found)"}', file=sys.stderr)
    print(f'Directors: {", ".join(directors) or "(none found)"}', file=sys.stderr)
    print(f'Cast     : {", ".join(cast) or "(none found)"}', file=sys.stderr)

    if not cast:
        print('Warning: cast section not found — page structure may have changed.', file=sys.stderr)

    content = build_entry(title, year, genres, directors, cast, rating, finished)

    filename = sanitize_filename(title)
    filepath = os.path.join(MOVIES_DIR, f'{filename}.md')

    if os.path.exists(filepath):
        print(f'File already exists: {filepath}', file=sys.stderr)
        sys.exit(1)

    os.makedirs(MOVIES_DIR, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

    print(f'Created: {filepath}')


if __name__ == '__main__':
    main()
