/frontend/server 2>&1 &
/usr/local/chaosblade/blade c network loss --percent 97 --interface eth0 2>&1 &
/usr/local/chaosblade/blade c network corrupt --percent 97 --interface eth0 2>&1 &
/usr/local/chaosblade/blade c network delay --time 500 --interface eth0 2>&1 &
# ifconfig
# eval $(ifconfig | grep flag | sed -e "s/:.*/ ;/g" | sed -e "s/^/\/usr\/local\/chaosblade\/blade c network loss --percent 50 --remote-port 3550,7000,7070,8080,50051,5050,9555 -n --interface /g")

while [[ true ]]; do
    sleep 1
done