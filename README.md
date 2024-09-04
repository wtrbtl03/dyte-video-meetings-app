# Dyte Video Meetings App
Utilizes [Dyte.io](https://dyte.io) [V2 API](https://docs.dyte.io/api#/) to create a shareable video meeting.

## Environment variables
- Make a ```.env``` file.
- Add the following environment variables.
```
SECRET_KEY=<"django secret key">
DEBUG=True
ALLOWED_HOSTS="localhost,127.0.0.1" // for running locally
DYTE_API_KEY=<"your Dyte API key">
DYTE_ORG_ID=<"your Dyte organisation ID">
DYTE_CONN_BASE64="Base64 <ORG_ID>:<API_KEY>" // can use https://www.base64encode.org/ 
NPM_BIN_PATH=<"path to npm"> // path to npm eg.- C:/Program Files/nodejs/npm.cmd
```
