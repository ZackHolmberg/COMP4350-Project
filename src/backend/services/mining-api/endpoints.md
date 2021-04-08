# Mining

```json
Transaction Object = {
    "from" : string,
    "to" : string,
    "amount" : string,
    "id" : string,
    "signature" : string
}

```

## Queue a new transaction for mining

> GET <http://localhost/mining/queue>

Required JSON:

```json
Transaction Object
```

Example return:

```json
200

{
  "success": True
}
```

```json
400

{
  "error": string
}
```

# Socket events

> client sends "proof"

Required JSON:

```json
{
  "id": string, // transaction id for which the proof was found
  "proof": string,
  "nonce": string,
  "minerId": string
}
```

> broadcast to all clients broadcasts "findProof"

Sends JSON:

```json
Transaction Object
```

> broadcast to all clients "stopProof"

```json
N / A
```

> emits to client "reward"

```json
N / A
```
