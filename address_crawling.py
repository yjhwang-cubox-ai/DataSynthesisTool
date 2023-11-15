import requests
import xml.etree.ElementTree as ET

url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
API_key = 'Ui2rzzrvxw45wAqUhkVN8u1f+era7fZwSwHGwEcqi4Fs9PghJn4auUaEWXVeHuIUl9iJdpLpAZSLZgqHN2dTyw=='
key = requests.utils.unquote(API_key)

searchSe = 'road'
srchwrd = '마린시티1로 137'

params = {'ServiceKey' : key,
          'searchSe' : searchSe,
          'srchwrd' : srchwrd}

r = requests.get(url, params=params)
print(r.content)