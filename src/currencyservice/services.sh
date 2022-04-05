node server.js 2>&1 &
/usr/local/chaosblade/blade c mem load --mode ram --rate 200 --reserve 200

while [[ true ]]; do
    sleep 1
    /usr/local/chaosblade/blade status --type create
done