#!/usr/bin/env python3
"""Test script for microservices interaction."""
import asyncio
import httpx


async def test_users_service():
    """Test users-service endpoints."""
    print("\n=== Testing Users Service ===\n")
    
    async with httpx.AsyncClient(base_url="http://localhost:8003") as client:
        # Try to login first
        print("1. Attempting to login with existing user...")
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        try:
            response = await client.post("/api/users/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {response.status_code}")
                print(f"User logged in: {data['user']['username']}")
                token = data['token']['access_token']
                user_id = data['user']['id']
                print(f"Token: {token[:20]}...")
                print(f"User ID: {user_id}")
            else:
                # If login fails, register new user
                print("Login failed, registering new user...")
                import random
                register_data = {
                    "email": f"test{random.randint(1000, 9999)}@example.com",
                    "username": f"testuser{random.randint(1000, 9999)}",
                    "password": "testpass123"
                }
                
                response = await client.post("/api/users", json=register_data)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"User created: {data['user']['username']}")
                    token = data['token']['access_token']
                    user_id = data['user']['id']
                    print(f"Token: {token[:20]}...")
                    print(f"User ID: {user_id}")
                else:
                    print(f"Error: {response.json()}")
                    return None, None
            
            # 2. Get user profile
            print("\n2. Getting user profile...")
            response = await client.get(
                "/api/user",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Profile: {response.json()['user']}")
            
            # 3. Get user by ID (public endpoint)
            print(f"\n3. Getting user by ID ({user_id})...")
            response = await client.get(f"/api/users/{user_id}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"User data: {response.json()}")
            
            return token, user_id
                
        except Exception as e:
            print(f"Error: {e}")
            return None, None



async def test_backend_service(token: str, user_id: int):
    """Test backend service with users-service integration."""
    print("\n=== Testing Backend Service ===\n")
    
    async with httpx.AsyncClient(base_url="http://localhost:8002") as client:
        # 1. Create an article
        print("1. Creating article (authenticated)...")
        article_data = {
            "title": "Test Article",
            "description": "This is a test article",
            "body": "Article body content",
            "tags": ["test", "demo"]
        }
        
        try:
            response = await client.post(
                "/api/articles",
                json=article_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                article = response.json()
                print(f"Article created: {article['title']}")
                print(f"Author ID: {article['author_id']}")
                article_id = article['id']
                
                # 2. Get article by ID
                print(f"\n2. Getting article (ID: {article_id})...")
                response = await client.get(f"/api/articles/{article_id}")
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"Article: {response.json()}")
                
                # 3. List articles
                print("\n3. Listing all articles...")
                response = await client.get("/api/articles")
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    articles = response.json()
                    print(f"Total articles: {len(articles)}")
                
                return article_id
            else:
                print(f"Error: {response.json()}")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            return None


async def test_integration():
    """Test full integration between services."""
    print("\n" + "="*50)
    print("MICROSERVICES INTEGRATION TEST")
    print("="*50)
    
    # Test users-service
    token, user_id = await test_users_service()
    
    if token and user_id:
        # Test backend with users-service integration
        await test_backend_service(token, user_id)
    
    print("\n" + "="*50)
    print("TEST COMPLETED")
    print("="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(test_integration())
