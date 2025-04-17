# Immich Photostream

There's more on this in [my blogpost](). But A little python script basically syncs the latest photos from my Immich server to a folder on my Mac, almost recreating a Photostream like Apple used to offer. 

## How to run

1.  Install [uv](https://docs.astral.sh/uv/).
2.  Set `IMMICH_API_KEY` and `IMMICH_SERVER` the values you need.
3.  Run `uv run main.py`. (dependencies are inlined for easy of use, `uv` handles those ✌️).
4.  Your latest photos should show up in the `Photostream` folder, which you can symlink or use however you want! 

