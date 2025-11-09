#!/usr/bin/env python3
"""
Comprehensive test script for all API routes through Nginx Gateway.
Tests routing to both backend and users-service.
"""
import asyncio
import httpx
from typing import Optional, Dict, Any


class GatewayTester:
    """Test all routes through API Gateway."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.article_id: Optional[int] = None
        self.comment_id: Optional[int] = None
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def log_test(self, name: str, passed: bool, details: str = ""):
        """Log test result."""
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} | {name}")
        if details:
            print(f"       {details}")
        
        if passed:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{name}: {details}")
    
    async def test_gateway_health(self, client: httpx.AsyncClient):
        """Test 1: Gateway health endpoint."""
        print("\n" + "="*70)
        print("GATEWAY HEALTH CHECKS")
        print("="*70)
        
        try:
            response = await client.get("/healthz")
            self.log_test(
                "Gateway /healthz",
                response.status_code == 200,
                f"Status: {response.status_code}, Response: {response.json()}"
            )
        except Exception as e:
            self.log_test("Gateway /healthz", False, str(e))
        
        try:
            response = await client.get("/")
            self.log_test(
                "Gateway root /",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.log_test("Gateway root /", False, str(e))
    
    async def test_users_service_routes(self, client: httpx.AsyncClient):
        """Test 2-6: Users service routes through gateway."""
        print("\n" + "="*70)
        print("USERS SERVICE ROUTES (via /api/users/* and /api/user)")
        print("="*70)
        
        # Test 2: Register new user
        import random
        email = f"test{random.randint(1000, 9999)}@example.com"
        username = f"user{random.randint(1000, 9999)}"
        
        try:
            response = await client.post(
                "/api/users",
                json={
                    "email": email,
                    "username": username,
                    "password": "testpass123"
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']['access_token']
                self.user_id = data['user']['id']
                self.log_test(
                    "POST /api/users (register)",
                    True,
                    f"User created: {username} (ID: {self.user_id})"
                )
            else:
                self.log_test(
                    "POST /api/users (register)",
                    False,
                    f"Status: {response.status_code}, Response: {response.text[:100]}"
                )
        except Exception as e:
            self.log_test("POST /api/users (register)", False, str(e))
        
        # Test 3: Login
        try:
            response = await client.post(
                "/api/users/login",
                json={
                    "email": email,
                    "password": "testpass123"
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']['access_token']
                self.log_test(
                    "POST /api/users/login",
                    True,
                    f"Token: {self.token[:30]}..."
                )
            else:
                self.log_test(
                    "POST /api/users/login",
                    False,
                    f"Status: {response.status_code}"
                )
        except Exception as e:
            self.log_test("POST /api/users/login", False, str(e))
        
        if not self.token:
            print("\n⚠ No token available, skipping authenticated tests")
            return
        
        # Test 4: Get current user profile
        try:
            response = await client.get(
                "/api/user",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            self.log_test(
                "GET /api/user (current profile)",
                response.status_code == 200,
                f"Status: {response.status_code}, User: {response.json().get('user', {}).get('username') if response.status_code == 200 else ''}"
            )
        except Exception as e:
            self.log_test("GET /api/user (current profile)", False, str(e))
        
        # Test 5: Update user profile
        try:
            response = await client.put(
                "/api/user",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "bio": "Updated bio via gateway",
                    "image_url": "https://example.com/avatar.jpg"
                }
            )
            self.log_test(
                "PUT /api/user (update profile)",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.log_test("PUT /api/user (update profile)", False, str(e))
        
        # Test 6: Get user by ID
        if self.user_id:
            try:
                response = await client.get(f"/api/users/{self.user_id}")
                self.log_test(
                    f"GET /api/users/{self.user_id} (public profile)",
                    response.status_code == 200,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.log_test(f"GET /api/users/{self.user_id}", False, str(e))
    
    async def test_backend_article_routes(self, client: httpx.AsyncClient):
        """Test 7-11: Backend article routes through gateway."""
        print("\n" + "="*70)
        print("BACKEND ARTICLE ROUTES (via /api/articles/*)")
        print("="*70)
        
        if not self.token:
            print("\n⚠ No token available, skipping article tests")
            return
        
        # Test 7: Create article
        try:
            response = await client.post(
                "/api/articles",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "title": "Test Article via Gateway",
                    "description": "Testing article creation through API Gateway",
                    "body": "Full article body content here",
                    "tag_list": ["test", "gateway", "microservices"]
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.article_id = data['id']
                self.log_test(
                    "POST /api/articles (create)",
                    True,
                    f"Article created: ID {self.article_id}"
                )
            else:
                self.log_test(
                    "POST /api/articles (create)",
                    False,
                    f"Status: {response.status_code}, Response: {response.text[:100]}"
                )
        except Exception as e:
            self.log_test("POST /api/articles (create)", False, str(e))
        
        # Test 8: List all articles
        try:
            response = await client.get("/api/articles")
            if response.status_code == 200:
                articles = response.json()
                self.log_test(
                    "GET /api/articles (list)",
                    True,
                    f"Found {len(articles)} articles"
                )
            else:
                self.log_test(
                    "GET /api/articles (list)",
                    False,
                    f"Status: {response.status_code}"
                )
        except Exception as e:
            self.log_test("GET /api/articles (list)", False, str(e))
        
        if not self.article_id:
            print("\n⚠ No article ID, skipping article detail tests")
            return
        
        # Test 9: Get specific article
        try:
            response = await client.get(f"/api/articles/{self.article_id}")
            self.log_test(
                f"GET /api/articles/{self.article_id} (detail)",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.log_test(f"GET /api/articles/{self.article_id}", False, str(e))
        
        # Test 10: Update article
        try:
            response = await client.put(
                f"/api/articles/{self.article_id}",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "title": "Updated Article Title",
                    "description": "Updated description"
                }
            )
            self.log_test(
                f"PUT /api/articles/{self.article_id} (update)",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.log_test(f"PUT /api/articles/{self.article_id}", False, str(e))
        
        # Test 11: Delete article (will test at the end)
        # Keeping article for comment tests
    
    async def test_backend_comment_routes(self, client: httpx.AsyncClient):
        """Test 12-15: Backend comment routes through gateway."""
        print("\n" + "="*70)
        print("BACKEND COMMENT ROUTES (via /api/articles/{id}/comments/*)")
        print("="*70)
        
        if not self.token or not self.article_id:
            print("\n⚠ No token or article ID, skipping comment tests")
            return
        
        # Test 12: Create comment
        try:
            response = await client.post(
                f"/api/articles/{self.article_id}/comments",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "body": "Test comment via gateway"
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.comment_id = data['id']
                self.log_test(
                    f"POST /api/articles/{self.article_id}/comments (create)",
                    True,
                    f"Comment created: ID {self.comment_id}"
                )
            else:
                self.log_test(
                    f"POST /api/articles/{self.article_id}/comments (create)",
                    False,
                    f"Status: {response.status_code}, Response: {response.text[:100]}"
                )
        except Exception as e:
            self.log_test(f"POST /api/articles/{self.article_id}/comments", False, str(e))
        
        # Test 13: List comments for article
        try:
            response = await client.get(f"/api/articles/{self.article_id}/comments")
            if response.status_code == 200:
                comments = response.json()
                self.log_test(
                    f"GET /api/articles/{self.article_id}/comments (list)",
                    True,
                    f"Found {len(comments)} comments"
                )
            else:
                self.log_test(
                    f"GET /api/articles/{self.article_id}/comments (list)",
                    False,
                    f"Status: {response.status_code}"
                )
        except Exception as e:
            self.log_test(f"GET /api/articles/{self.article_id}/comments", False, str(e))
        
        # Test 14: Delete comment
        if self.comment_id:
            try:
                response = await client.delete(
                    f"/api/articles/{self.article_id}/comments/{self.comment_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                self.log_test(
                    f"DELETE /api/articles/{self.article_id}/comments/{self.comment_id}",
                    response.status_code in [200, 204],
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.log_test(f"DELETE /api/articles/{self.article_id}/comments/{self.comment_id}", False, str(e))
        
        # Test 15: Delete article (cleanup)
        if self.article_id:
            try:
                response = await client.delete(
                    f"/api/articles/{self.article_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                self.log_test(
                    f"DELETE /api/articles/{self.article_id}",
                    response.status_code in [200, 204],
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.log_test(f"DELETE /api/articles/{self.article_id}", False, str(e))
    
    async def test_service_health_via_gateway(self, client: httpx.AsyncClient):
        """Test 16-17: Service health checks via gateway."""
        print("\n" + "="*70)
        print("SERVICE HEALTH CHECKS (via gateway)")
        print("="*70)
        
        # Test 16: Backend health
        try:
            response = await client.get("/backend/healthz")
            self.log_test(
                "GET /backend/healthz",
                response.status_code == 200,
                f"Status: {response.status_code}, Response: {response.json() if response.status_code == 200 else ''}"
            )
        except Exception as e:
            self.log_test("GET /backend/healthz", False, str(e))
        
        # Test 17: Users service health
        try:
            response = await client.get("/users/healthz")
            self.log_test(
                "GET /users/healthz",
                response.status_code == 200,
                f"Status: {response.status_code}, Response: {response.json() if response.status_code == 200 else ''}"
            )
        except Exception as e:
            self.log_test("GET /users/healthz", False, str(e))
    
    async def run_all_tests(self):
        """Run all tests."""
        print("\n" + "="*70)
        print("MICROSERVICES API GATEWAY - COMPREHENSIVE ROUTE TEST")
        print("="*70)
        print(f"Testing against: {self.base_url}")
        
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            await self.test_gateway_health(client)
            await self.test_users_service_routes(client)
            await self.test_backend_article_routes(client)
            await self.test_backend_comment_routes(client)
            await self.test_service_health_via_gateway(client)
        
        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✓ Passed: {self.results['passed']}")
        print(f"✗ Failed: {self.results['failed']}")
        print(f"Total:   {self.results['passed'] + self.results['failed']}")
        
        if self.results['errors']:
            print("\nFailed tests:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("="*70 + "\n")
        
        return self.results['failed'] == 0


async def main():
    """Main entry point."""
    tester = GatewayTester()
    success = await tester.run_all_tests()
    
    # Exit with appropriate code
    import sys
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
