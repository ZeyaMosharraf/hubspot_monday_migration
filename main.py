from config.settings import load_settings
from clients.hubspot_client import fetch_companies
from transformers.company_mapper import map_company
from clients.monday_client import upsert_company
from state.checkpoint import load_checkpoint, save_checkpoint


def run_migration():
    settings = load_settings()

    checkpoint = load_checkpoint()
    offset = checkpoint.get("offset", 0)

    print(f"Starting migration from offset: {offset}")

    while True:
        companies, has_more = fetch_companies(
            offset=offset,
            limit=settings["HUBSPOT_PAGE_LIMIT"]
        )

        if not companies:
            print("No more companies to process.")
            break

        for company in companies:
            mapped_company = map_company(company)
            upsert_company(mapped_company)

        offset += settings["HUBSPOT_PAGE_LIMIT"]
        save_checkpoint({"offset": offset})

        print(f"Processed batch. New offset: {offset}")

        if not has_more:
            print("Reached end of HubSpot data.")
            break

    print("Migration completed successfully.")


if __name__ == "__main__":
    run_migration()
