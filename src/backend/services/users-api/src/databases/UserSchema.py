userSchema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["first_name", "last_name", "umnetId", "password", "public_key"],
        "properties": {
            "first_name": {
                "bsonType": "string",
                "description": "user's first name must be a string and is required.",
            },
            "last_name": {
                "bsonType": "string",
                "description": "user's last name must be a string and is required.",
            },
            "umnetId": {
                "bsonType": "string",
                "description": "user's umnetId must be a string and is required. This is the umnetId in our implementation.",
            },
            "password": {
                "bsonType": "string",
                "description": "user's password must be a string and is required.",
            },
            "public_key": {
                "bsonType": "string",
                "description": "user requires a string public key to enable lookups.",
            },
        },
    }
}
