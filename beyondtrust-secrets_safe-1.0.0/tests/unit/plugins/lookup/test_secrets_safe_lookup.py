# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import unittest

from ansible.plugins.loader import lookup_loader
from unittest.mock import MagicMock, patch
from ansible.errors import AnsibleError


class TestSecretsSafeLookUp(unittest.TestCase):
    """
    Test for SecretsSafeLookUp lookup plugin
    """
    
    password_safe_api_url = "https://www.fakeurl.com/fake_path/" #NOSONAR

    @patch('requests.Session.put')
    @patch('requests.Session.get')
    @patch('requests.Session.post')
    @patch('requests.post')
    def test_get_managed_account(self, mock_post, mock_req_post, mock_req_get, mock_req_put):
        """
        Test get managed account flow, successed case
        """
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            'access_token': 'my_token'
        })
        mock_post.return_value = mock_response
        
        sign_app_in_mock_response = MagicMock()
        sign_app_in_mock_response.status_code = 200
        sign_app_in_mock_response.json.return_value = {}
        
        create_request_mock_response = MagicMock()
        create_request_mock_response.status_code = 200
        create_request_mock_response.json.return_value = "123"

        mock_req_post.side_effect = [
            sign_app_in_mock_response,
            create_request_mock_response
        ]
        
        get_managed_accounts_response = MagicMock()
        get_managed_accounts_response.status_code = 200
        get_managed_accounts_response.json.return_value = { "SystemId": 1, "AccountId": 1 }
        
        get_credential_by_request_id_response = MagicMock()
        get_credential_by_request_id_response.status_code = 200
        get_credential_by_request_id_response.text = "Passcord_content_123456"

        mock_req_get.side_effect = [
            get_managed_accounts_response,
            get_credential_by_request_id_response
        ]
        
        request_check_in_response = MagicMock()
        request_check_in_response.status_code = 204

        mock_req_put.side_effect = [
            request_check_in_response
        ]
            
        lookup = lookup_loader.get('beyondtrust.secrets_safe.secrets_safe_lookup')
        attributes = {
            'api_url': self.password_safe_api_url,
            'retrieval_type': 'MANAGED_ACCOUNT',
            'client_id': 'fake_client_id',
            'client_secret': 'fake_client_secret',
            'secret_list': 'system_01/managed_account_1'
        }

        response = lookup.run([], **attributes)
        assert response == ["Passcord_content_123456"]


    @patch('requests.post')
    def test_get_managed_account_bad_token(self, mock_post):
        """
        Test get managed account flow, error getting token case
        """
        lookup = lookup_loader.get('beyondtrust.secrets_safe.secrets_safe_lookup')
        attributes = {
            'api_url': self.password_safe_api_url,
            'retrieval_type': 'MANAGED_ACCOUNT',
            'client_id': 'fake_client_id',
            'client_secret': 'fake_client_secret',
            'secret_list': 'system_01/managed_account_2'
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "error geting token"
        mock_post.return_value = mock_response
        with self.assertRaises(AnsibleError) as ex:
            lookup.run([], **attributes)
        
        exception_message = "Error getting token, message: error geting token, statuscode: 400"
        self.assertEqual(str(ex.exception), exception_message)


    @patch('requests.Session.put')
    @patch('requests.Session.get')
    @patch('requests.Session.post')
    @patch('requests.post')
    def test_get_managed_account_managed_account_not_found(self, mock_post, mock_req_post, mock_req_get, mock_req_put):
        """
        Test get managed account flow, managed account not found case
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            'access_token': 'my_token'
        })
        mock_post.return_value = mock_response
        
        sign_app_in_mock_response = MagicMock()
        sign_app_in_mock_response.status_code = 200
        sign_app_in_mock_response.json.return_value = {}
        
        create_request_mock_response = MagicMock()
        create_request_mock_response.status_code = 200
        create_request_mock_response.json.return_value = "123"

        mock_req_post.side_effect = [
            sign_app_in_mock_response,
            create_request_mock_response
        ]
        
        get_managed_accounts_response = MagicMock()
        get_managed_accounts_response.status_code = 400
        get_managed_accounts_response.text = "Managed account not found"
        
        mock_req_get.side_effect = [
            get_managed_accounts_response,
        ]

        lookup = lookup_loader.get('beyondtrust.secrets_safe.secrets_safe_lookup')
        attributes = {
            'api_url': self.password_safe_api_url,
            'retrieval_type': 'MANAGED_ACCOUNT',
            'client_id': 'fake_client_id',
            'client_secret': 'fake_client_secret',
            'secret_list': 'system_01/managed_account_3'
        }

        with self.assertRaises(AnsibleError) as ex:
            lookup.run([], **attributes)

        exception_message = "Error getting the manage account, message: Managed account not found, statuscode: 400, system name: system_01, managed account name: managed_account_3"
        self.assertEqual(str(ex.exception), exception_message)
        

    @patch('requests.Session.get')
    @patch('requests.Session.post')
    @patch('requests.post')
    def test_get_secret(self, mock_post, mock_req_post, mock_req_get):
        """
        Test get secret flow, successed case 
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            'access_token': 'my_token'
        })
        mock_post.return_value = mock_response
        
        sign_app_in_mock_response = MagicMock()
        sign_app_in_mock_response.status_code = 200
        sign_app_in_mock_response.json.return_value = {}
        
        get_secret_by_path_mock_response = MagicMock()
        get_secret_by_path_mock_response.status_code = 200
        get_secret_by_path_mock_response.json.return_value = [
            {
                "Password": "line 1\nline 2\nline 3", # NOSONAR
                "Id": "1ca2f649-5837-4bc4-235f-08db774dd40b",
                "Title": "text2",
                "SecretType": "Text"
            }
        ]
        
        mock_req_get.side_effect = [
            get_secret_by_path_mock_response
        ]
        
        mock_req_post.side_effect = [
            sign_app_in_mock_response
        ]
            
        lookup = lookup_loader.get('beyondtrust.secrets_safe.secrets_safe_lookup')
        attributes = {
            'api_url': self.password_safe_api_url,
            'retrieval_type': 'SECRET',
            'client_id': 'fake_client_id',
            'client_secret': 'fake_client_secret',
            'secret_list': 'path/secret_title'
        }

        response = lookup.run([], **attributes)
        assert response == ["line 1\nline 2\nline 3"]
        
        
    @patch('requests.Session.get')
    @patch('requests.Session.post')
    @patch('requests.post')
    def test_get_secret_file_case(self, mock_post, mock_req_post, mock_req_get):
        """
        Test get secret flow, getting file secret, successed case 
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            'access_token': 'my_token'
        })
        mock_post.return_value = mock_response
        
        sign_app_in_mock_response = MagicMock()
        sign_app_in_mock_response.status_code = 200
        sign_app_in_mock_response.json.return_value = {}
        
        get_secret_by_path_mock_response = MagicMock()
        get_secret_by_path_mock_response.status_code = 200
        get_secret_by_path_mock_response.json.return_value = [
            {
                "Id": "1ca2f649-5837-4bc4-235f-08db774dd40b",
                "Title": "text2",
                "SecretType": "File"
            }
        ]
        
        get_file_by_id_mock_response = MagicMock()
        get_file_by_id_mock_response.status_code = 200
        get_file_by_id_mock_response.text = "secret_content"
        
        mock_req_get.side_effect = [
            get_secret_by_path_mock_response,
            get_file_by_id_mock_response
        ]
        
        mock_req_post.side_effect = [
            sign_app_in_mock_response
        ]
            
        lookup = lookup_loader.get('beyondtrust.secrets_safe.secrets_safe_lookup')
        attributes = {
            'api_url': self.password_safe_api_url,
            'retrieval_type': 'SECRET',
            'client_id': 'fake_client_id',
            'client_secret': 'fake_client_secret',
            'secret_list': 'path/secret_title'
        }

        response = lookup.run([], **attributes)
        assert response == ["secret_content"]
        

    @patch('requests.Session.get')
    @patch('requests.Session.post')
    @patch('requests.post')
    def test_get_secret_invalid_folder_case(self, mock_post, mock_req_post, mock_req_get):
        """
        Test get secret flow, invalid folder case
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            'access_token': 'my_token'
        })
        mock_post.return_value = mock_response
        
        sign_app_in_mock_response = MagicMock()
        sign_app_in_mock_response.status_code = 200
        sign_app_in_mock_response.json.return_value = {}
        
        mock_req_post.side_effect = [
            sign_app_in_mock_response
        ]
            
        lookup = lookup_loader.get('beyondtrust.secrets_safe.secrets_safe_lookup')
        attributes = {
            'api_url': self.password_safe_api_url,
            'retrieval_type': 'SECRET',
            'client_id': 'fake_client_id',
            'client_secret': 'fake_client_secret',
            'secret_list': 'path'
        }

        with self.assertRaises(AnsibleError) as ex:
            lookup.run([], **attributes)

        exception_message = "Invalid secret path: path, check your path and title separator"
        self.assertEqual(str(ex.exception), exception_message)