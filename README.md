# LateBloomers
For NASA Spaceapps Challenge

## Running server with authentication
1. Download the private key JSON file.
2. Copy the contents of the .env-template file into a .env file at the top level of the directory (./)
3. Set the environment variables as defined below.

### Environment Variables
| Environment Variable Name | Definition | Example |
| :------- | :------- | :------- |
| PRIVATE_KEY_PATH  | Path to the local private key JSON file                      | /Users/me/sa-private-key.json |
| SERVICE_ACCOUNT   | The service account registered with out Earth Engine project | service_account_name@project_id.iam.gserviceaccount.com |
