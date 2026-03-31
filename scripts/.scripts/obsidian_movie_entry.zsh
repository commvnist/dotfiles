OBSIDIAN_MOVIES_DIR="$HOME/Documents/naek/movies"

obsidian_movie_entry() {
  OBSIDIAN_MOVIES_DIR="$OBSIDIAN_MOVIES_DIR" python3 ~/.scripts/obsidian_movie_entry.py "$1"
}
