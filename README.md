# Automated News Email (China + UK/US)

This repo sends a twice-daily analysis-style email brief with 6–8 items, balanced 1:1 between China and UK/US topics (finance, tech, international politics).

## One-click deployment (GitHub Actions)

1. Push this repo to GitHub.
2. Go to **Settings → Secrets and variables → Actions → New repository secret**.
3. Add:
   - `SMTP_HOST` = `smtp.qq.com`
   - `SMTP_PORT` = `465`
   - `SMTP_USER` = your sender mailbox
   - `SMTP_PASS` = SMTP authorization code
   - `TO_EMAIL` = destination mailbox
4. Open **Actions → News Mailer → Run workflow** to send a test immediately.

## Schedule

- 08:00 Beijing time (`cron: 0 0 * * *` UTC)
- 20:00 Beijing time (`cron: 0 12 * * *` UTC)

## Local test

```bash
SMTP_HOST=smtp.qq.com \
SMTP_PORT=465 \
SMTP_USER=your_sender@qq.com \
SMTP_PASS=your_smtp_auth_code \
TO_EMAIL=target@qq.com \
python news_mailer.py
```
