# 🚀 RENDER.COM DEPLOYMENT GUIDE

## Quick Deploy Checklist

### 1. **Create New Web Service on Render.com**
- Go to https://render.com/dashboard
- Click "New +" → "Web Service"
- Connect your GitHub repository

### 2. **Configure Build Settings**

**Environment:** `Python 3`

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. **Environment Variables**

Add these in the Render.com dashboard:

| Key | Value | Notes |
|-----|-------|-------|
| `API_KEY` | `buildathon-secret-2026` | Change this to your actual API key |
| `PORT` | (Auto-set by Render) | Don't manually set this |

### 4. **Instance Settings**

- **Instance Type:** Free
- **Region:** Choose closest to India (Singapore recommended)
- **Auto-Deploy:** Yes (optional)

### 5. **Health Check Configuration**

Render.com will automatically ping your service. The `/health` endpoint is configured to respond.

**Health Check Path:** `/health`

---

## Testing Your Deployment

### 1. **Test Health Endpoint**
```bash
curl https://your-service.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2026-02-02T12:44:42"}
```

### 2. **Test Metrics Endpoint**
```bash
curl https://your-service.onrender.com/metrics
```

Expected response:
```json
{
  "active_sessions": 0,
  "total_callbacks_sent": 0,
  "total_callbacks_failed": 0,
  "total_requests": 0,
  "average_scam_score": 0.0,
  "circuit_breaker_active": false,
  "failed_callbacks_queued": 0,
  "rate_limit_tracked_sessions": 0
}
```

### 3. **Test Honeypot Endpoint**
```bash
curl -X POST https://your-service.onrender.com/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: buildathon-secret-2026" \
  -d '{
    "session_id": "test-session-001",
    "message": "Your account will be blocked! Send OTP urgently to verify: 1234567890"
  }'
```

Expected response:
```json
{
  "session_id": "test-session-001",
  "reply": "Oh no, is my account really blocked? I'm worried!",
  "status": "engaged"
}
```

---

## Performance Optimizations Applied

### ✅ Memory Efficiency
- **LRU Eviction:** Max 500 sessions, oldest removed first
- **TTL Cleanup:** Sessions older than 30 minutes auto-deleted
- **Conversation Limits:** Only last 10 messages stored per session

### ✅ CPU Efficiency
- **Single Worker:** Optimized for free tier (512MB RAM)
- **Connection Pooling:** Reuses HTTP connections
- **Early Exit Logic:** Skips processing for short messages (<10 chars)
- **Lazy Evaluation:** Only extracts expensive patterns when needed

### ✅ Network Efficiency
- **Global HTTP Client:** Persistent connections to callback endpoint
- **Circuit Breaker:** Disables callbacks after 5 consecutive failures
- **Retry Logic:** 3 attempts with exponential backoff

### ✅ Security
- **Rate Limiting:** Max 10 requests per session per minute
- **Input Validation:** Rejects malformed/suspicious input
- **DoS Protection:** Session limits prevent memory exhaustion

---

## Monitoring in Production

### View Logs
In Render.com dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for structured JSON logs with metrics

### Key Metrics to Watch
- **Active Sessions:** Should stay under 500
- **Circuit Breaker Status:** Should be `false` (if `true`, callback endpoint is down)
- **Response Time:** Should be under 100ms for most requests
- **Callback Success Rate:** Should be >95%

---

## Troubleshooting

### Issue: Service keeps restarting
**Solution:** Check logs for memory errors. Free tier has 512MB limit.
- Reduce `MAX_SESSIONS` to 300 in `main.py`
- Reduce `MAX_CONVERSATION_HISTORY` to 5

### Issue: Callbacks not being sent
**Solution:** Check circuit breaker status at `/metrics`
- If active, wait 5 minutes for auto-reset
- Verify GUVI callback URL is correct
- Check logs for HTTP errors

### Issue: Rate limit errors
**Solution:** Legitimate traffic hitting limits
- Increase `RATE_LIMIT_REQUESTS` to 20 in `main.py`
- Or increase `RATE_LIMIT_WINDOW` to 120 seconds

### Issue: High response times
**Solution:** Too many sessions or slow regex
- Check `/metrics` for active session count
- Reduce `SESSION_TTL_MINUTES` to 15 for faster cleanup
- Verify cleanup task is running (check logs)

---

## Advanced Configuration

### Custom Domain (Optional)
1. Go to service settings
2. Add custom domain
3. Update DNS records as instructed

### Scaling (Paid Tiers Only)
If you upgrade from free tier:
- Increase `MAX_SESSIONS` to 2000+
- Enable multiple workers (change `workers=1` to `workers=4`)
- Consider Redis for session storage instead of in-memory

---

## Security Best Practices

### 1. Change API Key
```bash
# In Render.com dashboard, update API_KEY to a strong random value
openssl rand -hex 32
```

### 2. Enable HTTPS Only
Render.com provides free SSL certificates automatically.

### 3. Monitor Logs Regularly
Watch for:
- Unauthorized access attempts
- Suspicious content patterns
- Unusual traffic spikes

---

## Performance Benchmarks (Expected)

On Render.com free tier:

| Metric | Expected Value |
|--------|---------------|
| Response Time (avg) | 50-100ms |
| Concurrent Sessions | 100-500 |
| Requests/minute | 600+ |
| Memory Usage | 200-400MB |
| Callback Success Rate | >95% |

---

## Support

If you encounter issues:
1. Check `/metrics` endpoint first
2. Review logs in Render.com dashboard
3. Verify environment variables are set correctly
4. Test with curl commands above

---

**🎯 Your service is now production-ready with Anti-Gravity optimizations!**
