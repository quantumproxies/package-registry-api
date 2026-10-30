"""Package Registry API: Package registry API for Python and the command line: npm, crates.io and Docker Hub search, PyPI package metadata, Hacker News stories and Stack Overflow questions in one client, with one sign-in and the same JSON or CSV rows for every source. Free and open source; runs on your QuanticData account.

    from quanticdata_package_registry_api import PackageRegistry

    scraper = PackageRegistry()   # saved login (`package-registry login`) or QUANTICDATA_API_KEY
    run = scraper.npm(...)   # npm registry search
    run = scraper.pypi(...)   # PyPI package metadata by name
    run = scraper.crates(...)   # crates.io search for Rust crates
    run = scraper.docker(...)   # Docker Hub image search and repository stats
    run = scraper.hackernews(...)   # Hacker News stories by search or the front page
    run = scraper.stackoverflow(...)   # Stack Overflow and Stack Exchange questions
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["PackageRegistry", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class PackageRegistry:
    """Package Registry API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="package-registry/0.1.0 (+https://github.com/quantumproxies/package-registry-api)", timeout=timeout)

    def npm(
        self, query: str,
        *,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Search the npm registry: name, latest version, description, license, weekly and monthly downloads, dependents, maintainers and links.

        Args:
            query: Search text: a package name, words, keywords:web-scraping, author:NAME or a scope, e.g. "react state management".
            max_results: How many packages to deliver at most (1–100). You pay only for delivered packages.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per package: see ``types.NpmPackagesRow``.
        """
        payload = {
            "query": query,
            "max_results": max_results,
        }
        return self.client.run_collector("npm_packages", payload, wait=wait, timeout=timeout)

    def pypi(
        self, packages: Union[str, Sequence[str]],
        *,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Python package metadata from PyPI — version, summary, license, Python support, links.

        Args:
            packages: PyPI package names, e.g. requests, numpy.
            max_results: How many packages to deliver at most (1–50). You pay only for delivered packages.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per package: see ``types.PypiPackagesRow``.
        """
        payload = {
            "packages": _as_list(packages),
            "max_results": max_results,
        }
        return self.client.run_collector("pypi_packages", payload, wait=wait, timeout=timeout)

    def crates(
        self, query: str,
        *,
        sort: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Rust package search from the crates.io registry — downloads, versions, links.

        Args:
            query: Crate name or keyword.
            sort: Result order. One of: relevance, downloads, recent_downloads, recent_updates, new.
            max_results: How many crates to deliver at most (1–100). You pay only for delivered crates.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per crate: see ``types.CratesIoRow``.
        """
        payload = {
            "query": query,
            "sort": sort,
            "max_results": max_results,
        }
        return self.client.run_collector("crates_io", payload, wait=wait, timeout=timeout)

    def docker(
        self, query: Optional[str] = None,
        *,
        images: Optional[Union[str, Sequence[str]]] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Docker image search and repository stats — stars, pulls, official flag.

        Args:
            query: Image search text, e.g. postgres. Leave it out when you pass --images.
            images: Exact image references for detail lookups, e.g. redis or bitnami/postgresql.
            max_results: How many images to deliver at most (1–100). You pay only for delivered images.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per image: see ``types.DockerHubRow``.
        """
        payload = {
            "query": query,
            "images": _as_list(images),
            "max_results": max_results,
        }
        return self.client.run_collector("docker_hub", payload, wait=wait, timeout=timeout)

    def hackernews(
        self, query: Optional[str] = None,
        *,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Hacker News stories for a search query, or the current front page: title, link, points, comment count, author and dates.

        Args:
            query: What to search, e.g. "web scraping". Omit it for the current front page.
            type: Story type filter (default: story when searching, front_page otherwise). One of: story, ask_hn, show_hn, front_page.
            sort: relevance (default when searching) or date (newest first). One of: relevance, date.
            max_results: How many stories to deliver at most (1–200). You pay only for delivered stories.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per story: see ``types.HackerNewsRow``.
        """
        payload = {
            "query": query,
            "type": type,
            "sort": sort,
            "max_results": max_results,
        }
        return self.client.run_collector("hacker_news", payload, wait=wait, timeout=timeout)

    def stackoverflow(
        self, query: Optional[str] = None,
        *,
        tags: Optional[str] = None,
        site: Optional[str] = None,
        sort: Optional[str] = None,
        include_body: Optional[bool] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Questions from Stack Overflow and other Stack Exchange sites, by keyword or tag: score, answers, views, accepted answer, tags, license and, with --include-body, the question text.

        Args:
            query: Keyword to search in titles and bodies, e.g. "web scraping".
            tags: Semicolon-separated tags, e.g. python;asyncio.
            site: Stack Exchange site (default stackoverflow). One of: stackoverflow, superuser, serverfault, askubuntu, mathoverflow, unix, dba, security, datascience.
            sort: Sort order. Default: relevance when a query is given, votes for a tag-only listing. One of: votes, activity, creation, relevance.
            include_body: Also deliver the question body as plain text (same call, larger rows).
            max_results: How many questions to deliver at most (1–100). You pay only for delivered questions.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per question: see ``types.StackoverflowRow``.
        """
        payload = {
            "query": query,
            "tags": tags,
            "site": site,
            "sort": sort,
            "include_body": include_body,
            "max_results": max_results,
        }
        return self.client.run_collector("stackoverflow", payload, wait=wait, timeout=timeout)
