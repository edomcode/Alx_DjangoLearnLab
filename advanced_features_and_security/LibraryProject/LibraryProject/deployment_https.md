HTTPS & Secure Redirect Configuration
Django Security Settings
The following settings were added to 'settings.py':

SECURE_SSL_REDIRECT
SECURE_HSTS_*
SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE
X_FRAME_OPTIONS
SECURE_CONTENT_TYPE_NOSNIFF
SECURE_BROWSER_XSS_FILTER
Web Server Configuration
To serve over HTTPS, an Nginx server was configured with SSL certificates.

Security Review
All cookies are now HTTPS-only
XSS, clickjacking, and MIME sniffing mitigated
All HTTP traffic redirects to HTTPS