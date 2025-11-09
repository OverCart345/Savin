#!/usr/bin/env python3
"""Test API Gateway routing."""
import asyncio
import httpx


async def test_gateway():
    """Test API Gateway routing to microservices."""
    print("\n" + "="*60)
    print("API GATEWAY ROUTING TEST")
    print("="*60)
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(base_url=base_url) as client:
        # 1. Test gateway root
        print("\n1. Testing gateway root endpoint...")
        response = await client.get("/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # 2. Test gateway healthz
        print("\n2. Testing gateway health check...")
        response = await client.get("/healthz")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # 3. Test routing to users-service (login)
        print("\n3. Testing routing to users-service (login)...")
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = await client.post("/api/users/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data['token']['access_token']
            print(f"✓ Logged in as: {data['user']['username']}")
            print(f"✓ Token: {token[:30]}...")
            
            # 4. Test routing to users-service (get profile)
            print("\n4. Testing routing to users-service (get profile)...")
            response = await client.get(
                "/api/user",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                user = response.json()['user']
                print(f"✓ Profile: {user['username']} ({user['email']})")
            
            # 5. Test routing to backend (list articles)
            print("\n5. Testing routing to backend (list articles)...")
            response = await client.get("/api/articles")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                articles = response.json()
                print(f"✓ Found {len(articles)} articles")
                for article in articles[:3]:
                    print(f"  - {article['title']} (author_id: {article['author_id']})")
            
            # 6. Test routing to backend (create article)
            print("\n6. Testing routing to backend (create article via gateway)...")
            article_data = {
                "title": "Article via Gateway",
                "description": "Created through API Gateway",
                "body": "This article was created using the API Gateway routing",
                "tag_list": ["gateway", "test"]
            }
            response = await client.post(
                "/api/articles",
                json=article_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                article = response.json()
                print(f"✓ Created: {article['title']} (ID: {article['id']})")
            
            # 7. Test backend health through gateway
            print("\n7. Testing backend health through gateway...")
            response = await client.get("/backend/healthz")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ Backend health: {response.json()}")
            
            # 8. Test users health through gateway
            print("\n8. Testing users-service health through gateway...")
            response = await client.get("/users/healthz")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ Users-service health: {response.json()}")
        
        else:
            print(f"✗ Login failed: {response.json()}")
    
    print("\n" + "="*60)
    print("API GATEWAY TEST COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_gateway())
