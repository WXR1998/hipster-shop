node server.js 2>&1 &
/usr/local/chaosblade/blade c cpu fullload --cpu-percent 14

while [[ true ]]; do
    sleep 1
done