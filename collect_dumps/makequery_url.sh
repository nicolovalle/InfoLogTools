#!/bin/bash

echo 'http://alihlt-gw-prod.cern.ch:8081/?q={%22facility%22:{%22match%22:%22ODC%22},%22partition%22:{%22match%22:%22__PARTITION__%22},%22message%22:{%22match%22:%22Agent%20ID%25%22},%22severity%22:{%22in%22:%22I%20W%20E%20F%22}}' | sed "s/__PARTITION__/$1/g" > epnlogurl.html


echo ""
cat epnlogurl.html
echo ""

if command -v xclip &> /dev/null
then
    xclip -sel clip < epnlogurl.html
    echo "COPIED TO CLIPBOARD"
fi


