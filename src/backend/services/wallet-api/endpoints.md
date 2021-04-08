# Wallet API

## Get the user's wallet amount

> `POST` <http://localhost/wallet/amount>

**Required JSON:**

```json
{
  "umnetId": string,
  "password": string
}
```

Returns the amount of bisoncoin that the user currently owns.

**Example return:**

```json
{
  "amount": int
}
200
```

or

```json
{
  "error" : string
}
400
```

## Get the user's transaction history

> `GET` <<http://localhost/wallet/history/><umnetId>>

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
        "timestamp": int
      },
      "type": send or receive or reward
    }
  ]
}
200
```
