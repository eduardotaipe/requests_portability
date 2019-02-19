# -*- coding: utf-8 -*-

import uritemplate
import requests
import json

from collections import namedtuple

from requests_portability import __version__

try:
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from urllib import urlencode

try:
    string_types = basestring
except NameError:
    string_types = str


def _split_params_and_files(params_):
        params = {}
        files = {}
        for k, v in params_.items():
            if hasattr(v, 'read') and callable(v.read):
                files[k] = v
            elif isinstance(v, string_types):
                params[k] = v
            else:
                continue
        return params, files


# Errors

class PortabilityClientError(Exception):

    def __init__(self, message, error_code=None, error_list=None):

        self.error_code = error_code
        self.message = message
        self.error_list = error_list

        if error_code is not None:
            self.message = '%s: %s' % (error_code, message)

        super(PortabilityClientError, self).__init__(self.message)


class PortabilityAPIError(PortabilityClientError):
    pass


class PortabilityAuthError(PortabilityClientError):
    pass


# API

class PortabilityAPI(object):

    RESPONSE_TYPES = ('dict', 'object', 'raw', 'response', )

    def __init__(self, base_url=None, api_key=None, headers=None, home=True):

        self.base_url = base_url
        self.api_key = api_key

        # If there's headers, set them. If not, lets
        self.headers = headers or {
            'User-agent': 'Requests-Portability %s' % __version__
        }

        if home:
            self.load_home_document()


    def get(self, endpoint, params=None, response_type='dict'):
        return self.request(
            endpoint,
            method='GET',
            params=params,
            response_type=response_type
        )


    def put(self, endpoint, params=None, files=None, response_type='dict'):
        return self.request(
            endpoint,
            method='PUT',
            params=params,
            response_type=response_type
        )


    def post(self, endpoint, params=None, files=None, response_type='dict'):
        return self.request(
            endpoint,
            method='POST',
            params=params,
            response_type=response_type
        )


    def delete(self, endpoint, params=None, response_type='dict'):
        return self.request(
            endpoint,
            method='DELETE',
            params=params,
            response_type=response_type
        )


    def process_response(self, response, response_type='dict'):
        if response_type == 'dict':
            return response.json()
        elif response_type == 'object':
            return json.loads(
                response.text,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values())
            )
        if response_type == 'raw':
            return response.text
        elif response_type == 'response':
            return response
        else:
            raise PortabilityClientError(
                'Unsupported response type \'%(response_type)s\'' % {
                    'response_type': response_type
                }
            )


    def request(
        self, endpoint, method='GET', params=None, response_type='dict'
    ):

        params = params or {}

        # Check for a supported response type
        if response_type not in self.RESPONSE_TYPES:
            raise PortabilityClientError(
                'Unsupported response type \'%(response_type)s\'' % {
                    'response_type': response_type
                }
            )

        # Works with relative and absolute endpoints
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            url = endpoint
        else:
            url = self.base_url + endpoint

        method = method.lower()

        if not method in ('get', 'put', 'post', 'delete'):
            raise PortabilityClientError(
                'Method must be of GET, PUT, POST or DELETE'
            )

        params, files = _split_params_and_files(params)

        headers = self.headers

        if 'X-ApiKey' not in headers:
            headers['X-ApiKey'] = self.api_key

        func = getattr(requests, method)
        try:
            if method == 'get':
                response = func(url, params=params, headers=self.headers)
            else:
                response = func(
                    url,
                    data=params,
                    files=files,
                    headers=headers
                )

        except requests.exceptions.RequestException:
            raise PortabilityClientError('An unknown error occurred.')

        try:
            content = response.json()
        except ValueError:
            raise PortabilityClientError(
                'Unable to parse response, invalid JSON.'
            )

        if response.status_code in [401, 403]:
            exception_class = PortabilityAuthError
            has_errors = True
        elif response.status_code not in [200, 204]:
            has_errors = True
            exception_class = PortabilityAPIError
        else:
            has_errors = False

        if has_errors:
            try:
                errors = content['errors']
                if len(errors)>0:

                    error = errors[0]
                    error_code = error.get('code', '')
                    error_message = error.get('message', '')

                    error_list = errors

                    raise exception_class(
                        error_message,
                        error_code=error_code,
                        error_list=error_list
                    )
            except KeyError:
                raise PortabilityClientError(
                    'Unknown JSON structure in response.'
                )

        # Return response according to requested response type
        return self.process_response(response, response_type)


    def __repr__(self):
        return u'<PortabilityAPI: %s>' % self.api_key


    def get_home_document(self, response_type='dict'):
        return self.get('/', response_type=response_type)


    def load_home_document(self):
        self.home_document = self.get_home_document()


    def has_home_document(self):
        return hasattr(self, 'home_document')


    def get_uri_template(self, key):
        return self.home_document.get(key, None)


    def expand_uri_template(self, key, **params):
        template = self.get_uri_template(key)
        if template is None:
            return None
        return uritemplate.expand(template, params)


    def get_resource(self, endpoint, response_type='object'):
        return self.get(endpoint, response_type=response_type)


    def get_numbers(self):
        endpoint = self.expand_uri_template('number_collection_url')
        return self.get_resource(endpoint)


    def get_number(self, number_id):
        endpoint = self.expand_uri_template(
            'number_url',
            number_id=number_id
        )
        return self.get_resource(endpoint)
        

    def get_customers(self):
        endpoint = self.expand_uri_template('customer_collection_url')
        return self.get_resource(endpoint)


    def get_customer(self, customer_id):
        endpoint = self.expand_uri_template(
            'customer_url',
            customer_id=customer_id
        )
        return self.get_resource(endpoint)


    def get_customer_numbers(self, customer_id):
        endpoint = self.expand_uri_template(
            'customer_number_collection_url',
            customer_id=customer_id
        )
        return self.get_resource(endpoint)
