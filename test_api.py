"""
Quick test script for the API
"""
import requests
import json

# Test 1: Health Check
print("=" * 60)
print("TEST 1: Health Check")
print("=" * 60)
response = requests.get("http://localhost:8000/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

# Test 2: Categories
print("=" * 60)
print("TEST 2: Get Categories")
print("=" * 60)
response = requests.get("http://localhost:8000/categories")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

# Test 3: Classify a ticket
print("=" * 60)
print("TEST 3: Classify Ticket")
print("=" * 60)
test_tickets = [
    "I forgot my password and cannot login",
    "My laptop screen is cracked and needs replacement",
    "How do I submit a vacation request?",
   "The website is loading very slowly",
    "I need access to the shared drive"
]

for ticket_text in test_tickets:
    print(f"\n📩 Ticket: \"{ticket_text}\"")
    print("-" * 60)
    
    response = requests.post(
        "http://localhost:8000/classify",
        json={"text": ticket_text}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Category: {result['category']}")
        print(f"   Priority: {result['priority']}")
        print(f"   Confidence: {result['confidence']:.2%}")
        print(f"   Route to: {result['routing_team']}")
        print(f"   Similar tickets found: {len(result.get('similar_tickets', []))}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")

print("\n" + "=" * 60)
print("✅ ALL TESTS COMPLETE!")
print("=" * 60)
print("\n💡 Visit http://localhost:8000/docs for interactive API documentation")
