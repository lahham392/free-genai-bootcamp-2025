TOPICS = {
    "Food & Dining": ["restaurants", "cooking", "meals", "ingredients"],
    "Travel": ["transportation", "locations", "accommodation", "tourism"],
    "Family & Friends": ["relationships", "activities", "celebrations"],
    "Daily Activities": ["routines", "hobbies", "work", "school"],
    "Nature & Environment": ["weather", "animals", "plants", "conservation"]
}

DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

# Fallback sentences in case AWS Bedrock is unavailable
FALLBACK_SENTENCES = {
    "Food & Dining": {
        "Beginner": ("Me gusta comer ___ para el desayuno.", "Me gusta comer huevos para el desayuno.", "huevos"),
        "Intermediate": ("El chef preparó una ___ deliciosa.", "El chef preparó una sopa deliciosa.", "sopa"),
        "Advanced": ("La receta tradicional requiere ___ frescos de la región.", "La receta tradicional requiere ingredientes frescos de la región.", "ingredientes")
    },
    # Add more fallback sentences for other topics...
}
