import requests
import json
from config.settings import load_settings

def alter_dropdown_add_label(column_id: str, new_label: str):
    settings = load_settings()

    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": settings["MONDAY_API_TOKEN"],
        "Content-Type": "application/json",
        "API-Version": "2023-10"
    }

    board_id = settings["MONDAY_COMPANY_BOARD_ID"]

    fetch_query = """
    query ($board_id: ID!, $column_id: [String!]) {
      boards(ids: $board_id) {
        columns(ids: $column_id) {
          settings_str
        }
      }
    }
    """

    fetch_vars = {
        "board_id": board_id,
        "column_id": [column_id]
    }

    response = requests.post(
        url,
        headers=headers,
        json={"query": fetch_query, "variables": fetch_vars}
    )

    response.raise_for_status()
    data = response.json()

    settings_str = data["data"]["boards"][0]["columns"][0]["settings_str"]
    settings_json = json.loads(settings_str)

    labels = settings_json.get("labels", {})

    if new_label in labels.values():
        print("Label already exists.")
        return

    next_index = str(max([int(k) for k in labels.keys()], default=-1) + 1)
    labels[next_index] = new_label

    settings_json["labels"] = labels

    mutation = """
    mutation ($board_id: ID!, $column_id: String!, $settings: JSON!) {
      change_column_settings(
        board_id: $board_id,
        column_id: $column_id,
        settings: $settings
      ) {
        id
      }
    }
    """

    update_vars = {
        "board_id": board_id,
        "column_id": column_id,
        "settings": json.dumps(settings_json)
    }

    update_response = requests.post(
        url,
        headers=headers,
        json={"query": mutation, "variables": update_vars}
    )

    update_response.raise_for_status()
    print("Dropdown altered successfully.")
