Integracion Portabilidad Python Client
======================================

Cliente en Python para el WS RESTful de integración de portabilidad usando 
la librería python-requests.

**Uso:**

```python
from requests_portability import *

client = PortabilityAPI(
    base_url='http://apis.yachay.pe/portabilidad/v2/',
    api_key='5c901fde-88b1-4955-bcc6-cf0ffe87fa89'
)

obj = client.get_number('7022887') # response_type='object'

print obj.customer.customer_id # 19063

obj = client.get_number('7022887', response_type='dict')

print obj # Prints response as a Python dictionary

```

**Referencia:**

```
class PortabilityAPI(__builtin__.object)
 |  Methods defined here:
 |  
 |  __init__(self, base_url=None, api_key=None, headers=None, home=True)
 |  
 |  __repr__(self)
 |  
 |  delete(self, endpoint, params=None, response_type='dict')
 |  
 |  expand_uri_template(self, key, **params)
 |  
 |  get(self, endpoint, params=None, response_type='dict')
 |  
 |  get_customer(self, customer_id)
 |  
 |  get_customer_numbers(self, customer_id)
 |  
 |  get_customers(self)
 |  
 |  get_home_document(self, response_type='dict')
 |  
 |  get_number(self, number_id)
 |  
 |  get_numbers(self)
 |  
 |  get_resource(self, endpoint, response_type='object')
 |  
 |  get_uri_template(self, key)
 |  
 |  has_home_document(self)
 |  
 |  load_home_document(self)
 |  
 |  post(self, endpoint, params=None, files=None, response_type='dict')
 |  
 |  process_response(self, response, response_type='dict')
 |  
 |  put(self, endpoint, params=None, files=None, response_type='dict')
 |  
 |  request(self, endpoint, method='GET', params=None, response_type='dict')
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  RESPONSE_TYPES = ('dict', 'object', 'raw', 'response')
```

**Instrucciones de instalación:**

```
git -c http.sslVerify=false clone https://git.yachay.pe/devteam/requests-portability.git
cd requests-portability/
python setup.py install
cd ..
rm -Rf requests-portability/
```

(c) 2014 - Red Científica Peruana
