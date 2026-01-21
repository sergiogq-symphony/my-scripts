# my-scripts

## `delete_tenants.py` Script

This script fetches a list of tenants from a specified API endpoint, filters them by `vanityName` (only includes those starting with "phx-"), and then attempts to delete the filtered tenants, excluding a predefined list of ignored tenant IDs.

### Setup

1.  **Install Python dependencies**:
    ```bash
    pip install requests
    ```

### Usage

To run the script, you need to provide a JWT token for authentication.

```bash
python3 delete_tenants.py <YOUR_PMP_JWT_TOKEN>
```
