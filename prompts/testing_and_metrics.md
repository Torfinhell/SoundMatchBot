# Testing and Metrics

## Testing Strategy

### Unit Tests (Backend)
- **Database models**: test creation, relationships, constraints.
- **API endpoints**: using `pytest` and `httpx` to test each endpoint with valid/invalid inputs.
- **FAISS wrapper**: test add/search with dummy embeddings.
- **Matching algorithm**: test text filter and music rerank with mock data.
- **Redis cache**: test set/get/invalidate.

### Integration Tests
- Test the full flow: user registration → poll creation → poll submission → recommendations.
- Ensure FAISS and PostgreSQL are consistent.
- Test background embedding extraction.

### Frontend Tests (Telegram Bot)
- Mock Telegram updates and test handler logic.
- Use `pytest` with `python-telegram-bot` test utilities.

### Frontend Tests (React)
- Unit tests for components (Jest + React Testing Library).
- Integration tests for API calls (mocking Axios).

## Metrics to Monitor

### Performance
- **API response time** (95th percentile) – target <200ms for cached endpoints.
- **Embedding extraction time** – should be acceptable for background jobs.
- **FAISS search latency** – log and alert if >100ms.

### Accuracy
- **User satisfaction** – implicit feedback: how often users view rankings, click on profiles.
- **Poll completion rate** – measure engagement.
- **Ranking relevance** – A/B test with random vs. algorithm.

### System Health
- **Redis cache hit rate** – aim >80%.
- **Database connection pool usage**.
- **Background task queue length** (if using Celery).

## Monitoring Tools
- Prometheus + Grafana for metrics.
- ELK stack for logs.
- Sentry for error tracking.

## Load Testing
- Simulate multiple users with Locust.
- Test endpoints: `/recommendations`, `/polls/active`, `/leaderboard`.
- Ensure system scales.