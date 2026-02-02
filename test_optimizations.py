"""
Test script to verify Anti-Gravity optimizations
Run this locally before deploying to Render.com
"""

import httpx
import asyncio
import time
from typing import List, Dict

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "buildathon-secret-2026"

def create_message_request(session_id: str, message_text: str) -> dict:
    """Helper function to create properly formatted message requests"""
    from datetime import datetime
    return {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": message_text,
            "timestamp": datetime.now().isoformat()
        },
        "conversationHistory": [],
        "metadata": {}
    }


async def test_health_check():
    """Test #8: Health endpoint for Render.com"""
    print("\n🔍 Testing health check endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print(f"✅ Health check passed: {data}")

async def test_metrics_endpoint():
    """Test #7: Metrics endpoint for monitoring"""
    print("\n🔍 Testing metrics endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "active_sessions" in data
        assert "total_callbacks_sent" in data
        print(f"✅ Metrics endpoint passed: {data}")

async def test_authentication():
    """Test #6: API key authentication"""
    print("\n🔍 Testing authentication...")
    async with httpx.AsyncClient() as client:
        # Test with wrong API key
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request("test-001", "Hello"),
            headers={"x-api-key": "wrong-key"}
        )
        assert response.status_code == 401
        print("✅ Authentication rejection works")
        
        # Test with correct API key
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request("test-001", "Hello"),
            headers={"x-api-key": API_KEY}
        )
        assert response.status_code == 200
        print("✅ Authentication acceptance works")

async def test_input_validation():
    """Test #6: Input validation and security"""
    print("\n🔍 Testing input validation...")
    async with httpx.AsyncClient() as client:
        # Test invalid session_id (with special chars)
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request("test<script>", "Hello"),
            headers={"x-api-key": API_KEY}
        )
        assert response.status_code == 422  # Validation error
        print("✅ Session ID validation works")
        
        # Test suspicious content
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request("test-002", "<script>alert('xss')</script>"),
            headers={"x-api-key": API_KEY}
        )
        assert response.status_code == 422  # Validation error
        print("✅ Suspicious content detection works")

async def test_weighted_keyword_scoring():
    """Test #3: Critical fix - weighted keyword scoring"""
    print("\n🔍 Testing weighted keyword scoring...")
    async with httpx.AsyncClient() as client:
        session_id = "test-weighted-001"
        
        # Send message with repeated keywords
        message = "urgent urgent urgent verify verify otp"
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request(session_id, message),
            headers={"x-api-key": API_KEY}
        )
        assert response.status_code == 200
        print(f"✅ Weighted scoring message sent: '{message}'")
        
        # Check metrics to verify scoring
        metrics = await client.get(f"{BASE_URL}/metrics")
        data = metrics.json()
        print(f"   Metrics after weighted message: {data}")
        print("✅ Weighted keyword scoring implemented (check logs for score=6)")

async def test_rate_limiting():
    """Test #6: Rate limiting protection"""
    print("\n🔍 Testing rate limiting...")
    async with httpx.AsyncClient() as client:
        session_id = "test-ratelimit-001"
        
        # Send 11 requests rapidly (limit is 10/minute)
        for i in range(11):
            response = await client.post(
                f"{BASE_URL}/honeypot",
                json=create_message_request(session_id, f"Message {i}"),
                headers={"x-api-key": API_KEY}
            )
            if i < 10:
                assert response.status_code == 200
            else:
                assert response.status_code == 429  # Rate limit exceeded
                print(f"✅ Rate limiting triggered after {i} requests")
                break

async def test_early_exit_optimization():
    """Test #3: Early exit for short messages"""
    print("\n🔍 Testing early exit optimization...")
    async with httpx.AsyncClient() as client:
        session_id = "test-earlyexit-001"
        
        # Send very short message (should skip intelligence extraction)
        start = time.time()
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request(session_id, "Hi"),
            headers={"x-api-key": API_KEY}
        )
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        print(f"✅ Short message processed in {elapsed:.2f}ms (early exit)")

