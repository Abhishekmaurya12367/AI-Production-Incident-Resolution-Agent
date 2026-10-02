# General Troubleshooting

When issues arise in the Production App:

1. **Check Logs**: Review `app.log` in the application root directory for `ERROR` or `WARN` entries.
2. **Verify Services**: Ensure all simulated services (User, Payment, Order) are acknowledging requests.
3. **Check Database Connectivity**: 90% of Payment Service issues stem from database connection failures.
