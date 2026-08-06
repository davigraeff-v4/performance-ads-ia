"""MCP entrypoint with fail-closed capability gates."""

from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations

from . import __version__
from .client import get_google_ads_client
from .config import ConfigurationError, Settings
from .planner import generate_keyword_ideas as planner_generate_keyword_ideas


mcp = FastMCP("PERFORMANCE ADS IA - Google Ads Extended")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_extended_capabilities() -> dict[str, object]:
    """Return sanitized runtime gates without returning credential or customer values."""

    try:
        settings = Settings.from_environment()
        return {"server_version": __version__, **settings.public_capabilities()}
    except ConfigurationError as error:
        raise ToolError(str(error)) from error


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def generate_keyword_ideas(
    customer_id: str,
    keywords: list[str] = [],
    page_url: str | None = None,
    location_ids: list[str] = [],
    language_id: str = "1014",
    network: str = "GOOGLE_SEARCH",
    limit: int = 100,
) -> list[dict[str, object]]:
    """Generate official Google Ads keyword ideas and historical metrics.

    This tool stays blocked unless keyword_planning is declared locally,
    planner access is explicitly enabled, and the customer is allowlisted.
    Customer, location and language IDs must contain digits only; hyphens in
    customer IDs are normalized locally.
    """

    try:
        settings = Settings.from_environment()
        normalized_customer = settings.require_planner(customer_id)
        client = get_google_ads_client()
        return planner_generate_keyword_ideas(
            client,
            customer_id=normalized_customer,
            keywords=keywords,
            page_url=page_url,
            location_ids=location_ids,
            language_id=language_id,
            network=network,
            limit=limit,
        )
    except Exception as error:
        # Tool errors expose only the exception message, never environment values.
        raise ToolError(str(error)) from error


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
