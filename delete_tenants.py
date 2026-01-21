import requests
import json
import argparse

def get_and_filter_tenants(url, ignored_tenant_ids):
    phx_tenant_ids = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tenants = response.json()

        for tenant in tenants:
            tenant_id = tenant.get("tenantId")
            if "properties" in tenant and \
               "vanityName" in tenant["properties"] and \
               tenant_id not in ignored_tenant_ids:
                vanity_name = tenant["properties"]["vanityName"]
                if vanity_name is not None and vanity_name.startswith("phx-"):
                    phx_tenant_ids.append(tenant_id)

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return phx_tenant_ids

def delete_tenant(tenant_id, jwt_token):
    delete_url = f"https://tlm-api.gke-use4-001.qa.symphony.com/v1/sdus/s003/tenants/{tenant_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {jwt_token}",
        "content-type": "application/json"
    }
    try:
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()
        print(f"Successfully deleted tenant with ID: {tenant_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting tenant {tenant_id}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete tenants with vanityName starting with 'phx-'")
    parser.add_argument("jwt_token", help="JWT token for authorization")
    args = parser.parse_args()

    url = "https://tlm-api.gke-use4-001.qa.symphony.com/v1/sdus/s003/tenants/"

    ignored_tenant_ids = [
        "1288", "1340", "1383", "1306", "1341", "1378", "1237", "1056", 
        "1300", "1381", "1382", "1136"
    ]

    phx_tenant_ids = get_and_filter_tenants(url, ignored_tenant_ids)
    
    if phx_tenant_ids:
        print(f"Found {len(phx_tenant_ids)} tenants to delete.")
        for tenant_id in phx_tenant_ids:
            print(f"Deleting tenant with ID: {tenant_id} ...")
            delete_tenant(tenant_id, args.jwt_token)
    else:
        print("No tenants to delete.")
