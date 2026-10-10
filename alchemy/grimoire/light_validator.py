def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients

    allowed = light_spell_allowed_ingredients()
    for ingredient in allowed:
        if ingredient in ingredients.lower():
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"