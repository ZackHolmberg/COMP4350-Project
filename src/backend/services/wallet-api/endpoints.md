# Wallet API

## Get the user's wallet amount

> `POST` <http://localhost/wallet/amount>

**Required JSON:**

```json
200
{
  "umnetId": string,
  "password": string
}
```

Returns the amount of bisoncoin that the user currently owns.

**Example return:**

```json
400
{
  "amount": int
}
```

or

```json
{
  "error": string
}
```
