# Ergo

Automated ergonomic break reminder. Fires an OS notification every hour during working hours. Clicking the notification opens a guided exercise page in your browser.

---

## Requirements

- Python 3.8+
- `pip install schedule plyer`

---

## Quick start (Windows)

### 1. Install dependencies

```
pip install schedule plyer
```

### 2. Edit the config

Open `ergo-config.json` and adjust to your preferences:

```json
{
  "break_interval_minutes": 60,
  "break_duration_seconds": 30,
  "start_hour": 9,
  "end_hour": 18,
  "exercise_page_url": "https://<your-azure-static-web-app-url>"
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `break_interval_minutes` | `60` | How often to remind (30–90 recommended) |
| `break_duration_seconds` | `30` | Timer shown on each exercise card |
| `start_hour` | `9` | First reminder no earlier than this hour (24h) |
| `end_hour` | `18` | No reminders at or after this hour (24h) |
| `exercise_page_url` | _(blank)_ | URL of the hosted exercise page |

### 3. Test it manually

Set `break_interval_minutes` to `1`, then run:

```
python ergo.py
```

A notification should appear within ~1 minute. Click it — the exercise page opens in your browser. Revert the interval to `60` when done.

### 4. Set up autostart (runs at Windows login)

**a.** Open `ergo-autostart.xml` and update the two paths:

```xml
<Command>pythonw.exe</Command>           <!-- or full path: C:\Python312\pythonw.exe -->
<WorkingDirectory>C:\path\to\Ergo</WorkingDirectory>
```

To find your `pythonw.exe` path:
```
where pythonw
```

**b.** Import the task:
```
schtasks /create /xml ergo-autostart.xml /tn "Ergo Break Reminder"
```

**c.** Verify it's registered:
```
schtasks /query /tn "Ergo Break Reminder"
```

**d.** Reboot and confirm `ergo.py` is running (check Task Manager → Details for `pythonw.exe`).

### 5. Remove autostart (if needed)

```
schtasks /delete /tn "Ergo Break Reminder" /f
```

---

## Exercise web page

The `web/` folder contains the exercise page. Deploy it to Azure Static Web Apps (free tier):

1. Push this repo to GitHub.
2. In the Azure portal, create a **Static Web App** linked to your repo.
3. Set the **App location** to `web` and **Output location** to blank.
4. Copy the generated URL into `ergo-config.json` → `exercise_page_url`.

Any push to `main` will auto-redeploy the page.

### Adding GIFs

Drop `.gif` files into `web/gifs/` and update `web/exercises.json` to reference them. Each GIF should be under 500 KB. To compress:

```
ffmpeg -i input.gif -vf "scale=400:-1" web/gifs/output.gif
```

The page falls back to emoji placeholders if a GIF is missing, so exercises work without them.

---

## macOS setup

### 1. Install Python 3

Check if Python 3 is already installed:

```bash
python3 --version
```

If not, install via Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

### 2. Install dependencies

```bash
pip3 install schedule plyer
```

### 3. Edit the config

Open `ergo-config.json` and set your preferences — same fields as Windows. Make sure `exercise_page_url` points to your Azure Static Web App URL.

### 4. Test it manually

Set `break_interval_minutes` to `1`, then run:

```bash
cd /path/to/Ergo
python3 ergo.py
```

A notification should appear within ~1 minute and open the exercise page in your browser. Revert the interval to `60` when done.

> **Note:** macOS may ask you to allow notifications for Terminal (or your Python app) the first time. Go to **System Settings → Notifications** and enable them.

### 5. Set up autostart (runs at Mac login)

**a.** Edit `com.ergo.plist` — update the two `YOURUSERNAME/path/to/Ergo` placeholders with your real paths:

```bash
# Find your python3 path:
which python3

# Find your Ergo folder path:
pwd   # run this from inside the Ergo folder
```

**b.** Copy the plist to LaunchAgents:

```bash
cp /path/to/Ergo/com.ergo.plist ~/Library/LaunchAgents/
```

**c.** Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.ergo.plist
```

**d.** Verify it's running:

```bash
launchctl list | grep com.ergo
```

You should see `com.ergo` listed with a PID (if running) or `0` (loaded, waiting for next trigger).

**e.** Check logs if something seems wrong:

```bash
cat /tmp/ergo.log        # stdout — normal output
cat /tmp/ergo-error.log  # stderr — errors
```

### 6. Remove autostart (if needed)

```bash
launchctl unload ~/Library/LaunchAgents/com.ergo.plist
rm ~/Library/LaunchAgents/com.ergo.plist
```

---

## File structure

```
Ergo/
├── ergo.py                 # Main scheduler script
├── ergo-config.json        # Your config (edit this)
├── ergo-autostart.xml      # Windows autostart (Task Scheduler)
├── com.ergo.plist          # macOS autostart (launchd)
├── README.md
├── docs/                   # Architecture docs and ADRs
└── web/
    ├── index.html          # Exercise page
    ├── exercises.json      # Exercise library (10 exercises)
    └── gifs/               # Animated GIFs (add your own)
```
