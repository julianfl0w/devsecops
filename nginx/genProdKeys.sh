certbot certonly \
  --manual \
  --preferred-challenges dns \
  --email "julian@codecollective.us" \
  --agree-tos \
  --no-eff-email \
  --config-dir "$(pwd)/certbot-config" \
  --work-dir "$(pwd)/certbot-work" \
  --logs-dir "$(pwd)/certbot-logs" \
  -d "localhost" \
  -d "*.localhost"