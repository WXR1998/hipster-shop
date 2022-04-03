/frontend/server 2>&1 &

while [[ true ]]; do
    sshpass -p logpecker scp -o StrictHostKeyChecking=no wxr@testbed-master-1:~/packages/fileload ./$RANDOM
done