import requests
from config.settings import load_settings

def fetch_companies(after: str | None, limit: int):
    
    settings = load_settings()

    if not settings.get("HUBSPOT_ACCESS_TOKEN"):
        raise RuntimeError("HUBSPOT_ACCESS_TOKEN is missing")

    url = "https://api.hubapi.com/crm/v3/objects/companies"

    headers = {
        "Authorization": f"Bearer {settings['HUBSPOT_ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }

    params = {
        "limit": limit
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