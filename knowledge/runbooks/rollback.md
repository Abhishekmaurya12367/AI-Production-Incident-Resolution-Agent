# Runbook: Deployment Rollback

If a recent deployment causes systemic failures across multiple services:

1. Identify the previous stable commit hash.
2. Trigger the rollback pipeline in CI/CD.
3. If doing it manually:
   ```bash
   git checkout <previous_stable_commit>
   npm install
   npm start
   ```
4. Monitor `app.log` for 5 minutes post-rollback to ensure error rates drop.
