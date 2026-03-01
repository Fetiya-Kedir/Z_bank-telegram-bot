from __future__ import annotations

from typing import Dict

TEXTS: Dict[str, Dict[str, str]] = {
    "en": {
        "WELCOME": "Welcome. Please choose your language:",
        "LANG_SAVED": "Language set to English.",
        "MAIN_MENU": "Main menu:",
        "BTN_FAQ": "📌 FAQs",
        "BTN_BRANCH": "🏦 Find Branch",
        "BTN_SUPPORT": "☎ Contact Support",
        "BTN_ABOUT": "ℹ About",
        "UNKNOWN": "Sorry, I didn't understand that. Use /start to begin.",
    },
    "am": {
        "WELCOME": "እንኳን ደህና መጡ። ቋንቋ ይምረጡ፦",
        "LANG_SAVED": "ቋንቋው ወደ አማርኛ ተቀይሯል።",
        "MAIN_MENU": "ዋና ምናሌ፦",
        "BTN_FAQ": "📌 መረጃ (FAQ)",
        "BTN_BRANCH": "🏦 ቅርንጫፍ ፈልግ",
        "BTN_SUPPORT": "☎ ድጋፍ አግኝ",
        "BTN_ABOUT": "ℹ ስለ ባንኩ",
        "UNKNOWN": "ይቅርታ፣ አልገባኝም። /start ብለው ይጀምሩ።",
    },
    "om": {
        "WELCOME": "Baga nagaan dhuftan. Afaan filadhaa:",
        "LANG_SAVED": "Afaaniin Afaan Oromootti jijjiirameera.",
        "MAIN_MENU": "Baafata mootummaa:",
        "BTN_FAQ": "📌 Gaaffii fi Deebii (FAQ)",
        "BTN_BRANCH": "🏦 Damee barbaadi",
        "BTN_SUPPORT": "☎ Deeggarsa argadhu",
        "BTN_ABOUT": "ℹ Waa'ee baankii",
        "UNKNOWN": "Dhiifama, hin hubanne. /start jedhuun jalqabi.",
    },
}


def t(lang: str, key: str) -> str:
    lang = lang if lang in TEXTS else "en"
    return TEXTS[lang].get(key, TEXTS["en"].get(key, key))