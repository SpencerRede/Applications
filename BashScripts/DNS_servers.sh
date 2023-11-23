# This small bash script is used to retrieve all DNS servers for a resepective domain,
# Sort them into A, AA, AAA, AAAA, TXT, MX, and SOA servers and save the query to a .txt file

!/bin/bash

# Check if domain name is provided as an argument
if [ -z "$1" ]; then
    echo "Please provide a domain name as an argument."
    exit 1
fi

domain="$1"
output_file="dns_servers_$domain.txt"

# Fetch DNS servers for the domain
echo "Fetching DNS servers for $domain..."
dig ANY $domain | awk '{
    if ($4 == "NS") {
        ns_servers = ns_servers $NF "\n"
    } else if ($4 == "A") {
        a_servers = a_servers $NF "\n"
    } else if ($4 == "AA") {
        aa_servers = aa_servers $NF "\n"
    } else if ($4 == "AAAA") {
        aaaa_servers = aaaa_servers $NF "\n"
    } else if ($4 == "TXT") {
        txt_servers = txt_servers $NF "\n"
    } else if ($4 == "MX") {
        mx_servers = mx_servers $NF "\n"
    } else if ($4 == "SOA") {
        SOA_servers = SOA_servers $NF "\n"
    }
} END {
    print "NS Servers:\n" ns_servers > "'$output_file'"
    print "\nA Servers:\n" a_servers >> "'$output_file'"
    print "\nAA Servers:\n" aa_servers >> "'$output_file'"
    print "\nAAAA Servers:\n" aaaa_servers >> "'$output_file'"
    print "\nTXT Servers:\n" txt_servers >> "'$output_file'"
    print "\nMX Servers:\n" mx_servers >> "'$output_file'"
    print "\nSOA Servers:\n" soa_servers >> "'$output_file'"
}'

echo "DNS servers for $domain have been saved and sorted by server type to $output_file."