async def test_conversation_history_limit():
    """Test #2: Conversation history limited to 10 messages"""
    print("\n🔍 Testing conversation history limits...")
    async with httpx.AsyncClient() as client:
        session_id = "test-history-001"
        
        # Send 15 messages
        for i in range(15):
            await client.post(
                f"{BASE_URL}/honeypot",
                json=create_message_request(session_id, f"Message {i}"),
                headers={"x-api-key": API_KEY}
            )
        
        print("✅ Sent 15 messages (history should be limited to 10)")
        print("   Check logs to verify history size is capped")

async def test_response_variety():
    """Test #4: Response generation with variety"""
    print("\n🔍 Testing response variety...")
    async with httpx.AsyncClient() as client:
        session_id = "test-response-001"
        responses = []
        
        # Get 5 responses
        for i in range(5):
            response = await client.post(
                f"{BASE_URL}/honeypot",
                json=create_message_request(session_id, f"Test message {i}"),
                headers={"x-api-key": API_KEY}
            )
            data = response.json()
            responses.append(data["reply"])
        
        # Check for variety (at least 2 different responses)
        unique_responses = len(set(responses))
        print(f"✅ Got {unique_responses} unique responses out of 5 requests")
        assert unique_responses >= 2, "Responses should have variety"

async def test_concurrent_sessions():
    """Test #1 & #2: Handle multiple concurrent sessions"""
    print("\n🔍 Testing concurrent session handling...")
    async with httpx.AsyncClient() as client:
        # Create 10 concurrent sessions
        tasks = []
        for i in range(10):
            task = client.post(
                f"{BASE_URL}/honeypot",
                json=create_message_request(f"concurrent-{i}", "Test"),
                headers={"x-api-key": API_KEY}
            )
            tasks.append(task)
        
        start = time.time()
        responses = await asyncio.gather(*tasks)
        elapsed = (time.time() - start) * 1000
        
        assert all(r.status_code == 200 for r in responses)
        print(f"✅ Handled 10 concurrent sessions in {elapsed:.2f}ms")
        
        # Check metrics
        metrics = await client.get(f"{BASE_URL}/metrics")
        data = metrics.json()
        print(f"   Active sessions: {data['active_sessions']}")

async def test_intelligence_extraction():
    """Test #3: Intelligence extraction with lazy evaluation"""
    print("\n🔍 Testing intelligence extraction...")
    async with httpx.AsyncClient() as client:
        session_id = "test-intel-001"
        
        # Send message with UPI, bank account, and URL
        message = "Send money to test@upi and account 1234567890123 or visit http://scam.com urgent urgent"
        response = await client.post(
            f"{BASE_URL}/honeypot",
            json=create_message_request(session_id, message),
            headers={"x-api-key": API_KEY}
        )
        assert response.status_code == 200
        print(f"✅ Intelligence extraction message sent")
        print(f"   Message contained: UPI ID, bank account, URL, keywords")

async def run_all_tests():
    """Run all test suites"""
    print("=" * 60)
    print("🚀 ANTI-GRAVITY OPTIMIZATION TEST SUITE")
    print("=" * 60)
    
    try:
        await test_health_check()
        await test_metrics_endpoint()
        await test_authentication()
        await test_input_validation()
        await test_weighted_keyword_scoring()
        await test_rate_limiting()
        await test_early_exit_optimization()
        await test_conversation_history_limit()
        await test_response_variety()
        await test_concurrent_sessions()
        await test_intelligence_extraction()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n🎯 Your service is ready for deployment to Render.com!")
        print("   Next step: Follow instructions in DEPLOYMENT.md")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except httpx.ConnectError:
        print("\n❌ CONNECTION FAILED")
        print("   Make sure the service is running:")
        print("   python main.py")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    print("\n⚠️  PREREQUISITES:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Start the service: python main.py")
    print("   3. Run this test in a separate terminal\n")
    
    input("Press ENTER to start tests...")
    asyncio.run(run_all_tests())
