userSchema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["first_name", "last_name", "umnetID", "password", "public_key"],
            "properties": {
                "first_name": {
                    "bsonType": "string",
                    "description": "user's first name must be a string and is required."
                },
                "last_name": {
                    "bsonType": "string",
                    "description": "user's last name must be a string and is required."
                },
                "umnetID": {
                    "bsonType": "string",
                    "description": "user's umnetID must be a string and is required. This is the umnetID in our implementation."
                },
                "password": {
                    "bsonType": "string",
                    "description": "user's password must be a string and is required."
                },
                "public_key": {
                    "bsonType": "string",
                    "description": "user requires a string public key to enable lookups."
                }
            }
        }
    }