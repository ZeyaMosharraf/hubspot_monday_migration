import requests
import json
import time
from config.settings import load_settings
from config.monday_columns import monday_company_columns

def upsert_item(board_id: str, unique_column_id: str, column_mapping: dict, item_data: dict):
    settings = load_settings()

    token = settings.get("MONDAY_API_TOKEN")
    board_id = settings.get("MONDAY_COMPANY_BOARD_ID")

    if not token:
        raise RuntimeError("MONDAY_API_TOKEN is missing")
    if not board_id:
        raise RuntimeError("MONDAY_COMPANY_BOARD_ID is missing")

    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "API-Version": "2023-10"
    }

    column_values = {}

    for key, value in item_data["columns"].items():
        if value is None:
            continue

        column_id = column_mapping.get(key)

        if not column_id:
            continue

        if key.endswith("_domain"):
            column_values[column_id] = {
                "url": value,
                "text": value.replace("https://", "").replace("http://", "")
            }
        else:
            column_values[column_id] = value

    column_values = {k: v for k, v in column_values.items() if v is not None}

    search_query = """
    query ($board_id: ID!, $column_id: String!, $value: [String]!) {
      items_page_by_column_values (board_id: $board_id, 
                                   columns: [{column_id: $column_id, 
                                    column_values: $value}]) {
        items {
          id
        }
      }
    }
    """
    
    search_vars = {
        "board_id": board_id,
        "column_id": unique_column_id,
        "value": [str(item_data["unique_value"])]
    }

    search_response = requests.post(url, 
                                    headers=headers, 
                                    json={"query": search_query, 
                                          "variables": search_vars}, 
                                    timeout=30)
    
    search_response.raise_for_status()
    search_data = search_response.json()

    if "errors" in search_data:
        raise RuntimeError(f"Monday Search Error: {search_data['errors']}")

    items = search_data.get("data", {}).get("items_page_by_column_values", {}).get("items", [])

    if items:
        item_id = items[0]["id"]
        mutation = """
        mutation ($board_id: ID!, $item_id: ID!, $column_values: JSON!) {
          change_multiple_column_values (board_id: $board_id, 
                                         item_id: $item_id, 
                                         column_values: $column_values,
                                         create_labels_if_missing: true
                                         ) {
            id
          }
        }
        """
        variables = {
            "board_id": board_id,
            "item_id": item_id,
            "column_values": json.dumps(column_values)
        }
    else:
        mutation = """
        mutation ($board_id: ID!, $item_name: String!, $column_values: JSON!) {
          create_item (board_id: $board_id, 
                       item_name: $item_name, 
                       column_values: $column_values, 
                       create_labels_if_missing: true) {
            id
          }
        }
        """
        variables = {
            "board_id": board_id,
            "item_name": item_data.get("item_name") or "Unnamed Item",
            "column_values": json.dumps(column_values)
        }

    final_response = requests.post(url, 
                                   headers=headers, 
                                   json={"query": mutation, "variables": variables}, 
                                   timeout=30)
    final_response.raise_for_status()
    result = final_response.json()

    if "errors" in result:
        raise RuntimeError(f"Monday Mutation Error: {result['errors']}")

    return result
