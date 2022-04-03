/checkoutservice 2>&1 &
/usr/local/chaosblade/blade c cpu fullload

while [[ true ]]; do
    sleep 1
done