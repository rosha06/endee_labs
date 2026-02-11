# 🚀 Quick Start Guide - ONE COMMAND!

## Option 1: Complete Setup (Recommended for First Time)

Just run this **ONE command**:

```bash
.\setup_and_run.bat
```

This will automatically:
1. ✅ Start Endee Docker container
2. ✅ Install Python dependencies
3. ✅ Create vector index
4. ✅ Load sample tickets
5. ✅ Start API server

**That's it!** 🎉

---

## Option 2: Step-by-Step (If you want more control)

### Step 1: Start Endee
```bash
.\start_endee.bat
```

### Step 2: Run the API
```bash
.\start.bat
```

---

## What You Get

After running, you'll have:

- **Endee Server**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Test the Classifier

Visit http://localhost:8000/docs and try:

```json
{
  "text": "I forgot my password and can't login"
}
```

Expected result:
```json
{
  "category": "Authentication",
  "priority": "High",
  "confidence": 0.87,
  "routing_team": "Security Team"
}
```

---

## Stopping Everything

```bash
# Stop API: Press Ctrl+C in the terminal

# Stop Endee:
docker compose -f docker-compose-endee.yml down
```

---

## Troubleshooting

**Issue**: "Docker not found"  
**Solution**: Install Docker Desktop from https://www.docker.com/products/docker-desktop

**Issue**: "Port 8080 already in use"  
**Solution**: Stop other services using port 8080, or edit `docker-compose-endee.yml` to use a different port

**Issue**: "Cannot connect to Endee"  
**Solution**: Make sure Endee is running: `docker ps` should show `endee-server`

---

## What Changed

✅ **Endee now runs via Docker** (no complex local build)  
✅ **Python client uses HTTP API** (no SDK needed)  
✅ **One command setup** (`setup_and_run.bat`)  
✅ **Port 8080** for Endee (not 6333)  

---

**Ready? Just run**: `.\setup_and_run.bat` 🚀
