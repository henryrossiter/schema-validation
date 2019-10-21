from pyld import jsonld
import json

KEYS_TO_EXPAND = [
    "responseOptions",
    "https://schema.repronim.org/valueconstraints"
]

def expand(obj, keepUndefined=False):
    """
    Function to take an unexpanded JSON-LD Object and return it expandedself.

    :param obj: unexpanded JSON-LD Object
    :type obj: dict
    :param keepUndefined: keep undefined-in-context terms?
    :param keepUndefined: bool
    :returns: list, expanded JSON-LD Array or Object
    """
    if obj==None:
        return(obj)
    try:
        newObj = jsonld.expand(obj)
    except jsonld.JsonLdError as e: # 👮 Catch illegal JSON-LD
        if e.cause.type == "jsonld.ContextUrlError":
            invalidContext = e.cause.details.get('url')
            print("Invalid context: {}".format(invalidContext))
            obj["@context"] = obj.get('@context', []).remove(invalidContext)
            return(expand(obj, keepUndefined))
        return(obj)
    newObj = newObj[0] if (
        isinstance(newObj, list) and len(newObj)==1
    ) else newObj
    if isinstance(
        newObj,
        dict
    ):
        if not isinstance(obj, dict):
            obj={}
        for k, v in newObj.copy().items():
            if not bool(v):
                newObj.pop(k)
        newObj.update({
            k: obj.get(k) for k in obj.keys() if (
                bool(obj.get(k)) and k not in keyExpansion(
                    list(newObj.keys())
                )
            )
        })
        for k in KEYS_TO_EXPAND:
            if k in newObj.keys():
                if isinstance(newObj.get(k), list):
                    v = [
                        expand(lv.get('@id')) for lv in newObj.get(k)
                    ]
                    v = v if v!=[None] else None
                else:
                    v = expand(newObj[k])
                if bool(v):
                    newObj[k] = v
        return(newObj if bool(newObj) else None)
    else:
        expanded = [expand(n, keepUndefined) for n in newObj]
        return(expanded if bool(expanded) else None)

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=10))

# compact a document according to a particular context
# see: http://json-ld.org/spec/latest/json-ld/#compacted-document-form
expanded = expand('https://raw.githubusercontent.com/ReproNim/schema-standardization/master/activities/BeckAnxietyInventory/BeckAnxietyInventory_schema')


print(json.dumps(expanded, indent=2))

# Output:
# {
#   "@context": {...},
#   "image": "http://manu.sporny.org/images/manu.png",
#   "homepage": "http://manu.sporny.org/",
#   "name": "Manu Sporny"
# }