from config.settings import load_settings
from clients.hubspot_client import fetch_companies
from transformers.company_mapper import transform_company
from clients.monday_client import upsert_company
from state.checkpoint import load_checkpoint, save_checkpoint
from config.monday_columns import monday_company_columns
# from schema.monday_schema import alter_dropdown_add_label

def run_migration():
    settings = load_settings()

    after = load_checkpoint()

    print(f"Starting migration from cursor: {after}")

    while True:
        companies, next_after = fetch_companies(
            after=after,
            limit=settings["HUBSPOT_PAGE_LIMIT"]
        )

        if not companies:
            print("No more companies to process.")
            break

        for company in companies:
            mapped_company = transform_company(company)
            upsert_company(mapped_company)

        save_checkpoint({"after": next_after})

        print(f"Processed batch. Next cursor: {next_after}")

        if not next_after:
            print("Reached end of HubSpot data.")
            break

        after = next_after

    print("Migration completed successfully.")

if __name__ == "__main__":
    run_migration()
