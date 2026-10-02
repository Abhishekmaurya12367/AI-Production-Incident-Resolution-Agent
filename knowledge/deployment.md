# Deployment Guide

The application is deployed using standard CI/CD pipelines.

## Steps
1. Build the Node.js application `npm run build` (if applicable).
2. Run tests `npm test`.
3. Deploy to production servers.
4. Start the service with `npm start`.

*Logs are written to `app.log` by default in the current directory.*
