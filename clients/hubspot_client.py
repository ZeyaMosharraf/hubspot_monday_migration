import requests
from config.settings import load_settings
from config.hubspot_columns import hubspot_properties

def fetch_object(object_type: str, properties: list[str], after: str | None, limit: int):
    
    settings = load_settings()

    if not settings.get("HUBSPOT_ACCESS_TOKEN"):
        raise RuntimeError("HUBSPOT_ACCESS_TOKEN is missing")

    if not hubspot_properties:
        raise RuntimeError("HUBSPOT_OBJECT_PROPERTIES is empty")

    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}"

    headers = {
        "Authorization": f"Bearer {settings['HUBSPOT_ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }

    params = {
        "limit": limit,
        "properties": ",".join(hubspot_properties)
    }

    if after:
        params["after"] = after

    session = requests.Session()

    response = session.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()

    hubspot_result = data.get("results", [])

    paging = data.get("paging", {})
    next_after = paging.get("next", {}).get("after")

    return hubspot_result, next_after
