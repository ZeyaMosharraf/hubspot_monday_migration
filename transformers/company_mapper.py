
def transform_company(hubspot_company: dict) -> dict:
    props = hubspot_company.get("properties", {})

    return {
        "hubspot_id": hubspot_company.get("id"),
        "item_name": props.get("name"),
        "phone": props.get("phone"),
        "industry": props.get("industry"),
        "company_domain": props.get("domain"),
        "city": props.get("city"),
        "country": props.get("country"),
        "Created_date": props.get("createdate")
    }
