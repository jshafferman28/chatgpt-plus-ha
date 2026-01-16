"""The ChatGPT Plus HA integration."""

from __future__ import annotations

import logging
from pathlib import Path

import voluptuous as vol
from homeassistant.components.frontend import async_register_built_in_panel
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .agent import ChatGPTPlusAgent
from .const import CONF_SIDECAR_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)

# Config schema - this integration only supports config entries
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

# Service schemas
SERVICE_SEND_MESSAGE = "send_message"
SERVICE_NEW_CONVERSATION = "new_conversation"

SEND_MESSAGE_SCHEMA = vol.Schema(
    {
        vol.Required("message"): cv.string,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ChatGPT Plus HA component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ChatGPT Plus HA from a config entry."""
    sidecar_url = entry.data[CONF_SIDECAR_URL]

    # Create agent
    agent = ChatGPTPlusAgent(hass, sidecar_url)

    # Store agent
    hass.data[DOMAIN][entry.entry_id] = {
        "agent": agent,
        "sidecar_url": sidecar_url,
    }

    # Register frontend panel
    await _async_register_panel(hass)

    # Register services
    await _async_register_services(hass)

    _LOGGER.info("ChatGPT Plus HA integration set up successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return True


async def _async_register_panel(hass: HomeAssistant) -> None:
    """Register the frontend panel."""
    frontend_path = Path(__file__).parent / "frontend"

    # Register static path for frontend files
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                f"/chatgpt_plus_ha/frontend",
                str(frontend_path),
                cache_headers=False,
            )
        ]
    )

    # Register panel
    async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="ChatGPT",
        sidebar_icon="mdi:robot",
        frontend_url_path="chatgpt-plus",
        config={
            "_panel_custom": {
                "name": "chatgpt-plus-panel",
                "module_url": "/chatgpt_plus_ha/frontend/chat-panel.js",
            }
        },
        require_admin=False,
    )


async def _async_register_services(hass: HomeAssistant) -> None:
    """Register integration services."""

    async def handle_send_message(call: ServiceCall) -> dict:
        """Handle the send_message service call."""
        message = call.data["message"]

        # Get the first available agent
        for entry_data in hass.data[DOMAIN].values():
            if "agent" in entry_data:
                agent: ChatGPTPlusAgent = entry_data["agent"]
                result = await agent.send_message(message)
                
                # Fire an event with the response
                hass.bus.async_fire(
                    f"{DOMAIN}_response",
                    {
                        "message": message,
                        "response": result.get("message", ""),
                        "success": result.get("success", False),
                        "conversation_id": result.get("conversationId"),
                    },
                )
                return result

        _LOGGER.error("No ChatGPT Plus HA agent available")
        return {"success": False, "error": "No agent available"}

    async def handle_new_conversation(call: ServiceCall) -> dict:
        """Handle the new_conversation service call."""
        for entry_data in hass.data[DOMAIN].values():
            if "agent" in entry_data:
                agent: ChatGPTPlusAgent = entry_data["agent"]
                return await agent.new_conversation()

        _LOGGER.error("No ChatGPT Plus HA agent available")
        return {"success": False, "error": "No agent available"}

    # Register services if not already registered
    if not hass.services.has_service(DOMAIN, SERVICE_SEND_MESSAGE):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SEND_MESSAGE,
            handle_send_message,
            schema=SEND_MESSAGE_SCHEMA,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_NEW_CONVERSATION):
        hass.services.async_register(
            DOMAIN,
            SERVICE_NEW_CONVERSATION,
            handle_new_conversation,
        )
