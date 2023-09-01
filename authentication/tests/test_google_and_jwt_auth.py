from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch,MagicMock
from authentication.views import UserGoogleLoginCallback

User = get_user_model()

class GoogleJWTAuthenticationTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "email": "test@gmail.com",
            "given_name": "test",
            "family_name": "test",
        }
        cls.user = User.objects.create_user(username="test2",email="test2@gmail.com",password="testing1234")
    
    
    @patch.object(UserGoogleLoginCallback,"verify_state",return_value=True)
    @patch("requests.get")
    @patch("requests.post")
    def test_with_new_user(self,mock_post:MagicMock,mock_get:MagicMock,mock_state:MagicMock):
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id_token": "id_token"}
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = self.user_data
        
        mock_get.return_value = mock_get_response
        mock_post.return_value = mock_post_response
        
        data = {
            "code": "code",
            "state": "state",
        }
        self.client.get("/auth/google/")
        response = self.client.get("/auth/google/callback/",data=data)
        self.assertEqual(response.status_code,200)
        self.assertIn("access_token",response.data)
        
    @patch.object(UserGoogleLoginCallback,"verify_state",return_value=True)
    @patch("requests.get")
    @patch("requests.post")
    def test_with_registered_user(self,mock_post:MagicMock,mock_get:MagicMock,mock_state:MagicMock):
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id_token": "id_token"}
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = {"email": "test2@gmail.com"}
        
        mock_get.return_value = mock_get_response
        mock_post.return_value = mock_post_response
        
        data = {
            "code": "code",
            "state": "state",
        }
        self.client.get("/auth/google/")
        response = self.client.get("/auth/google/callback/",data=data)
        self.assertEqual(response.status_code,200)
        self.assertIn("access_token",response.data)