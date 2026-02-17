from config.settings import load_settings
from clients.hubspot_client import fetch_object
from transformers.company_mapper import transform_company
from clients.monday_client import upsert_company
from state.checkpoint import load_checkpoint, save_checkpoint
from config.monday_columns import monday_company_columns
from config.hubspot_columns import hubspot_properties


def run_migration():
    settings = load_settings()

    after = load_checkpoint() or None

    total_processed = 0

    print(f"Starting migration from cursor: {after}")

    while True:
        hubspot_result, next_after = fetch_object(
            object_type="2-54742785",
            properties=hubspot_properties,
            after=after,
            limit=settings["HUBSPOT_PAGE_LIMIT"]
        )

        if not hubspot_result:
            print("No more companies to process.")
            break

        for hubspot_result in hubspot_result:
            mapped_company = transform_company(hubspot_result)

            result = upsert_company(mapped_company)

            total_processed += 1

            if result == "created":
                total_created += 1
            elif result == "updated":
                total_updated += 1

        save_checkpoint(next_after)

        print(f"Processed batch of {len(hubspot_result)}. Next cursor: {next_after}")

        if not next_after:
            print("Reached end of HubSpot data.")
            break
        save_checkpoint(next_after)
        after = next_after

    print("\n===== MIGRATION SUMMARY =====")
    print(f"Total processed: {total_processed}")
    print(f"Created: {total_created}")
    print(f"Updated: {total_updated}")
    print("Migration completed successfully.")

if __name__ == "__main__":
    run_migration()
