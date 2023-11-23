# Short Bash script to pull out the MX server and the DMARC policy for a respective domain

!/bin/bash

# Check if domain name is provided as an argument
if [ -z "$1" ]; then
    echo "Please provide a domain name as an argument."
    exit 1
fi

domain="$1"

echo "\nFetching mail server for $domain..."
mail_server=$(dig +short MX $domain)
echo "Mail Server for $domain: $mail_server"

output=$(nslookup -type=txt _dmarc."$domain")

if [ -n "$(echo "$output" | egrep "\;[^s]*p[s]*\s*=\s*reject\s*")" ];then
	echo "$domain's DMARC policy is REJECT (not vulnerable)"
elif [ -n "$(echo "$output" | egrep "\;[^s]*p[s]*\s*=\s*quarantine\s*")" ];then
	echo "$domain's DMARC policy is QUARANTINE (may be vulnerable)"
elif [ -n "$(echo "$output" | egrep "\;[^s]*p[s]*\s*=\s*none\s*")" ];then
	echo "$domain's DMARC policy is NONE (is vulnerable)"
else
	echo "No DMARC record found for $domain)"
fi