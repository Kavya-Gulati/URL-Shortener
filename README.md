# URL Shortener (CLI)

A simple command-line URL shortener written in Python. It generates short codes for URLs using SHA-3's SHAKE-256 hash function, stores the mappings in a local JSON file (`data.json`), and lets you resolve codes back into their original URLs. It also tracks how many times each code has been resolved.

## Features

- **Shorten** a URL into a short hash-based code (or provide your own alias)
- **Resolve** a short code back into its original URL
- **List** all previously shortened URL/code pairs, along with resolve counts
- Basic URL validation (must be `http://` or `https://` with a valid host)
- Duplicate detection — shortening the same URL twice returns the existing code
- Persistent local storage via `data.json`

## Requirements

- Python 3.6+ (no external dependencies — only the standard library is used: `hashlib`, `argparse`, `json`, `urllib.parse`)

## Installation

1. Clone or download this repository.
2. Make sure `main.py` is in your working directory.
3. No `pip install` needed — it's dependency-free.

## Usage

The tool is run from the command line via `main.py` and has three subcommands: `shorten`, `resolve`, and `list`.

```bash
python main.py <command> [options]
```

### 1. Shorten a URL

```bash
python main.py shorten <URL> [--alias ALIAS]
```

**Arguments:**
| Argument | Required | Description |
|---|---|---|
| `URL` | Yes | The full URL to shorten (must include `http://` or `https://`) |
| `--alias` | No | A custom code to use instead of an auto-generated one |

**Example:**

```bash
$ python main.py shorten https://www.example.com/some/long/path
```

**Sample output:**

```
--------------- URL shortened successfully ---------------
https://www.example.com/some/long/path ==> a1b2c3d4e5
```

Running the same command again (same URL) will detect the duplicate instead of creating a new entry:

```
----- This URL has already been shortened and stored. -----
https://www.example.com/some/long/path ==> a1b2c3d4e5
```

**Invalid URL example:**

```bash
$ python main.py shorten not-a-real-url
```

```
error: Invalid URL
```

### 2. Resolve a code

```bash
python main.py resolve <code>
```

**Example:**

```bash
$ python main.py resolve a1b2c3d4e5
```

**Sample output:**

```
--------- The code has been resolved into the URL ---------
a1b2c3d4e5 ==> https://www.example.com/some/long/path
This Code has been resolved 1 times
```

**Invalid code example:**

```bash
$ python main.py resolve doesnotexist
```

```
error: The given code is invalid
```

### 3. List all shortened URLs

```bash
python main.py list
```

**Sample output:**

```
--------------- List of shortened URLs ---------------
1.  https://www.example.com/some/long/path ===> a1b2c3d4e5
(It has been resolved 1 times)

2.  https://another-example.com ===> mycode
(It has been resolved 0 times)
```

If no URLs have been shortened yet (i.e. `data.json` doesn't exist):

```
No URls have been shortened yet.
```

## How it works

- Each new URL (without an alias) is hashed using `hashlib.shake_256`, producing a 10-character hex digest (5 bytes) as its short code.
- All mappings are stored in `data.json` in the current working directory, in the form:

```json
{
  "https://www.example.com/some/long/path": {
    "code": "a1b2c3d4e5",
    "count": 1
  }
}
```

- `count` is incremented every time the code is successfully resolved via `resolve`.

## Known Limitations

- **`data.json` location:** the file is created in whatever directory you run the script from, so results are only visible when you run commands from the same folder.
- **Custom aliases on new URLs:** using `--alias` currently only works reliably if the URL has already been shortened once before (it assumes an entry already exists); using it on a brand-new URL can raise a `KeyError`. If you hit this, shorten the URL first without `--alias`, then re-run with it, or edit `data.json` directly.
- **Alias collisions:** the tool does not currently check whether a chosen alias is already in use by another URL.
- **No delete/update commands:** there's currently no way to remove or edit an existing entry from the CLI — you'd need to edit `data.json` manually.

## Project Structure

```
.
├── main.py       # CLI entry point and all logic
└── data.json     # Auto-generated storage file (created on first shorten)
```

## License

No license specified — add one if you plan to distribute this project.
