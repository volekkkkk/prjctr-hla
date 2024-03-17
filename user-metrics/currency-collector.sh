#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

ga_url="https://www.google-analytics.com/mp/collect?measurement_id=${GA_MEASUREMENT_ID}&api_secret=${GA_TOKEN}"
currency_api="https://api.monobank.ua/bank/currency"

iso_4217_uah=980
iso_4217_usd=840

rateSell=$(curl -s $currency_api | jq -c ".[] | select(.currencyCodeA | contains($iso_4217_usd)) | .rateSell")
echo "Rate Sell - $rateSell"

curl --header "Content-Type: application/json" \
  --request POST \
  --data "{\"client_id\": \"usd_currency_collector\", \"events\": [{\"name\": \"usd_rate_sell\", \"params\": {\"rateSell\": "$rateSell"}}]}" \
  $ga_url
