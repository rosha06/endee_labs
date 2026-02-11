# Quick Setup Guide

Follow these steps to get your ticket classifier running:

## Step 1: Install Dependencies (5 minutes)

```bash
cd c:/Users/Roshan\ Rony/Desktop/endee_labs

# Install Python packages
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 ...
```

**Note**: The `endee` package line in requirements.txt is commented out. You'll need to install Endee based on their official documentation.

## Step 2: Install/Start Endee Server

### Option A: Docker (Recommended)
```bash
docker run -p 6333:6333 endee/endee
```

### Option B: Local Installation
Follow Endee Labs documentation for local installation.

**Verify Endee is running:**
```bash
curl http://localhost:6333/health
```

## Step 3: Create Vector Index (1 minute)

```bash
python scripts/setup_endee.py
```

**Expected Output:**
```
======================================================================
🚀 Endee Index Setup
======================================================================

📡 Connecting to Endee...
✅ Created index 'support_tickets' (dim: 384, metric: cosine)

======================================================================
✅ Setup Complete!
======================================================================
```

## Step 4: Index Sample Tickets (2 minutes)

```bash
python scripts/index_tickets.py
```

**Expected Output:**
```
======================================================================
📚 Indexing Sample Tickets
======================================================================

🤖 Loading MiniLM model...
✅ Loaded model from: ./dataset/minilm_model

📄 Loading sample tickets...
✅ Loaded 20 tickets

💾 Indexing 20 tickets into Endee...
✅ Inserted 20 vectors

📊 Indexed Tickets by Category:
  • Authentication: 4 tickets
  • Billing: 5 tickets
  • Technical: 5 tickets
  • Feature Request: 3 tickets
  • General Inquiry: 3 tickets
```

## Step 5: Start the API (Running!)

```bash
python main.py
```

**Expected Output:**
```
======================================================================
🎯 Support Ticket Classifier API
======================================================================

📚 Documentation: http://localhost:8000/docs
❤️  Health Check: http://localhost:8000/health
📊 API Root: http://localhost:8000

======================================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
🤖 Initializing Ticket Classifier...
  ✓ Loaded model from ./dataset/minilm_model
  ✓ Endee client initialized
✅ API ready!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 6: Test the API! 🎉

### Method 1: Browser (Interactive Docs)
1. Open: http://localhost:8000/docs
2. Click on `POST /classify`
3. Click "Try it out"
4. Enter test data:
   ```json
   {
     "text": "I can't login to my account, reset password not working"
   }
   ```
5. Click "Execute"

### Method 2: cURL
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "I forgot my password"}'
```

### Method 3: Python
```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={"text": "App crashes when I open settings"}
)

print(response.json())
```

## Expected Classification Result

```json
{
  "category": "Authentication",
  "priority": "High",
  "confidence": 0.87,
  "routing_team": "Security Team",
  "similar_tickets": [
    {
      "text": "Cannot login to my account, forgot password",
      "category": "Authentication",
      "priority": "High",
      "similarity": 0.92
    },
    {
      "text": "Reset password link not working",
      "category": "Authentication",
      "priority": "High",
      "similarity": 0.89
    }
  ]
}
```

## Troubleshooting

### Issue: "Endee client not available"
**Solution:** Make sure Endee server is running on port 6333

### Issue: "Module not found: endee"
**Solution:** Install Endee package based on their documentation

### Issue: "Model not found"
**Solution:** The model should be in `dataset/minilm_model/`. If missing, run:
```bash
python download_model.py
```

### Issue: Port 8000 already in use
**Solution:** Change port in `main.py` to 8001 or kill the process using 8000

## Next Steps

1. ✅ Test with different ticket types
2. ✅ Check accuracy on the sample data
3. ✅ Review the code in `src/` directory
4. ✅ Modify sample tickets to match your domain
5. ✅ Deploy to GitHub for your portfolio

## File Structure

```
endee_labs/
├── data/
│   └── sample_tickets.json      ✅ Created (20 tickets)
├── dataset/
│   └── minilm_model/            ✅ Downloaded
├── src/
│   ├── __init__.py              ✅ Created
│   ├── endee_client.py          ✅ Created
│   ├── classifier.py            ✅ Created
│   └── api.py                   ✅ Created
├── scripts/
│   ├── setup_endee.py           ✅ Created
│   └── index_tickets.py         ✅ Created
├── main.py                      ✅ Created
├── requirements.txt             ✅ Created
├── .env                         ✅ Created
└── README.md                    ✅ Created
```

## Total Time: ~10 minutes

You now have a fully functional AI-powered ticket classifier! 🚀
