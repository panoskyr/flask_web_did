#a python class to use with json documents

import json


class clsVerificationMethod:

    def __init__(self,id,controller,type,publicKeyJwk):
        self.controller=controller
        self.id=id
        self.type=type
        self.publicKeyJwk=publicKeyJwk

    def __iter__(self):
        yield from {
            "id":self.id,
            "controller":self.controller,
            "type":self.type,
            "publicKeyJwk":self.publicKeyJwk
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        to_return={
            "id":self.id,
            "controller":self.controller,
            "type":self.type,
            "publicKeyJwk":self.publicKeyJwk.to_json()
        }
        return to_return


    @staticmethod
    #returns a verificationMethod object given a python dictionary
    def from_json(jsonDict):
        if "kty" in jsonDict.keys():
            return clsPublicKeyJwk.from_json(jsonDict)
        elif "id" in jsonDict.keys():
            #create a clsPublicKeyJwk object
            #pass it as argument to the clsVerificationMethod constructor
            publicKeyDict=jsonDict["publicKeyJwk"]
            publicKeyObj=clsPublicKeyJwk.from_json(publicKeyDict)
            verificationMethodObj=clsVerificationMethod(
                jsonDict["id"],
                jsonDict["controller"],
                jsonDict["type"],
                publicKeyObj
            )
            return verificationMethodObj

    
class clsPublicKeyJwk:
    def __init__(self,kty,crv,x):
        self.kty=kty
        self.crv=crv
        self.x=x

    def __iter__(self):
        yield from {
            "kty":self.kty,
            "crv":self.crv,
            "x":self.x
        }.items()

    def __str__(self):
        return json.dumps(dict(self),ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    #a function that takes a dictionary and returns 
    #an object
    def from_json(jsonDict):
        return clsPublicKeyJwk(
            jsonDict["kty"],
            jsonDict["crv"],
            jsonDict["x"]
        )

class clsVerificationMethodCollection:
    def __init__(self, verificationMethods):
        #a list of verification methods passed as parameter
        self.verificationMethods=verificationMethods

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        li=[]
        for vm in self.verificationMethods:
            li.append(vm.to_json())
        to_return={"verificationMethod":li}
        return to_return
        

    
    #given a dict entry of verificationMethod list
    @staticmethod
    def from_json(jsonDict):
        if "verificationMethod" in jsonDict.keys():
            verificationMethodObjList=[]
            for item in jsonDict["verificationMethod"]:
                verificationMethodObj=clsVerificationMethod.from_json(item)
                verificationMethodObjList.append(verificationMethodObj)
            return (clsVerificationMethodCollection(verificationMethodObjList))
    
    def addVerMethod(self,verificationMethod):
        self.verificationMethods.append(verificationMethod)
        print("verification Method added succesfully")

    #given a string of the verification method id
    #it removes the verification Method
    def removeVerMethod(self,id):
        for verMethod in self.verificationMethods:
            if id==verMethod.id:
                self.verificationMethods.remove(verMethod)
                print("Succesfully removed verificationMethod ")
                return

        print("no such verification method exists!")
        

jsondict={"verificationMethod": [
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

jsond2={
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


o=clsVerificationMethodCollection.from_json(jsondict)
verObj=clsVerificationMethod.from_json(jsond2)
o.addVerMethod(verObj)
o.removeVerMethod("did:web:example.com#key-0")
print(o.to_json())