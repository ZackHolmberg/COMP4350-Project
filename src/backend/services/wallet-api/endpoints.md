# Wallet API

## Get the user's wallet amount

> `POST` <http://localhost/wallet/amount>

**Required JSON:**

```json 
{
  "umnetId": string
}
```
Returns the amount of bisoncoin that the user currently owns.

**Example return:**

```json
{
  "amount": int
}
```

or

```json
{
  "error" : string
}
```

## Get the user's transaction history

> `GET` <http://localhost/wallet/history/umnetId>

Returns the transaction history of the umnetId passed in the query.


**Example return:**

```json
{
  "history": List of dicts arranged by timestamps by recency as follows 
  [
    {
      "transaction": {
        "amount": float,
        "from_address": string,
        "to_address": string,
        "id": string,
        "signature": string,
        "timestamp": float
      }, 
      "type": send or receive or reward
    }
  ]
}
200
```
