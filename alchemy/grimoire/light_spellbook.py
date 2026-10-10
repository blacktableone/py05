def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_ingredients

    result = validate_ingredients(ingredients)
    if "VALID" in result and "INVALID" not in result:
        return f"Spell recorded: {spell_name} ({ingredients} - VALID)"
    return f"Spell rejected: {spell_name} ({ingredients} - INVALID)"