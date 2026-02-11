from dotenv import load_dotenv
import os

load_dotenv(override=True)

def load_settings():
    return {
        "HUBSPOT_ACCESS_TOKEN": os.getenv("HUBSPOT_ACCESS_TOKEN"),
        "MONDAY_API_TOKEN": os.getenv("MONDAY_API_TOKEN"),
        "HUBSPOT_PAGE_LIMIT": int(os.getenv("HUBSPOT_PAGE_LIMIT", 20)),
        "MONDAY_COMPANY_BOARD_ID": os.getenv("MONDAY_COMPANY_BOARD_ID")
    }
