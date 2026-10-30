"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class NpmPackagesRow(TypedDict, total=False):
    """One row of `package-registry npm` (npm_packages v1.1.1)."""

    rank: int
    """1-based position."""
    name: str
    """Package name."""
    version: Optional[str]
    """Latest version."""
    description: Optional[str]
    """Package description."""
    keywords: List[str]
    """Declared keywords."""
    license: Optional[str]
    """License (SPDX)."""
    publisher: Optional[str]
    """Last publisher."""
    homepage: Optional[str]
    """Homepage URL."""
    repository: Optional[str]
    """Repository URL."""
    npm_url: str
    """npmjs.com package URL."""
    published_at: Optional[str]
    """Last publish (ISO 8601)."""
    quality_score: Optional[float]
    """Registry quality score 0–1; null while the registry sends a fixed placeholder (currently 1 for every package)."""
    downloads_weekly: Optional[int]
    """Weekly downloads."""
    downloads_monthly: Optional[int]
    """Monthly downloads."""
    dependents: Optional[int]
    """Dependent packages."""
    maintainers: List[str]
    """Maintainer usernames."""
    bugs_url: Optional[str]
    """Issue tracker URL."""
    popularity_score: Optional[float]
    """Registry popularity score 0–1; null while the registry sends a fixed placeholder (currently 1 for every package)."""
    maintenance_score: Optional[float]
    """Registry maintenance score 0–1; null while the registry sends a fixed placeholder (currently 1 for every package)."""
    search_score: Optional[float]
    """Relevance score of this result for the query."""
    insecure: bool
    """Flagged insecure by the registry."""

class PypiPackagesRow(TypedDict, total=False):
    """One row of `package-registry pypi` (pypi_packages v1.2.1)."""

    rank: int
    """1-based position."""
    name: str
    """Package name."""
    version: Optional[str]
    """Latest version."""
    summary: Optional[str]
    """Short summary."""
    author: Optional[str]
    """Author name(s), never an e-mail address."""
    license: Optional[str]
    """License."""
    requires_python: Optional[str]
    """Required Python version spec."""
    homepage: Optional[str]
    """Homepage URL."""
    repository: Optional[str]
    """Source repository URL."""
    keywords: List[str]
    """Declared keywords."""
    python_versions: List[str]
    """Supported Python versions (classifiers)."""
    release_count: Optional[int]
    """Number of releases."""
    url: str
    """PyPI project URL."""
    maintainer: Optional[str]
    """Maintainer."""
    documentation: Optional[str]
    """Documentation URL."""
    changelog: Optional[str]
    """Changelog URL."""
    dependencies: List[str]
    """Runtime dependencies (requires_dist without extras)."""
    optional_dependencies_count: int
    """Dependencies that belong to an extra."""
    extras: List[str]
    """Extras the package provides."""
    development_status: Optional[str]
    """Development status classifier."""
    released_at: Optional[str]
    """Upload time of the current version."""
    first_release_at: Optional[str]
    """Upload time of the first release."""
    yanked: bool
    """Whether the current version is yanked."""
    known_vulnerabilities: Optional[int]
    """Known vulnerabilities PyPI lists for the current version."""

class CratesIoRow(TypedDict, total=False):
    """One row of `package-registry crates` (crates_io v1.1.0)."""

    rank: int
    """1-based position."""
    name: str
    """Crate name."""
    description: Optional[str]
    """Description."""
    version: Optional[str]
    """Latest stable version."""
    downloads: Optional[int]
    """All-time downloads."""
    recent_downloads: Optional[int]
    """Downloads in the last 90 days."""
    created_at: Optional[str]
    """First publish."""
    updated_at: Optional[str]
    """Last update."""
    homepage: Optional[str]
    """Homepage."""
    documentation: Optional[str]
    """Docs URL."""
    repository: Optional[str]
    """Repository URL."""
    exact_match: bool
    """Query matched the name exactly."""
    url: str
    """crates.io page."""
    newest_version: Optional[str]
    """Newest published version, pre-releases included."""
    versions_count: Optional[int]
    """Number of published versions."""
    yanked: bool
    """Whether the crate's default version is yanked."""
    docs_rs_url: str
    """docs.rs page."""

class DockerHubRow(TypedDict, total=False):
    """One row of `package-registry docker` (docker_hub v1.1.0)."""

    rank: int
    """1-based position."""
    name: str
    """Image name (namespace/name; officials bare)."""
    description: Optional[str]
    """Short description."""
    stars: Optional[int]
    """Stars."""
    pulls: Optional[int]
    """Total pulls."""
    is_official: bool
    """Docker official image."""
    is_automated: bool
    """Automated build."""
    last_updated: Optional[str]
    """Last push (detail mode only)."""
    url: str
    """Docker Hub page."""
    namespace: str
    """Repository namespace (library for official images)."""
    date_registered: Optional[str]
    """Repository creation date (lookups)."""
    categories: List[str]
    """Docker Hub categories (lookups)."""
    storage_size: Optional[int]
    """Bytes stored across all tags (lookups)."""
    status: Optional[str]
    """Repository status (lookups)."""
    pull_command: str
    """docker pull command."""

class HackerNewsRow(TypedDict, total=False):
    """One row of `package-registry hackernews` (hacker_news v1.1.1)."""

    rank: int
    """1-based position."""
    id: str
    """HN item id."""
    title: str
    """Story title."""
    url: Optional[str]
    """Outbound link (null for text posts)."""
    points: Optional[int]
    """Upvotes."""
    author: Optional[str]
    """Submitter."""
    comments: Optional[int]
    """Comment count."""
    created_at: Optional[str]
    """Submission time (ISO 8601)."""
    text: Optional[str]
    """Self-post text (Ask HN), tags stripped."""
    hn_url: str
    """Link to the HN discussion."""
    tags: List[str]
    """Index tags (story, show_hn…)."""
    domain: Optional[str]
    """Host of the linked page (github.com); null for text posts."""
    updated_at: Optional[str]
    """Last time the story changed in the index (ISO 8601)."""
    type: str
    """story, ask_hn, show_hn, job or poll."""

class StackoverflowRow(TypedDict, total=False):
    """One row of `package-registry stackoverflow` (stackoverflow v1.1.1)."""

    rank: int
    """1-based position."""
    question_id: int
    """Stack Exchange question id."""
    title: str
    """Question title (entities decoded)."""
    score: Optional[int]
    """Net votes."""
    answer_count: Optional[int]
    """Number of answers."""
    view_count: Optional[int]
    """Views."""
    is_answered: bool
    """Has at least one upvoted answer."""
    has_accepted_answer: bool
    """An answer is accepted."""
    tags: List[str]
    """Question tags."""
    author: Optional[str]
    """Asker display name."""
    author_reputation: Optional[int]
    """Asker reputation."""
    created_at: Optional[str]
    """Asked at (ISO 8601)."""
    last_activity: Optional[str]
    """Last activity (ISO 8601)."""
    link: Optional[str]
    """Question permalink."""
    accepted_answer_id: Optional[int]
    """Id of the accepted answer."""
    author_id: Optional[int]
    """Asker's user id on that site."""
    author_url: Optional[str]
    """Asker's profile URL."""
    last_edit: Optional[str]
    """Last edit time (ISO 8601)."""
    closed_at: Optional[str]
    """When the question was closed (ISO 8601)."""
    closed_reason: Optional[str]
    """Why it was closed (Duplicate, Needs more focus…)."""
    license: Optional[str]
    """Content license (CC BY-SA 4.0…)."""
    body: Optional[str]
    """Question body as plain text — only with include_body."""
