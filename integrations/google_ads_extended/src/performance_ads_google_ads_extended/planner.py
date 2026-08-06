"""Bounded Keyword Plan Idea Service adapter."""

from __future__ import annotations

from collections.abc import Iterable
from urllib.parse import urlparse

from google.ads.googleads.client import GoogleAdsClient


_MAX_SEEDS = 20
_MAX_RESULTS = 1000


def _clean_keywords(keywords: Iterable[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for keyword in keywords:
        value = " ".join(keyword.split()).strip()
        key = value.casefold()
        if value and key not in seen:
            cleaned.append(value)
            seen.add(key)
    if len(cleaned) > _MAX_SEEDS:
        raise ValueError(f"use no maximo {_MAX_SEEDS} seeds por chamada")
    return cleaned


def _clean_url(page_url: str | None) -> str | None:
    if not page_url:
        return None
    parsed = urlparse(page_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("page_url deve ser uma URL http ou https valida")
    if parsed.username or parsed.password:
        raise ValueError("page_url nao pode conter credenciais")
    return page_url.strip()


def _competition_name(value: object) -> str | None:
    name = getattr(value, "name", None)
    return str(name) if name else None


def generate_keyword_ideas(
    client: GoogleAdsClient,
    *,
    customer_id: str,
    keywords: Iterable[str],
    page_url: str | None,
    location_ids: Iterable[str],
    language_id: str,
    network: str,
    limit: int,
) -> list[dict[str, object]]:
    """Generate bounded keyword ideas and historical metrics."""

    seeds = _clean_keywords(keywords)
    url = _clean_url(page_url)
    if not seeds and not url:
        raise ValueError("informe ao menos uma keyword seed ou page_url")
    if limit < 1 or limit > _MAX_RESULTS:
        raise ValueError(f"limit deve estar entre 1 e {_MAX_RESULTS}")

    normalized_locations = [str(int(item)) for item in location_ids]
    normalized_language = str(int(language_id))
    network_name = network.strip().upper()
    if network_name not in {"GOOGLE_SEARCH", "GOOGLE_SEARCH_AND_PARTNERS"}:
        raise ValueError(
            "network deve ser GOOGLE_SEARCH ou GOOGLE_SEARCH_AND_PARTNERS"
        )

    google_ads_service = client.get_service("GoogleAdsService")
    planner_service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = google_ads_service.language_constant_path(
        int(normalized_language)
    )
    request.geo_target_constants.extend(
        google_ads_service.geo_target_constant_path(int(location_id))
        for location_id in normalized_locations
    )
    request.include_adult_keywords = False
    request.keyword_plan_network = getattr(
        client.enums.KeywordPlanNetworkEnum, network_name
    )

    if seeds and url:
        request.keyword_and_url_seed.keywords.extend(seeds)
        request.keyword_and_url_seed.url = url
    elif seeds:
        request.keyword_seed.keywords.extend(seeds)
    else:
        request.url_seed.url = url

    response = planner_service.generate_keyword_ideas(request=request)
    output: list[dict[str, object]] = []
    for idea in response:
        metrics = idea.keyword_idea_metrics
        output.append(
            {
                "keyword": idea.text,
                "avg_monthly_searches": metrics.avg_monthly_searches,
                "competition": _competition_name(metrics.competition),
                "competition_index": metrics.competition_index,
                "low_top_of_page_bid_micros": metrics.low_top_of_page_bid_micros,
                "high_top_of_page_bid_micros": metrics.high_top_of_page_bid_micros,
                "monthly_search_volumes": [
                    {
                        "year": monthly.year,
                        "month": _competition_name(monthly.month),
                        "monthly_searches": monthly.monthly_searches,
                    }
                    for monthly in metrics.monthly_search_volumes
                ],
            }
        )
        if len(output) >= limit:
            break
    return output
