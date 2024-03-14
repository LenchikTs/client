# -*- coding: utf-8 -*-

import json
import os
import os.path
import requests
import requests.certs

#import urllib
import logging
try:                                # Python 2.x
    import urlparse
except Exception as e:              # Python 3
    import urllib.parse as urlparse

from auth import FHIRAuth


class FHIRException(Exception):
    """ Indicating a error response.
    """
    title = 'General Exception'

    def __init__(self, response):
        try:
            repAsDict = json.loads(response.content)
            message = 'FHIR %s (%s): %s' % ( self.title, response.status_code, repAsDict['issue'][0]['details'] )
        except:
            respText = response.content
            if isinstance(respText, str):
                try:
                    respText = respText.decode('utf8')
                except:
                    pass
            message = 'FHIR %s (%s): %s' % ( self.title, response.status_code, respText )
        Exception.__init__(self, message)
        self.response = response


class FHIRErrorException(FHIRException):
    """ Indicating a 400 response.
    """
    title = 'Error'


class FHIRUnauthorizedException(FHIRException):
    """ Indicating a 401 response.
    """
    title = 'Unauthorized'


class FHIRPermissionDeniedException(FHIRException):
    """ Indicating a 403 response.
    """
    title = 'PermissionDenied'


class FHIRNotFoundException(FHIRException):
    """ Indicating a 404 response.
    """
    title = 'Not found'


class FHIRMethodNotAllowedException(FHIRException):
    """ Indicating a 405 response.
    """
    title = 'RMethodNotAllowed'


class FHIRVersionConflictException(FHIRException):
    """ Indicating a 409 response.
    """
    title = 'Version conflict'


class FHIRVersionPreconditionFailedException(FHIRException):
    """ Indicating a 412 response.
    """
    title = 'Version Precondition Failed'


class FHIRUnprocessableEntityException(FHIRException):
    """ Indicating a 422 response.
    """
    title = 'Unprocessable Entity'


class FHIRServer(object):
    """ Handles talking to a FHIR server.
    """
    # было обнаружено, что в случае сборки exe-шки в windows
    # проверка сертификата не может быть выполнена правильным образом
    # так как сертификаты не включаются в exe-шку
    # встаёт ряд вопросов:
    # - где искать сертификаты?
    # - как называется файл с сертификатами?
    # - действительно-ли нам нужно проверять сертификаты?
    verify=True

    def __init__(self, client, base_uri=None, state=None):
        self.client = client
        self.auth = None
        self.base_uri = None

        # A URI can't possibly be less than 11 chars
        # make sure we end with "/", otherwise the last path component will be
        # lost when creating URLs with urllib
        if base_uri is not None and len(base_uri) > 10:
            self.base_uri = base_uri if '/' == base_uri[-1] else base_uri + '/'
        self._conformance = None
        if state is not None:
            self.from_state(state)
        if not self.base_uri or len(self.base_uri) <= 10:
            raise Exception("FHIRServer must be initialized with `base_uri` or `state` containing the base-URI, but neither happened")

        if FHIRServer.verify == True: # может быть ещё строка или False :)
            FHIRServer.init_verify()


    def should_save_state(self):
        if self.client is not None:
            self.client.save_state()


    @staticmethod
    def init_verify():
        for var in ('CA_BUNDLE', 'REQUESTS_CA_BUNDLE'):
            bundle = os.environ.get(var)
            if bundle and os.path.exists(bundle):
                FHIRServer.verify = bundle
                return
        path = requests.certs.where()
        if os.path.exists(path):
            FHIRServer.verify = path
            return
        # ещё можно поискать ca-bundle.crt в ~ или рядом с exe?
        FHIRServer.verify = False

    # MARK: Server Conformance Statement

    @property
    def conformance(self):
        self.get_conformance()
        return self._conformance

    def get_conformance(self, force=False):
        """ Returns the server's conformance statement, retrieving it if needed
        or forced.
        """
        if self._conformance is None or force:
            logging.info('Fetching conformance statement from {0}'.format(self.base_uri))
            conformance = getattr(self.client, 'conformance', None)
            if conformance is not None:
                conf = conformance.read_from('metadata', self)
            else:
                conf = None
            self._conformance = conf

            security = None
            try:
                security = conf.rest[0].security if conf else None
            except: # Exception as e:
                logging.info("No REST security statement found in server conformance statement")

            settings = {
                'aud': self.base_uri,
                'app_id': self.client.app_id if self.client is not None else None,
                'redirect_uri': self.client.redirect if self.client is not None else None,
            }
            self.auth = FHIRAuth.from_conformance_security(security, settings)
            self.should_save_state()


    # MARK: Authorization

    @property
    def desired_scope(self):
        return self.client.desired_scope if self.client is not None else None

    @property
    def launch_token(self):
        return self.client.launch_token if self.client is not None else None

    @property
    def headers(self):
        return self.client.headers if self.client is not None else None

    @property
    def authorize_uri(self):
        if self.auth is None:
            self.get_conformance()
        return self.auth.authorize_uri(self)

    def handle_callback(self, url):
        if self.auth is None:
            raise Exception("Not ready to handle callback, I do not have an auth instance")
        return self.auth.handle_callback(url, self)

    def reauthorize(self):
        if self.auth is None:
            raise Exception("Not ready to reauthorize, I do not have an auth instance")
        return self.auth.reauthorize(self) if self.auth is not None else None


    # MARK: Requests

    @property
    def ready(self):
        """ Check whether the server is ready to make calls, i.e. is has
        fetched its Conformance statement and its `auth` instance is ready.

        :returns: True if the server can make authenticated calls
        """
        return self.auth.ready if self.auth is not None else False

    def prepare(self):
        """ Check whether the server is ready to make calls, i.e. is has
        fetched its Conformance statement and its `auth` instance is ready.
        This method will fetch the Conformance statement if it hasn't already
        been fetched.

        :returns: True if the server can make authenticated calls
        """
        if self.auth is None:
            self.get_conformance()
        return self.auth.ready if self.auth is not None else False

    def request_json(self, path, nosign=False):
        """ Perform a request for JSON data against the server's base with the
        given relative path.

        :param str path: The path to append to `base_uri`
        :param bool nosign: If set to True, the request will not be signed
        :throws: Exception on HTTP status >= 400
        :returns: Decoded JSON response
        """
        headers = {'Accept': 'application/json+fhir'}
        res = self._get(path, headers, nosign)

        return res.json()

    def request_data(self, path, headers={}, nosign=False):
        """ Perform a data request data against the server's base with the
        given relative path.
        """
