import json

class DID:
    def __init__(self,dict):
        if "@context" in dict.keys():
            self.context=dict["@context"]
        elif "@context" not in dict.keys():
            self.context=[]
        if "id" in dict.keys():
            self.id=dict["id"]
        elif "id" not in dict.keys():
            self.id=""
        if "verificationMethod" in dict.keys():
            self.verificationMethod=dict["verificationMethod"]
        elif "verificationMethod" not in dict.keys():
            self.verificationMethod=[]

    #returns a json string of the did document
    def to_json(self):
        to_return={
            "@context":self.context,
            "id":self.id,
            "verificationMethod":self.verificationMethod
        }
        return to_return

    def __str__(self):
        return json.dumps(self.to_json())

    
dict={
    "@context": [
      "https://www.w3.org/ns/did/v1",
      "https://w3id.org/security/suites/jws-2020/v1"
    ],
    "id": "did:web:example.com",
    "verificationMethod": [
      {
        "id": "did:web:example.com#key-0",
        "type": "JsonWebKey2020",
        "controller": "did:web:example.com",
        "publicKeyJwk": {
          "kty": "OKP",
          "crv": "Ed25519",
          "x": "0-e2i2_Ua1S5HbTYnVB0lj2Z2ytXu2-tYmDFf8f5NjU"
        }
      },
      {
        "id": "did:web:example.com#key-1",
        "type": "JsonWebKey2020",
        "controller": "did:web:example.com",
        "publicKeyJwk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "9GXjPGGvmRq9F6Ng5dQQ_s31mfhxrcNZxRGONrmH30k"
        }
      },
      {
        "id": "did:web:example.com#key-2",
        "type": "JsonWebKey2020",
        "controller": "did:web:example.com",
        "publicKeyJwk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "38M1FDts7Oea7urmseiugGW7tWc3mLpJh6rKe7xINZ8",
          "y": "nDQW6XZ7b_u2Sy9slofYLlG03sOEoug3I0aAPQ0exs4"
        }
      }
    ]
  }

did=DID(dict)
did.verificationMethod.append({"newkey"})
print(did.to_json())