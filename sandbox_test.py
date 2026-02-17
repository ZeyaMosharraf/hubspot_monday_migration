from config.settings import load_settings
from config.monday_columns import monday_company_columns
from clients.monday_client import upsert_item


def run_test():
    settings = load_settings()

    dummy = {
        "item_name": "Universal Test",
        "unique_value": "999999",
        "columns": {
            "hubspot_id": "999999",
            "phone": "12345",
            "industry": "Software",
            "company_domain": "https://example.com",
            "city": "Delhi",
            "country": "India",
            "created_date": "2025-12-18"
        }
    }

    response = upsert_item(
        board_id=settings["MONDAY_COMPANY_BOARD_ID"],
        unique_column_id=monday_company_columns["hubspot_id"],
        column_mapping=monday_company_columns,
        item_data=dummy
    )

    print(response)


if __name__ == "__main__":
    run_test()
