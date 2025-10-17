# HeyMax Data Extraction Pipeline

Python tooling that classifies URLs from popular social platforms and pulls the associated transcript text. The pipeline currently supports YouTube, Instagram reels, and TikTok videos via a mix of direct APIs and Apify actors.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) or `pip` for dependency management
- Apify API token with access to the following actors:
  - `agentx/video-transcript` (Instagram)
  - `clockworks/tiktok-scraper` (TikTok)
  - Any additional actors you enable in `scraper/`

## Project Setup

1. Clone the repository and move into the project directory.
2. Create a virtual environment:
	```bash
	uv venv  # or: python -m venv .venv
	```
3. Activate the environment and install dependencies:
	```bash
	source .venv/bin/activate
	uv sync
	```
	If you prefer `pip`:
	```bash
	pip install -e .
	```
4. Provide credentials in a `.env` file located at the project root (or inside `.venv/.env`):
	```env
	APIFY_TOKEN=apify_api_xxx
	```
	The Instagram actor does not require extra tokens, but if you modify the code to use other services, add those keys here as well.

## Running the Extraction Pipeline

The entry point is `main.py`. You can run it with a URL argument or interactively:

```bash
uv run main.py "https://www.instagram.com/reel/<id>"
```

Pipeline flow:

1. `utils/link_classifier.py` determines whether the URL is YouTube, Instagram, TikTok, or unknown.
2. The appropriate extractor in `scraper/` fetches transcript data:
	- `scraper/youtube_extracter.py` uses `youtube-transcript-api`.
	- `scraper/instagram_extractor.py` triggers the Apify `agentx/video-transcript` actor.
	- `scraper/tiktok_extractor.py` relies on Apify metadata and subtitle downloads.
3. Results are saved under `output/<platform>-<timestamp>.json` for review or downstream processing.

## Validating the Setup

After installing dependencies and configuring `APIFY_TOKEN`, run a smoke test to confirm end-to-end execution:

```bash
uv run main.py "https://www.tiktok.com/@example/video/<id>"
uv run main.py "https://www.instagram.com/reel/<id>"
uv run main.py "https://www.youtube.com/watch?v=<id>"
```

Each command should print classification logs, fetch the transcript, and drop a JSON file into `output/`. Inspect the saved files to verify the returned `text` and metadata.

