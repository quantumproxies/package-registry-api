# Package Registry API

[![ci](https://github.com/quantumproxies/package-registry-api/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/package-registry-api/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Developer data from Python or the command line: npm search with weekly downloads and dependents, PyPI package metadata with dependencies and supported Python versions, crates.io search with download counts, Docker Hub images with pulls and stars, Hacker News stories and Stack Overflow questions, as JSON or CSV. The code is free and open source (MIT). Each of these registries and sites publishes its own API; this package puts all six behind one client and one QuanticData sign-in, returns the same flat rows and CSV export for every source, retries on rate limits and dropped connections, and runs long jobs in the background.

```bash
pip install git+https://github.com/quantumproxies/package-registry-api
package-registry login
package-registry npm "react state management" --max-results 20 -o npm.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `package-registry npm` | search text | Version, license, weekly and monthly downloads, dependents, links, 21 fields per row ([fields and price](https://quanticdata.io/collectors/npm-registry-api/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api)) | up to 100 |
| `package-registry pypi` | package names | Version, license, Python support, dependencies, releases, links, 24 fields per row ([fields and price](https://quanticdata.io/collectors/pypi-api/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api)) | up to 50 |
| `package-registry crates` | crate name or keyword | Version, all-time and 90-day downloads, dates, docs and repository links, 17 fields per row ([fields and price](https://quanticdata.io/collectors/crates-io-api/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api)) | up to 100 |
| `package-registry docker` | search text, or --images | Stars, pulls, official flag, description, pull command, 15 fields per row ([fields and price](https://quanticdata.io/collectors/docker-hub-api/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api)) | up to 100 |
| `package-registry hackernews` | search text (optional) | Title, link, points, comments, author, dates, 14 fields per row ([fields and price](https://quanticdata.io/collectors/hacker-news-api/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api)) | up to 200 |
| `package-registry stackoverflow` | keyword, or --tags | Score, answers, views, accepted answer, tags, license, 22 fields per row ([fields and price](https://quanticdata.io/collectors/stack-overflow-api/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api)) | up to 100 |

`stackoverflow` also reads Super User, Server Fault, Ask Ubuntu, MathOverflow, Unix, DBA, Security and Data Science with `--site`, and filters by tag with `--tags "python;asyncio"`. `hackernews` sorts by relevance or date and keeps only Ask HN or Show HN posts with `--type`; `crates` sorts by relevance, downloads, recent downloads, recent updates or newest; `docker` reads exact images with `--images redis bitnami/postgresql`.

## Sample output

A real row from `package-registry npm "react state management" --max-results 3` (2026-10-23):

```json
{
  "name": "unstated-next",
  "rank": 1,
  "license": "MIT",
  "npm_url": "https://www.npmjs.com/package/unstated-next",
  "version": "1.1.0",
  "bugs_url": null,
  "homepage": null,
  "insecure": false,
  "keywords": [],
  "publisher": "thejameskyle",
  "dependents": 257,
  "repository": null,
  "description": "200 bytes to never think about React state management libraries ever again",
  "maintainers": [
    "thejameskyle"
  ],
  "published_at": "2019-05-13T23:34:47.580Z",
  "search_score": 382.99,
  "quality_score": 1,
  "downloads_weekly": 85141,
  "popularity_score": 1,
  "downloads_monthly": 500976,
  "maintenance_score": 1
}
```

## Python

```python
from quanticdata_package_registry_api import PackageRegistry

registry = PackageRegistry()  # saved login, or QUANTICDATA_API_KEY

found = registry.npm("react state management", max_results=20)
for p in found:
    print(p["name"], p["version"], p["downloads_weekly"], p["dependents"])

meta = registry.pypi(["requests", "numpy", "fastapi"])
for p in meta:
    print(p["name"], p["version"], p["requires_python"], len(p["dependencies"]))

crates = registry.crates("http client", sort="downloads", max_results=10)
crates.to_csv("rust_http_clients.csv")

stories = registry.hackernews("sqlite", sort="date", max_results=30)
questions = registry.stackoverflow(tags="python;asyncio", sort="votes", max_results=30)
print(stories.rows[0]["title"], questions.rows[0]["title"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Dependency audit**: Read a requirements.txt and get, for every package, the latest version on PyPI next to the one you pin, the Python versions it needs, the yanked flag and the known vulnerabilities PyPI lists. See [`examples/dependency_audit.py`](examples/dependency_audit.py).
- **npm landscape for a need**: Search npm with a few phrases, merge the results into one list and sort it by weekly downloads, with the phrases that found each package. See [`examples/npm_landscape.py`](examples/npm_landscape.py).
- **What developers say about a tool**: Put the Hacker News stories and the Stack Overflow questions about a library side by side, with score, replies, date and link. See [`examples/tech_mentions.py`](examples/tech_mentions.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `package-registry run <id> -o out.csv` collects it later.

### `package-registry npm`

Search the npm registry: name, latest version, description, license, weekly and monthly downloads, dependents, maintainers and links.

```
package-registry npm QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Search text: a package name, words, keywords:web-scraping, author:NAME or a scope, e.g. "react state management". |
| `--max-results` | integer | `20` | How many packages to deliver at most (1–100). You pay only for delivered packages. |

### `package-registry pypi`

Python package metadata from PyPI — version, summary, license, Python support, links.

```
package-registry pypi PACKAGES [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `PACKAGES` | string[] |  | PyPI package names, e.g. requests, numpy. |
| `--max-results` | integer | `10` | How many packages to deliver at most (1–50). You pay only for delivered packages. |

### `package-registry crates`

Rust package search from the crates.io registry — downloads, versions, links.

```
package-registry crates QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Crate name or keyword. |
| `--sort` | relevance / downloads / recent_downloads / recent_updates / new | `relevance` | Result order. |
| `--max-results` | integer | `25` | How many crates to deliver at most (1–100). You pay only for delivered crates. |

### `package-registry docker`

Docker image search and repository stats — stars, pulls, official flag.

```
package-registry docker [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Image search text, e.g. postgres. Leave it out when you pass --images. |
| `--images` | string[] |  | Exact image references for detail lookups, e.g. redis or bitnami/postgresql. |
| `--max-results` | integer | `25` | How many images to deliver at most (1–100). You pay only for delivered images. |

### `package-registry hackernews`

Hacker News stories for a search query, or the current front page: title, link, points, comment count, author and dates.

```
package-registry hackernews [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search, e.g. "web scraping". Omit it for the current front page. |
| `--type` | story / ask_hn / show_hn / front_page |  | Story type filter (default: story when searching, front_page otherwise). |
| `--sort` | relevance / date |  | relevance (default when searching) or date (newest first). |
| `--max-results` | integer | `30` | How many stories to deliver at most (1–200). You pay only for delivered stories. |

### `package-registry stackoverflow`

Questions from Stack Overflow and other Stack Exchange sites, by keyword or tag: score, answers, views, accepted answer, tags, license and, with --include-body, the question text.

```
package-registry stackoverflow [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Keyword to search in titles and bodies, e.g. "web scraping". |
| `--tags` | string |  | Semicolon-separated tags, e.g. python;asyncio. |
| `--site` | stackoverflow / superuser / serverfault / askubuntu / mathoverflow / unix / dba / security / datascience | `stackoverflow` | Stack Exchange site (default stackoverflow). |
| `--sort` | votes / activity / creation / relevance |  | Sort order. Default: relevance when a query is given, votes for a tag-only listing. |
| `--include-body` | boolean | `False` | Also deliver the question body as plain text (same call, larger rows). |
| `--max-results` | integer | `30` | How many questions to deliver at most (1–100). You pay only for delivered questions. |

## Output fields

<details><summary><code>package-registry npm</code>: 21 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `name` | string | Package name. |
| `version` | string or null | Latest version. |
| `description` | string or null | Package description. |
| `keywords` | string[] | Declared keywords. |
| `license` | string or null | License (SPDX). |
| `publisher` | string or null | Last publisher. |
| `homepage` | string or null | Homepage URL. |
| `repository` | string or null | Repository URL. |
| `npm_url` | string | npmjs.com package URL. |
| `published_at` | string or null | Last publish (ISO 8601). |
| `quality_score` | number or null | Registry quality score 0–1; null while the registry sends a fixed placeholder (currently 1 for every package). |
| `downloads_weekly` | integer or null | Weekly downloads. |
| `downloads_monthly` | integer or null | Monthly downloads. |
| `dependents` | integer or null | Dependent packages. |
| `maintainers` | string[] | Maintainer usernames. |
| `bugs_url` | string or null | Issue tracker URL. |
| `popularity_score` | number or null | Registry popularity score 0–1; null while the registry sends a fixed placeholder (currently 1 for every package). |
| `maintenance_score` | number or null | Registry maintenance score 0–1; null while the registry sends a fixed placeholder (currently 1 for every package). |
| `search_score` | number or null | Relevance score of this result for the query. |
| `insecure` | boolean | Flagged insecure by the registry. |

</details>

<details><summary><code>package-registry pypi</code>: 24 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `name` | string | Package name. |
| `version` | string or null | Latest version. |
| `summary` | string or null | Short summary. |
| `author` | string or null | Author name(s), never an e-mail address. |
| `license` | string or null | License. |
| `requires_python` | string or null | Required Python version spec. |
| `homepage` | string or null | Homepage URL. |
| `repository` | string or null | Source repository URL. |
| `keywords` | string[] | Declared keywords. |
| `python_versions` | string[] | Supported Python versions (classifiers). |
| `release_count` | integer or null | Number of releases. |
| `url` | string | PyPI project URL. |
| `maintainer` | string or null | Maintainer. |
| `documentation` | string or null | Documentation URL. |
| `changelog` | string or null | Changelog URL. |
| `dependencies` | string[] | Runtime dependencies (requires_dist without extras). |
| `optional_dependencies_count` | integer | Dependencies that belong to an extra. |
| `extras` | string[] | Extras the package provides. |
| `development_status` | string or null | Development status classifier. |
| `released_at` | string or null | Upload time of the current version. |
| `first_release_at` | string or null | Upload time of the first release. |
| `yanked` | boolean | Whether the current version is yanked. |
| `known_vulnerabilities` | integer or null | Known vulnerabilities PyPI lists for the current version. |

</details>

<details><summary><code>package-registry crates</code>: 17 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `name` | string | Crate name. |
| `description` | string or null | Description. |
| `version` | string or null | Latest stable version. |
| `downloads` | integer or null | All-time downloads. |
| `recent_downloads` | integer or null | Downloads in the last 90 days. |
| `created_at` | string or null | First publish. |
| `updated_at` | string or null | Last update. |
| `homepage` | string or null | Homepage. |
| `documentation` | string or null | Docs URL. |
| `repository` | string or null | Repository URL. |
| `exact_match` | boolean | Query matched the name exactly. |
| `url` | string | crates.io page. |
| `newest_version` | string or null | Newest published version, pre-releases included. |
| `versions_count` | integer or null | Number of published versions. |
| `yanked` | boolean | Whether the crate's default version is yanked. |
| `docs_rs_url` | string | docs.rs page. |

</details>

<details><summary><code>package-registry docker</code>: 15 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `name` | string | Image name (namespace/name; officials bare). |
| `description` | string or null | Short description. |
| `stars` | integer or null | Stars. |
| `pulls` | integer or null | Total pulls. |
| `is_official` | boolean | Docker official image. |
| `is_automated` | boolean | Automated build. |
| `last_updated` | string or null | Last push (detail mode only). |
| `url` | string | Docker Hub page. |
| `namespace` | string | Repository namespace (library for official images). |
| `date_registered` | string or null | Repository creation date (lookups). |
| `categories` | string[] | Docker Hub categories (lookups). |
| `storage_size` | integer or null | Bytes stored across all tags (lookups). |
| `status` | string or null | Repository status (lookups). |
| `pull_command` | string | docker pull command. |

</details>

<details><summary><code>package-registry hackernews</code>: 14 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `id` | string | HN item id. |
| `title` | string | Story title. |
| `url` | string or null | Outbound link (null for text posts). |
| `points` | integer or null | Upvotes. |
| `author` | string or null | Submitter. |
| `comments` | integer or null | Comment count. |
| `created_at` | string or null | Submission time (ISO 8601). |
| `text` | string or null | Self-post text (Ask HN), tags stripped. |
| `hn_url` | string | Link to the HN discussion. |
| `tags` | string[] | Index tags (story, show_hn…). |
| `domain` | string or null | Host of the linked page (github.com); null for text posts. |
| `updated_at` | string or null | Last time the story changed in the index (ISO 8601). |
| `type` | string | story, ask_hn, show_hn, job or poll. |

</details>

<details><summary><code>package-registry stackoverflow</code>: 22 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `question_id` | integer | Stack Exchange question id. |
| `title` | string | Question title (entities decoded). |
| `score` | integer or null | Net votes. |
| `answer_count` | integer or null | Number of answers. |
| `view_count` | integer or null | Views. |
| `is_answered` | boolean | Has at least one upvoted answer. |
| `has_accepted_answer` | boolean | An answer is accepted. |
| `tags` | string[] | Question tags. |
| `author` | string or null | Asker display name. |
| `author_reputation` | integer or null | Asker reputation. |
| `created_at` | string or null | Asked at (ISO 8601). |
| `last_activity` | string or null | Last activity (ISO 8601). |
| `link` | string or null | Question permalink. |
| `accepted_answer_id` | integer or null | Id of the accepted answer. |
| `author_id` | integer or null | Asker's user id on that site. |
| `author_url` | string or null | Asker's profile URL. |
| `last_edit` | string or null | Last edit time (ISO 8601). |
| `closed_at` | string or null | When the question was closed (ISO 8601). |
| `closed_reason` | string or null | Why it was closed (Duplicate, Needs more focus…). |
| `license` | string or null | Content license (CC BY-SA 4.0…). |
| `body` | string or null | Question body as plain text — only with include_body. |

</details>

## Sign-in and API keys

- `package-registry login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `package-registry login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `package-registry login --api-key`.
- `package-registry logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/npm_packages/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "react state management", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this package registry API free?**

The code is free and MIT-licensed. Runs go through your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need an API key for each source?**

No. One QuanticData sign-in covers every command and the requests run on QuanticData's side. npm, PyPI, crates.io, Docker Hub, Hacker News and Stack Exchange publish their own APIs; what this package adds is one client for all of them, the same flat rows and CSV, JSON or JSONL export for every source, retries on rate limits and dropped connections, and background runs (`--no-wait`) you collect later with `package-registry run <run_id>`.

**How many rows can one run return?**

Up to 100 npm packages, 50 PyPI packages, 100 crates, 100 Docker images, 200 Hacker News stories or 100 Stack Overflow questions per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as keywords, maintainers, dependencies and tags are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/dependency_audit.py from cron, GitHub Actions or any scheduler.

**What about the usernames in the rows?**

Rows carry the public usernames the sites show (npm publishers and maintainers, Hacker News submitters, Stack Overflow askers), and Stack Exchange content is licensed CC BY-SA, as each row's license field states. You are responsible for respecting each site's terms and the data-protection rules that apply to how you use the data.

## Related scrapers

- [GitHub Repository Search](https://github.com/quantumproxies/github-repo-scraper): GitHub repository search for Python and the command line.
- [Public Data API](https://github.com/quantumproxies/public-data-api): Public data API for Python and the command line.
- [Web Scraper API](https://github.com/quantumproxies/web-scraper-api): Web scraper API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=package-registry-api).
