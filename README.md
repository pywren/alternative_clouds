
[Neither azure nor google cloud are mature enough for production use w pyren](http://pywren.io/pywren_backends.html)

## Azure
python isn't supported in 2.0, and any function that you try to execute will just fail.

## Google Cloud Functions
Limitations on socket traffic make it hard to scale out. Also, limited geographic availability (central US) and node.js environment make it not a great fit for pywren yet.

