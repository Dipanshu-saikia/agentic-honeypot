# ⚡ QUICK REFERENCE CARD

## 🚀 DEPLOYMENT COMMANDS

### Render.com Configuration
```
Build Command:    pip install -r requirements.txt
Start Command:    uvicorn main:app --host 0.0.0.0 --port $PORT
Environment:      Python 3
```

### Environment Variables
```
API_KEY = buildathon-secret-2026  (change this!)
```

---

## 🧪 LOCAL TESTING

### Start Service
```bash
python main.py
```

### Run Tests
```bash
python test_optimizations.py
```

### Quick Test Commands
```bash
# Health Check
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics

# Test Honeypot
curl -X POST http://localhost:8000/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: buildathon-secret-2026" \
  -d '{"session_id":"test-001","message":"urgent verify otp"}'
```

---

## 📊 KEY METRICS TO MONITOR

| Metric | Healthy Range | Action If Outside Range |
|--------|---------------|-------------------------|
| `active_sessions` | 0-500 | >500: Increase MAX_SESSIONS or reduce TTL |
| `circuit_breaker_active` | false | true: Check callback endpoint, wait 5min |
| `average_scam_score` | 0-10 | >20: Possible attack, review logs |
| Response time | <100ms | >200ms: Check session count, reduce limits |

---

## 🔧 CONFIGURATION QUICK TWEAKS

### For Higher Traffic (Paid Tier)
```python
MAX_SESSIONS = 2000
SESSION_TTL_MINUTES = 60
RATE_LIMIT_REQUESTS = 20
```

### For Lower Resources
```python
MAX_SESSIONS = 200
SESSION_TTL_MINUTES = 15
MAX_CONVERSATION_HISTORY = 5
```

### For Stricter Security
```python
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW = 60
```

---

## 🐛 TROUBLESHOOTING QUICK FIXES

| Problem | Solution |
|---------|----------|
| Service won't start | Check port 8000 availability, verify dependencies |
| Rate limit errors | Wait 60s or increase RATE_LIMIT_REQUESTS |
| Callbacks failing | Check /metrics for circuit breaker, verify GUVI_CALLBACK_URL |
| High memory | Reduce MAX_SESSIONS to 300, SESSION_TTL to 15 |
| Slow responses | Check active_sessions count, reduce if >400 |

---

## 📝 API ENDPOINTS CHEAT SHEET

### POST /honeypot
**Headers:** `x-api-key: your-api-key`
**Body:** `{"session_id": "string", "message": "string"}`
**Returns:** `{"session_id": "string", "reply": "string", "status": "engaged"}`

### GET /health
**No auth required**
**Returns:** `{"status": "healthy", "timestamp": "..."}`

### GET /metrics
**No auth required**
**Returns:** Full metrics JSON (see README.md)

---

## ✅ PRE-DEPLOYMENT CHECKLIST

- [ ] Changed API_KEY from default value
- [ ] Tested locally with `python main.py`
- [ ] Ran test suite with `python test_optimizations.py`
- [ ] Verified /health endpoint responds
- [ ] Verified /metrics endpoint responds
- [ ] Tested honeypot with sample scam message
- [ ] Reviewed DEPLOYMENT.md for Render.com setup
- [ ] Committed all files to Git repository
- [ ] Connected repository to Render.com
- [ ] Set environment variables in Render dashboard

---

## 🎯 OPTIMIZATION CATEGORIES (ALL 10 APPLIED)

1. ✅ Async Optimization
2. ✅ Memory Optimization
3. ✅ Intelligence Extraction Efficiency
4. ✅ Response Generation Optimization
5. ✅ Callback Optimization
6. ✅ Security Hardening
7. ✅ Monitoring & Logging
8. ✅ Render.com-Specific Optimizations
9. ✅ Code Quality Improvements
10. ✅ Edge Case Handling

---

## 📚 DOCUMENTATION FILES

- **README.md** - Main documentation, quick start
- **DEPLOYMENT.md** - Complete Render.com guide
- **OPTIMIZATION_SUMMARY.md** - Technical deep dive
- **QUICK_REFERENCE.md** - This file (cheat sheet)

---

## 🔥 CRITICAL FEATURES

### Weighted Keyword Scoring
```python
"urgent urgent urgent" → score = 3 (not 1!)
```

### Memory Bounded
```python
Max 500 sessions, auto-cleanup after 30min
```

### Circuit Breaker
```python
Disables callbacks after 5 failures, auto-resets
```

### Rate Limiting
```python
10 requests/min per session, returns 429 if exceeded
```

---

## 📞 QUICK SUPPORT

1. **Deployment issues?** → Read DEPLOYMENT.md
2. **Performance issues?** → Check /metrics endpoint
3. **Technical details?** → Read OPTIMIZATION_SUMMARY.md
4. **Local testing?** → Run test_optimizations.py

---

**🚀 READY TO DEPLOY!**

Your service is production-ready with all Anti-Gravity optimizations applied.

Built for India AI Impact Buildathon 2026 ❤️
