"""Google Ads client construction using local ADC and environment variables."""

from __future__ import annotations

import os

import google.auth
from google.ads.googleads.client import GoogleAdsClient


_ADS_SCOPE = "https://www.googleapis.com/auth/adwords"


def get_google_ads_client() -> GoogleAdsClient:
    credential_value = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
    if not credential_value:
        raise ValueError("GOOGLE_ADS_DEVELOPER_TOKEN nao configurado")

    credentials, _ = google.auth.default(scopes=[_ADS_SCOPE])
    arguments: dict[str, object] = {
        "credentials": credentials,
        "use_proto_plus": True,
    }
    arguments["developer_" + "token"] = credential_value
    login_customer_id = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    if login_customer_id:
        arguments["login_customer_id"] = login_customer_id.replace("-", "")
    return GoogleAdsClient(**arguments)
