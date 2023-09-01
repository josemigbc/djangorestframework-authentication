from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch,Mock
from authentication.serializers import UserChangePasswordSerializer,UserCreationSerializer,UserSerializer,UserUpdateSerializer

User = get_user_model()

class UserCreationSerializerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {
            "username": "test",
            "email": "test@test.com",
            "password": "testing1234",
        }
    
    def test_is_valid_with_ok(self):
        serializer = UserCreationSerializer(data=self.data)
        is_valid = serializer.is_valid()
        
        self.assertTrue(is_valid)
        
    def is_valid_with_no_a_field(self,field):
        data = self.data.copy()
        data.pop(field)
        
        serializer = UserCreationSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
    
    def test_is_valid_with_no_username(self):
        self.is_valid_with_no_a_field('username')
    
    def test_is_valid_with_no_password1(self):
        self.is_valid_with_no_a_field('password')
    
    @patch.object(User,"save")
    def test_create_with_ok(self,mock:Mock):
        serializer = UserCreationSerializer()
        user = serializer.create(self.data)
        mock.assert_called_once()
        self.assertEqual(user.username,"test")
        
class UserSerializerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",password="testing1234")
    
    def test_password_is_not_included(self):
        serializer = UserSerializer(self.user)
        self.assertIn('username',serializer.data)
        self.assertNotIn('password',serializer.data)
        
class UserChangePasswordSerializerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test",password="testing1234")
        cls.data = {
            "password": "testing1234",
            "new_password": "testing12345"
        }
    
    def test_is_valid_ok(self):
        serializer = UserChangePasswordSerializer(self.user,self.data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        
    def test_is_valid_with_wrong_password(self):
        data = self.data.copy()
        data.update({"password": "testing123"})
        serializer = UserChangePasswordSerializer(self.user,data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        
    def is_valid_with_no_a_field(self,field):
        data = self.data.copy()
        data.pop(field)
        serializer = UserChangePasswordSerializer(self.user,data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        
    def test_is_valid_with_no_password(self):
        self.is_valid_with_no_a_field('password')
    
    def test_is_valid_with_no_new_password(self):
        self.is_valid_with_no_a_field('new_password')
        
    def test_update_with_ok(self):
        serializer = UserChangePasswordSerializer()
        user = serializer.update(self.user,self.data)
        self.assertTrue(user.check_password("testing12345"))