# ChatGPT Plus HA

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add--on-blue.svg)](https://www.home-assistant.io/)

A Home Assistant Add-on & Integration that lets you chat with ChatGPT using your **ChatGPT Plus subscription** - no OpenAI API key required!

## Features
- 🚀 **Easy Installation**: Install via Home Assistant Add-on Store
- 💬 **Chat Interface**: Beautiful chat panel in sidebar
- 🔄 **Conversation Memory**: Maintains context
- 🏠 **Services**: Use ChatGPT in automations
- 🔒 **Persistent Session**: Login once, stays logged in

## Installation

### Step 1: Install the Add-on (Backend)

1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Click the three dots (top right) → **Repositories**
3. Add this URL: `https://github.com/jshafferman28/chatgpt-plus-ha`
4. Click **Add**
5. Find **"ChatGPT Plus HA"** in the list and install it
6. **Start** the add-on (enable "Start on boot" and "Watchdog")

### Step 2: First-Time Login

1. Go to the **Configuration** tab of the Add-on
2. Set `headless: false`
3. Save and Restart the Add-on
4. Click **Open Web UI** (or look for the sidebar link)
5. Log into ChatGPT manually
6. Once logged in, go back to Configuration
7. Set `headless: true`
8. Save and Restart

*Your session is now saved in the `/config/chatgpt_sessions` directory.*

### Step 3: Install the Integration (Frontend)

1. Open **HACS**
2. Add Custom Repository: `https://github.com/jshafferman28/chatgpt-plus-ha` (Category: Integration)
3. Install **"ChatGPT Plus HA"**
4. Restart Home Assistant
5. Go to **Settings** → **Devices & Services** → **Add Integration**
6. Search for "ChatGPT Plus HA"
7. The URL should automatically be `http://chatgpt_plus_ha:3000` (internal host)
8. Submit

## Usage

Click "ChatGPT" in your sidebar to start chatting!

### Services
- `chatgpt_plus_ha.send_message`
- `chatgpt_plus_ha.new_conversation`

## Troubleshooting
Check the Add-on logs for any browser errors. If login fails, try repeating Step 2.
