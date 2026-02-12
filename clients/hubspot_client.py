import requests
from config.settings import load_settings
from config.hubspot_columns import hubspot_properties

def fetch_companies(after: str | None, limit: int):
    
    settings = load_settings()

    if not settings.get("HUBSPOT_ACCESS_TOKEN"):
        raise RuntimeError("HUBSPOT_ACCESS_TOKEN is missing")

    if not hubspot_properties:
        raise RuntimeError("HUBSPOT_COMPANY_PROPERTIES is empty")

    url = "https://api.hubapi.com/crm/v3/objects/companies"

    headers = {
        "Authorization": f"Bearer {settings['HUBSPOT_ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }

    params = {
        "limit": limit,
        "properties": hubspot_properties
    }

    if after:
        params["after"] = after

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()

    companies = data.get("results", [])

    paging = data.get("paging", {})
    next_after = paging.get("next", {}).get("after")

    return companies, next_after