#        headers = headers.copy()
        headers = {}
        res = self._get(path, headers, nosign)
        return res.content


    def _get(self, path, headers={}, nosign=False):
        """ Issues a GET request.

        :returns: The response object
        """
        assert self.base_uri and path
        url = urlparse.urljoin(self.base_uri, path)

        headers = headers.copy()
        headers.update( {
                         'Accept': 'application/json+fhir',
                         'Accept-Charset': 'UTF-8',
                        }
                      )
        if self.headers:
            headers.update(self.headers)
        if not nosign and self.auth is not None and self.auth.can_sign_headers():
            headers = self.auth.signed_headers(headers)

        # perform the request but intercept 401 responses, raising our own Exception
        res = requests.get(url, headers=headers, verify=FHIRServer.verify)
        self.raise_for_status(res)
        return res

    def put_json(self, path, resource_json, headers={}):
        """ Performs a PUT request of the given JSON, which should represent a
        resource, to the given relative path.

        :param str path: The path to append to `base_uri`
        :param dict resource_json: The JSON representing the resource
        :throws: Exception on HTTP status >= 400
        :returns: The response object
        """
        url = urlparse.urljoin(self.base_uri, path)

        headers = headers.copy()
        headers.update( {
                          'Content-Type'  : 'application/json+fhir',
                          'Accept'        : 'application/json+fhir',
                          'Accept-Charset': 'UTF-8',
                        }
                      )
        if self.headers:
            headers.update(self.headers)
        res = requests.put(url, headers=headers, data=json.dumps(resource_json), verify=FHIRServer.verify)
        self.raise_for_status(res)
        return res

    def post_json(self, path, resource_json, headers={}, raiseIfstatusError=True, actionId = False ):
        """ Performs a POST of the given JSON, which should represent a
        resource, to the given relative path.

        :param str path: The path to append to `base_uri`
        :param dict resource_json: The JSON representing the resource
        :throws: Exception on HTTP status >= 400
        :returns: The response object
        """
        url = urlparse.urljoin(self.base_uri, path)
        headers = headers.copy()
        headers.update( {
                          'Content-Type'  : 'application/json+fhir',
                          'Accept'        : 'application/json+fhir',
                          'Accept-Charset': 'UTF-8',
                        }
                      )
        if self.headers:
            headers.update(self.headers)
        res = requests.post(url, headers=headers, data=json.dumps(resource_json), verify=FHIRServer.verify)
        if actionId:
            from PyQt4 import QtGui
            from library.Utils import toVariant, forceRef
            from PyQt4.QtCore import QDateTime
            db = QtGui.qApp.db
            externalSystemId = forceRef(QtGui.qApp.db.translate('rbExternalSystem', 'code', 'N3.ODLI', 'id'))
            tableAction_Export = db.table('Action_Export')
            actionExport = db.getRecordEx(tableAction_Export, '*',
                                          'master_id = %d and system_id = %d' % (actionId, externalSystemId))
            if not actionExport:
                actionExport = tableAction_Export.newRecord()
            actionExport.setValue('master_id', toVariant(actionId))
            # actionExport.setValue('masterDatetime', toVariant(QDateTime.currentDateTime()))
            actionExport.setValue('system_id', toVariant(externalSystemId))
            if res.status_code >= 400:
                if u'повтор' in res._content.decode('utf-8'):
                    actionExport.setValue('success', toVariant(1))
                else:
                    actionExport.setValue('success', toVariant(0))
                actionExport.setValue('note', u'%s %s' % (resource_json, res._content.decode('utf-8')))
            else:
                resAsJson = res.json()
                orderFullUrl = resAsJson['entry'][-1]['fullUrl']
                if orderFullUrl.startswith('Order/'):
                    identifier = orderFullUrl.partition('/')[2]
                    actionExport.setValue('externalId', toVariant(identifier))
                actionExport.setValue('success', toVariant(1))
                actionExport.setValue('note', toVariant(None))
            actionExport.setValue('dateTime', toVariant(QDateTime.currentDateTime()))

            db.insertOrUpdate(tableAction_Export, actionExport)
        if raiseIfstatusError:
            self.raise_for_status(res)
        return res

    def post_as_form(self, url, formdata, headers={}):
        """ Performs a POST request with form-data, expecting to receive JSON.
        This method is used in the OAuth2 token exchange and thus doesn't
        request json+fhir.

        :throws: Exception on HTTP status >= 400
        :returns: The response object
        """

        headers = headers.copy()
        headers.update( {
                          'Content-Type'  : 'application/x-www-form-urlencoded; charset=utf-8',
                          'Accept'        : 'application/json+fhir',
                          'Accept-Charset': 'UTF-8',
                        }
                      )
        if self.headers:
            headers.update(self.headers)

        res = requests.post(url, data=formdata, verify=FHIRServer.verify)
        self.raise_for_status(res)
        return res


    def delete_json(self, path, headers={}):
        """ Issues a DELETE command against the given relative path, accepting
        a JSON response.

        :param str url: The relative URL path to issue a DELETE against
        :returns: The response object
        """
        url = urlparse.urljoin(self.base_uri, path)
        headers = headers.copy()
        headers.update( {'Accept': 'application/json+fhir', })
        if self.headers:
            headers.update(self.headers)
        res = requests.delete(url, verify=FHIRServer.verify)
        self.raise_for_status(res)
        return res

    def raise_for_status(self, response):
        if response.status_code < 400:
            return
        if 400 == response.status_code:
            raise FHIRErrorException(response)
        if 401 == response.status_code:
            raise FHIRUnauthorizedException(response)
        elif 403 == response.status_code:
            raise FHIRPermissionDeniedException(response)
        elif 404 == response.status_code:
            raise FHIRNotFoundException(response)
        if response.status_code <500:
            raise FHIRErrorException(response)
        else:
            response.raise_for_status()


    # MARK: State Handling

    @property
    def state(self):
        """ Return current state.
        """
        return {
            'base_uri': self.base_uri,
            'auth_type': self.auth.auth_type if self.auth is not None else 'none',
            'auth': self.auth.state if self.auth is not None else None,
        }

    def from_state(self, state):
        """ Update ivars from given state information.
        """
        assert state
        self.base_uri = state.get('base_uri') or self.base_uri
        self.auth = FHIRAuth.create(state.get('auth_type'), state=state.get('auth'))

