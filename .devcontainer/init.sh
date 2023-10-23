#!/bin/bash

cd . || true # change dir to root of the repo, so you can reach everything.


#// region [ rgba(100, 15, 100, 0.05)]
#?||--------------------------------------------------------------------------------||
#?||                               Init .env                                    ||
#?||--------------------------------------------------------------------------------||
# Copy initial configuration files, use the template as default.
cp config/global/one.template.env config/global/.env || true
# Update the template with the custom conf if available, otherwise proceed with default.
cp config/global/.env config/global/.env || true
# Copy the .env into xgpt to use it for its container.
cp config/global/.env apps/xgpt/.env || true
# Copy now the user config.yaml.
cp config/user/config.yaml apps/xgpt/config.yaml || true
# Copy the Streamlit Theme and default sqldb user
cp config/streamlit/*.toml apps/xgpt/.streamlit/ || true
# Now source the final .env and proceed.
source config/global/.env || handle_error "Activating AI Environment Failed"
#// endregion

