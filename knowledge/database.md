# Database Specifications

The system utilizes PostgreSQL as its primary relational database.

- **Type**: PostgreSQL 15
- **Purpose**: Stores user data, orders, and payment ledgers.
- **Connection**: Managed via standard pg connection pooling.

## Known Issues
- The connection pool can occasionally exhaust under high payment load, resulting in 500 Internal Server Errors in the Payment Service.
