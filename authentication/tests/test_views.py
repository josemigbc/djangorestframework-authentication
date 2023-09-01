from rest_framework.test import APITestCase,APIRequestFactory
from django.contrib.auth import get_user_model
from authentication.views import UserDetailsUpdateView,UserChangePasswordView
from authentication.serializers import UserSerializer,UserUpdateSerializer

User = get_user_model()

class UserCreationViewTest(APITestCase):
    
    def test_status_code_with_ok(self):
        data = {
            "username": "test",
            "password": "testing1234",
        }
        
        response = self.client.post('/auth/signup/',data)
        self.assertEqual(response.status_code,201)
    
    def test_status_code_with_bad_data(self):
        data = {
            "password": "testing1234",
        }
        
        response = self.client.post('/auth/signup/',data)
        self.assertEqual(response.status_code,400)
        
class UserDetailsUpdateViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",password="testing1234")
        cls.view = UserDetailsUpdateView()
        cls.factory = APIRequestFactory()
    
    def setUp(self) -> None:
        self.client.login(username="test",password="testing1234")
        
    def test_status_code_with_get(self):
        response = self.client.get("/auth/user/")
        self.assertEqual(response.status_code,200)
        
    def test_status_code_with_patch(self):
        data = {
            "first_name": "test2",
        }
        
        response = self.client.patch("/auth/user/",data)
        self.assertEqual(response.status_code,200)
    
    def test_get_serializer_class_and_object_with_patch(self):
        
        request = self.factory.patch("/auth/user/")
        request.user = self.user
        
        self.view.request = request
        serializer = self.view.get_serializer_class()
        obj = self.view.get_object()
        
        self.assertEqual(serializer,UserUpdateSerializer)
        self.assertEqual(obj,self.user)
    
    def test_get_serializer_class_and_object_with_get(self):
        
        request = self.factory.get("/auth/user/")
        request.user = self.user
        self.view.request = request
        
        serializer = self.view.get_serializer_class()
        obj = self.view.get_object()
        
        self.assertEqual(serializer,UserSerializer)
        self.assertEqual(obj,self.user)
        
class UserChangePasswordViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",password="testing1234")
        cls.view = UserChangePasswordView()
        cls.factory = APIRequestFactory()
        cls.data = data ={
            "password": "testing1234",
            "new_password": "testing123",
        }
        
    def test_status_code(self):
        self.client.login(username="test",password="testing1234")
        response = self.client.patch("/auth/changepassword/",self.data)
        self.assertEqual(response.status_code,200)
        
    def test_get_object(self):
        request = self.factory.patch("/auth/changepassword/",self.data)
        request.user = self.user
        self.view.request = request
        
        obj = self.view.get_object()
        self.assertEqual(obj,self.user)

class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",password="testing1234")
        
    def test_with_ok(self):
        data = {
            "username": "test",
            "password": "testing1234",
        }
        response = self.client.post("/auth/login/",data=data)
        self.assertEqual(response.status_code,200)
        self.assertIn("username",response.data)
    
    def test_with_fail(self):
        data = {
            "username": "test",
            "password": "testing123",
        }
        response = self.client.post("/auth/login/",data=data)
        self.assertEqual(response.status_code,401)