#!/bin/bash

curl -s 'https://api.sandbox.ebay.com/ws/api.dll'\
 -H 'X-EBAY-API-CALL-NAME: GetCategories'\
 -H 'X-EBAY-API-APP-NAME: EchoBay62-5538-466c-b43b-662768d6841'\
 -H 'X-EBAY-API-CERT-NAME: 00dd08ab-2082-4e3c-9518-5f4298f296db'\
 -H 'X-EBAY-API-DEV-NAME: 16a26b1b-26cf-442d-906d-597b60c41c19'\
 -H 'X-EBAY-API-SITEID: 0'\
 -H 'X-EBAY-API-COMPATIBILITY-LEVEL: 861'\
 --data '<?xml version="1.0" encoding="utf-8"?>
<GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <CategoryParent>10542</CategoryParent>
  <CategorySiteID>0</CategorySiteID>
  <ViewAllNodes>True</ViewAllNodes>
  <DetailLevel>ReturnAll</DetailLevel>
  <RequesterCredentials>
    <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**t2XTUQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**pZOn+3Cb/dnuil4E90EEeGpHlaBVP0VpLebK58TPQ210Sn33HEvjGYoC9UYVqfbhxte6wp8/fPL795uVh9/4X00HC3wAfzcV+wobN2NfReqWAXFdfuj4CbTHEzIHVLJ8tApLPlI8Nxq6oCa5KsZf5L+An85i2BnohCfscJtl9OcZYnyWnD0oA4R3zdnH3dQeKRTxws/SbVCTgWcMXBqL9TUr4CrnOFyt0BdYp4lxg0HbMv1akuz+U7wQ3aLxJeFoUow20kUtVoTIDhnpfZ40Jcl/1a2ui0ha3rl9D3oA66PUhHSnHJTznwtp1pFLANWn9I49l9rrYbzzobB6SGf18LK/5cqSwse3AWMXJkFVbgFM7e5DZBv59S1sCRdEjzw8GciKYSxGDqu8UJQHgL/QPiTFhtj2Ad/vjZ/6PLBVA9rhOxJnlhCvLXmWZIf1NNcckN8uEEIqK7Wn0DdDi8p44ozIWNaIQ319HjYYOBp4a5FLUjwXCamoqfSjYli5ikqe0jwn+LxnOWblY47TFhruRQpYaBAro4VbgirwNYT7RlEGz+u7ol9A873dnqEZgdXWfrWkyxyKGeXHnHjiynfL/JDCdl2U2s+s5iOd8hp6QklHevPOlOtZgW+K/eFIv53UATQi4vMptUKEeD6QxFzvxP7wRAkKIQZUq+LKB8lZBP/Epjni47HXKpwQdgbTWbyfHpSF3A52u8koUY9chiBk1FCpqjBM/BT5tjhIlrQUVeWUUyGeQ49sJJvaeVnaavo9</eBayAuthToken>
  </RequesterCredentials>
</GetCategoriesRequest>' | xmllint --format -