#! /bin/bash

curl --request GET \
--url "https://api.github.com/devwithkrishna" \
--header "Authorization: Bearer $GITHUB_TOKEN" \
--header "X-GitHub-Api-Version: 2022-11-28"