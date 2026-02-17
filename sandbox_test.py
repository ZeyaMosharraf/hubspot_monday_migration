from clients.hubspot_client import fetch_object
from config.hubspot_columns import hubspot_properties
from config.settings import load_settings


def run_test():
    settings = load_settings()

    hubspot_result, next_after = fetch_object(
        object_type="2-54742785",
        properties=hubspot_properties,
        after=None, 
        limit=20
    )

    print("Fetched:", len(hubspot_result))
    print("Next cursor:", next_after)
    print("First record:", hubspot_result[0] if hubspot_result else None)


if __name__ == "__main__":
    run_test()