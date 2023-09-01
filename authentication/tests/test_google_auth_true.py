from rest_framework.test import APITestCase,APIRequestFactory
from django.contrib.auth import get_user_model
from unittest.mock import patch,MagicMock
from django.contrib.sessions.backends.base import SessionBase
from authentication.serializers import UserCreationSerializer
from authentication.views import UserGoogleLoginCallback

User = get_user_model()

class GoogleAuthenticationTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory = APIRequestFactory()
        cls.view = UserGoogleLoginCallback()
        cls.user_data = {
            "email": "test@gmail.com",
            "given_name": "test",
            "family_name": "test",
        }
        cls.user = User.objects.create_user(username="test2",email="test2@gmail.com",password="testing1234")
    
    def test_urls(self):
        response = self.client.get("/auth/google/")
        self.assertNotEqual(response.status_code,404)
        
    def test_google_login_view(self):
        response = self.client.get("/auth/google/")
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith("https://accounts.google.com"))
    
    def test_verify(self):
        request = self.factory.get("/auth/google/callback/")
        request.session = {"state": "state"}
        self.view.request = request
        state = self.view.verify_state("state")
        self.assertTrue(state)
    
    @patch.object(UserGoogleLoginCallback,"verify_state",return_value=True)
    @patch("requests.get")
    @patch("requests.post")
    def test_google_callback_view_with_new_user(self,mock_post:MagicMock,mock_get:MagicMock,mock_state:MagicMock):
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
        self.assertIn("email",response.data)
        self.assertNotIn("is_superuser",response.data)
    
    @patch.object(UserGoogleLoginCallback,"verify_state",return_value=True)
    @patch("requests.get")
    @patch("requests.post")
    def test_google_callback_view_with_new_user_serializer_invalid(self,mock_post:MagicMock,mock_get:MagicMock,mock_state:MagicMock):
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
        with patch.object(UserCreationSerializer,"is_valid",return_value=False):
            response = self.client.get("/auth/google/callback/",data=data)
            self.assertEqual(response.status_code,400)
    
    @patch.object(UserGoogleLoginCallback,"verify_state",return_value=True)
    @patch("requests.get")
    @patch("requests.post")
    def test_google_callback_view_with_ok_registered_user(self,mock_post:MagicMock,mock_get:MagicMock,mock_state:MagicMock):
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
        self.assertIn("email",response.data)
        self.assertIn("is_superuser",response.data)
    
    @patch.object(UserGoogleLoginCallback,"verify_state",return_value=False)       
    def test_google_callback_view_state_dismatch(self,mock):
        data = {
            "code": "code",
            "state": "state",
        }
        self.client.get("/auth/google/")
        response = self.client.get("/auth/google/callback/",data=data)
        self.assertEqual(response.status_code,400)