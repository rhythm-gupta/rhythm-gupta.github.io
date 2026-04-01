# WhatsApp Daily Legal Digest Bot (DHJS)

A ready-to-run Python bot that:
1. Scans these legal websites daily:
   - https://www.livelaw.in/
   - https://www.barandbench.com/
   - https://www.scconline.com/blog/
   - https://www.verdictum.in/
2. Filters items for:
   - Supreme Court of India and Delhi High Court matters.
   - The specified Acts/topics list (CPC, CrPC, IPC, BNS, etc.).
3. Generates a PDF digest with:
   - Hyperlinked headline.
   - Judgment/order PDF link (or fallback legal search URL if direct PDF is unavailable).
   - Court, bench, judges.
   - Bullet-point summary.
   - Act reference footnote.
4. Sends the PDF to WhatsApp group `DHJS` daily using WhatsApp Web automation.

## Privacy and permission model

- The bot only touches WhatsApp Web for sending the generated PDF.
- Before sending, the bot asks explicit terminal consent.
- If Chrome profile reuse is configured, it asks separate consent before using it.
- If consent is denied, no WhatsApp action is taken.

## Install

```bash
cd legal_digest_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure Google Chrome + compatible ChromeDriver are available for Selenium.

## Configure

```bash
cp .env.example .env
```

Set env vars in your shell (or via your process manager):

```bash
export WHATSAPP_GROUP_NAME=DHJS
export RUN_HOUR=8
export RUN_MINUTE=0
export TIMEZONE=Asia/Kolkata
export CHROME_PROFILE_DIR=/path/to/chrome/profile   # optional
```

## Usage

Run one immediate cycle:
```bash
PYTHONPATH=. python -m legal_digest_bot.main --once
```

Run as daily scheduler:
```bash
PYTHONPATH=. python -m legal_digest_bot.main
```

Output PDF path:
- `legal_digest_bot/output/legal_digest_YYYYMMDD.pdf`

## Notes

- News websites may change HTML often; selectors are intentionally generic.
- If direct judgment/order PDFs are not present in an article, a fallback legal search link is included for quick retrieval.
- For production hardening, deploy using `systemd`/Docker and monitor logs.
