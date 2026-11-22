"""Bilingual (English/Hindi) advice templates. General advisories only, not medical advice.
Wording must be reviewed against NCDC/NDMA guidance by faculty or a health professional."""

HEADLINE = {
    "en": ["LOW stress: normal precautions", "MODERATE stress: take care", "HIGH stress: protect yourself", "SEVERE stress: avoid heavy work"],
    "hi": ["कम तनाव: सामान्य सावधानी", "मध्यम तनाव: सावधानी रखें", "ज़्यादा तनाव: खुद को बचाएँ", "बहुत ज़्यादा तनाव: भारी काम से बचें"],
}
HEAT_TIP = {
    "en": "Drink water often, even if not thirsty. Rest in shade. Cover your head.",
    "hi": "प्यास न लगे तब भी बार-बार पानी पिएँ। छाया में आराम करें। सिर ढकें।",
}
AIR_TIP = {
    "en": "Air is poor: wear a well-fitting mask if you have one, and avoid heavy exertion near heavy traffic.",
    "hi": "हवा खराब है: मास्क हो तो ठीक से पहनें और भारी ट्रैफ़िक के पास भारी मेहनत से बचें।",
}
SEVERE_TIP = {
    "en": "If you feel dizzy, confused, faint or very unwell, stop, move to shade and seek medical help.",
    "hi": "चक्कर, उलझन, बेहोशी या बहुत बुरा लगे तो रुकें, छाया में जाएँ और डॉक्टरी मदद लें।",
}


def build_advice(result: dict, lang: str = "en") -> list:
    lines = [HEADLINE[lang][result["score"]]]
    if result["heat_level"] >= 1:
        lines.append(HEAT_TIP[lang])
    if result["air_level"] >= 2:
        lines.append(AIR_TIP[lang])
    if result["score"] >= 2:
        lines.append(SEVERE_TIP[lang])
    return lines
