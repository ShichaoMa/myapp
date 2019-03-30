sslocal -c ../shadowsocks.json > shadow.log 2>&1 &
polipo socksParentProxy=127.0.0.1:1080 > polipo.log 2>&1 &
custom-redis-server > redis.log 2>&1 & 
