# CB plus

Stock reading management system that indecate nearest expiration date of products. Along with sync mechanism to keep all connector update to date with latest changes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements
```

## API 

```
/api/doc/
{
    "stock_expiration": "host/api/public/stock_expiration/",
    "stock_readings": "host/api/public/stock_readings/",
    "products": "host/api/public/products/"
}
```

## SOCKET
#### Endpoint

```
ws/stock/{user_id}
```
#### Usage
* By connecting to socket you will recieve all updates in realtime.
* If user is offline, all updates are saved to be synced later.
There are 4 socket type 
1. Stock => automatic communication to recieve up to date changes. 
2. Sync_from => if user miss or want to check if something missing
3. Sync_to => if user have made some changes locally
4. Synced => to confirm sync

#### Dummy request
```
{
"type":"sync.to", "stock_dict": {"id": 1, "server_id":2, "product_id": "567890", "expired_at": "2020-09-19"},
"action_at": "2020-09-18",
"action": "UPDATE"
}

{
"type":"sync.to", "stock_dict": {"product_id": "567890", "expired_at": "2020-09-19"},
"action_at": "2020-09-18",
"action": "CREATE"
}

{
"type":"sync.to", "stock_dict": {"id": 1, "server_id":2, "product_id": "567890", "expired_at": "2020-09-19"},
"action_at": "2020-09-18",
"action": "DELETE"
}
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
