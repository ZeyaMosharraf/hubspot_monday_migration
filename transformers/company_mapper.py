from config.monday_columns import monday_company_columns
def transform_company(hubspot_company: dict) -> dict:
    props = hubspot_company.get("properties", {})

    mapped = {}

    for hubspot_field, monday_column in monday_company_columns.items():
        if hubspot_field == "hubspot_id":
            mapped[monday_column] = hubspot_company.get("id")
        else:
            mapped[monday_column] = props.get(hubspot_field)

    return mapped
