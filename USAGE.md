# WhatsApp-OSINT — Usage Instructions

## Prerequisites

- Python 3.8+
- A RapidAPI account with an active subscription to the [WhatsApp OSINT API](https://rapidapi.com/inutil-inutil-default/api/whatsapp-osint)

## Setup

### 1. Create and activate the virtual environment

```bash
cd WhatsApp-OSINT
python3 -m venv myvenv
source myvenv/bin/activate
```

### 2. Install dependencies

```bash
pip3 install -r requirements.txt
```

This installs: `requests`, `python-dotenv`, `colorama`.

### 3. Configure your API key

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder with your RapidAPI key:

```
RAPIDAPI_KEY=your_actual_api_key_here
```

> **Important:** Never commit `.env` to version control. It is excluded via `.gitignore`.

## Running the Tool

```bash
source myvenv/bin/activate   # if not already activated
python3 whatsapp-osint.py
```

### Menu Options

1. **Profile Photo** — Downloads the target's WhatsApp profile picture as a JPG file.
2. **User Status** — Retrieves the "about" text, online/offline status, and last seen time.
3. **Business Verification** — Checks whether the number is a WhatsApp Business account.
4. **Device Information** — Shows linked devices (count, type, OS).
5. **Full OSINT Information** — Combined data dump from the `/wspic/dck` endpoint.
6. **Privacy Settings** — Reports visibility of profile photo, read receipts, last seen, and status.

### Phone Number Format

Enter numbers **with country code** and **without the `+` sign**.

Examples:
- US: `14155552671`
- Peru: `51916574069`
- UK: `447911123456`

## Troubleshooting

- **403 "You are not subscribed to this API"** — Your RapidAPI key is missing or doesn't have an active subscription. Visit the [pricing page](https://rapidapi.com/inutil-inutil-default/api/whatsapp-osint/pricing) to subscribe.
- **`RAPIDAPI_KEY not found in .env`** — Make sure `.env` exists in the project root and contains your key.
- **`ModuleNotFoundError`** — Ensure the virtual environment is activated (`source myvenv/bin/activate`) and dependencies are installed.
- **API under maintenance** — The RapidAPI endpoint may occasionally be down. Retry later.
