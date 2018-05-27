set/p path="set path to DB beckup:  "
cd C:\Program Files\MongoDB\Server\3.6\bin
mongodump -d test -o %path%