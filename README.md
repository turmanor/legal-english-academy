# Automated News Email (China + UK/US)

This repo sends a twice-daily analysis-style email brief with 6–8 items, balanced 1:1 between China and UK/US topics (finance, tech, international politics).

## One-click deployment (GitHub Actions)

1. Push this repo to GitHub.
2. Go to **Settings → Secrets and variables → Actions → New repository secret**.
3. Add:
   - `SMTP_HOST` = `smtp.qq.com`
   - `SMTP_PORT` = `465`
   - `SMTP_USER` = your sender mailbox (must have SMTP enabled)
   - `SMTP_PASS` = SMTP authorization code (not mailbox login password)
   - `TO_EMAIL` = destination mailbox (e.g., `2130334277@qq.com`)
4. Open **Actions → News Mailer → Run workflow** to send a test immediately.

## Schedule

- 08:00 Beijing time (`cron: 0 0 * * *` UTC)
- 20:00 Beijing time (`cron: 0 12 * * *` UTC)

## Common failure reasons

- SMTP auth failed: usually wrong `SMTP_PASS` authorization code or SMTP not enabled.
- DNS lookup failed: runner/network cannot resolve `smtp.qq.com`.
- Secret not configured: `SMTP_USER`, `SMTP_PASS`, or `TO_EMAIL` missing.


## Troubleshooting checklist

1. In **Actions logs**, verify `Check SMTP DNS` step passes.
2. If DNS check fails, set `SMTP_HOST` explicitly to `smtp.qq.com` and retry; if still failing, it's runner/network-level DNS issue.
3. If DNS passes but send fails with auth error, regenerate QQ SMTP authorization code and update `SMTP_PASS`.

## Local test

```bash
SMTP_HOST=smtp.qq.com \
SMTP_PORT=465 \
SMTP_USER=your_sender@qq.com \
SMTP_PASS=your_smtp_auth_code \
TO_EMAIL=target@qq.com \
python news_mailer.py
```
