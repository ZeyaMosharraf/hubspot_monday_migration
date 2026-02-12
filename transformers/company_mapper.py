from datetime import datetime

def transform_company(hubspot_company: dict) -> dict:
    props = hubspot_company.get("properties", {})

    raw_created = props.get("createdate")
    formatted_date = None

    if raw_created:
        try:
            dt = datetime.fromisoformat(raw_created.replace("Z", "+00:00"))
            formatted_date = dt.strftime("%Y-%m-%d")
        except Exception:
            formatted_date = None

    return {
        "hubspot_id": hubspot_company.get("id"),
        "item_name": props.get("name"),
        "phone": props.get("phone"),
        "industry": props.get("industry"),
        "company_domain": props.get("domain"),
        "city": props.get("city"),
        "country": props.get("country"),
        "Created_date": formatted_date
    }


# if __name__ == "__main__":
#     sample = {
#         "id": "123",
#         "properties": {
#             "name": "Test Company",
#             "phone": "999999",
#             "industry": "Software",
#             "domain": "example.com",
#             "city": "Delhi",
#             "country": "India",
#             "createdate": "2026-02-03T09:03:12.137Z"
#         }
#     }

#     result = transform_company(sample)
#     print(result)
