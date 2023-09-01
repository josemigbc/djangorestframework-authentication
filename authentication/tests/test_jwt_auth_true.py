from rest_framework.test import APITestCase

class JWTAuthenticationTest(APITestCase):
    
    def test_urls(self):
        response = self.client.post("/auth/token/")
        self.assertNotEqual(response.status_code,404)
        