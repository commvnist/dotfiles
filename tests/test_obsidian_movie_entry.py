from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / ".scripts"
    / "obsidian_movie_entry.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("obsidian_movie_entry", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


movie_entry = load_module()


CURRENT_SEARCH_HTML = """
<div class="search_results movie ">
  <div class="results flex">
    <div id="52a81d06760ee31fe808b9b7" class="comp:media-card w-full tight">
      <a class="flex w-full" data-media-type="movie" href="/movie/242310-rage">
        <div class="image"></div>
      </a>
      <a class="font-normal" data-media-type="movie" href="/movie/242310-rage">
        <h2 class="font-semibold"><span>Rage</span></h2>
      </a>
      <span class="release_date w-full font-light">May  9, 2014</span>
      <div class="mt-4 line-clamp-2 [&amp;_*]:m-0">
        <p>When the Russian mob kidnaps a daughter, her father seeks justice.</p>
      </div>
    </div>
    <div id="4bc8c993017a3c122d08ffdd" class="comp:media-card w-full tight">
      <a class="flex w-full" data-media-type="movie" href="/movie/27150-silent-rage">
        <div class="image"></div>
      </a>
      <a class="font-normal" data-media-type="movie" href="/movie/27150-silent-rage">
        <h2 class="font-semibold"><span>Silent Rage</span></h2>
      </a>
      <span class="release_date w-full font-light">April  2, 1982</span>
      <div class="mt-4 line-clamp-2 [&amp;_*]:m-0">
        <p>A sheriff pursues a revived killer.</p>
      </div>
    </div>
  </div>
</div>
<div class="search_results tv ">
  <div class="results flex"></div>
</div>
"""


OLD_SEARCH_HTML = """
<div class="search_results movie ">
  <div class="results flex">
    <div id="4f841f31760ee33c310035d6" class="card v4 tight">
      <a href="/movie/101307-rage">
        <h2><span>Rage</span></h2>
      </a>
      <span class="release_date">November 22, 1972</span>
      <div class="overview">
        <p>A rancher fights for accountability.</p>
      </div>
    </div>
  </div>
</div>
"""


class SearchTmdbTests(unittest.TestCase):
    def test_current_tmdb_cards_return_multiple_results_with_years_and_descriptions(self):
        with patch.object(movie_entry, "fetch_html", return_value=CURRENT_SEARCH_HTML):
            results = movie_entry.search_tmdb("rage")

        self.assertEqual(
            results,
            [
                movie_entry.SearchResult(
                    title="Rage",
                    year="2014",
                    description=(
                        "When the Russian mob kidnaps a daughter, "
                        "her father seeks justice."
                    ),
                    url="https://www.themoviedb.org/movie/242310-rage",
                ),
                movie_entry.SearchResult(
                    title="Silent Rage",
                    year="1982",
                    description="A sheriff pursues a revived killer.",
                    url="https://www.themoviedb.org/movie/27150-silent-rage",
                ),
            ],
        )

    def test_search_year_filter_is_not_sent_as_literal_query_text(self):
        seen_urls: list[str] = []

        def fake_fetch(url: str) -> str:
            seen_urls.append(url)
            return CURRENT_SEARCH_HTML

        with patch.object(movie_entry, "fetch_html", side_effect=fake_fetch):
            results = movie_entry.search_tmdb("rage y:2014")

        self.assertEqual(seen_urls, ["https://www.themoviedb.org/search?query=rage"])
        self.assertEqual([result.title for result in results], ["Rage"])
        self.assertEqual([result.year for result in results], ["2014"])

    def test_old_tmdb_cards_remain_supported(self):
        with patch.object(movie_entry, "fetch_html", return_value=OLD_SEARCH_HTML):
            results = movie_entry.search_tmdb("rage")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Rage")
        self.assertEqual(results[0].year, "1972")
        self.assertEqual(results[0].description, "A rancher fights for accountability.")

    def test_year_only_query_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "movie title text"):
            movie_entry.parse_search_query("y:2014")


if __name__ == "__main__":
    unittest.main()
