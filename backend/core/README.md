### Middleware

A custom `RequestAuditMiddleware` is implemented to enforce global authentication
rules and log request metadata. Public endpoints such as user registration,
authentication, and job listings are explicitly allow-listed, while all other API
endpoints require authentication. The middleware also measures request execution
time and logs method, path, status code, and user identity.
