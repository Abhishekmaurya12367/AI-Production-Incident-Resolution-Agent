# Runbook: Payment Service Failures

**Alert**: `Payment API - 500 Internal Server Error`

## Symptoms
- `app.log` shows `ERROR Database connection failed` followed by `ERROR Payment request failed`.
- Users report inability to complete checkout.

## Mitigation Steps
1. **Verify Database Status**: Check if the PostgreSQL database is online and accepting connections.
2. **Check Connection Pool**: Restart the Node.js application to flush stale connection pools.
   ```bash
   # Restart the app
   npm start
   ```
3. **Escalate**: If the database is completely down, page the DBA team.
