import json
import os
import base64
import requests
from crewai.tools import BaseTool
from PIL import Image
from openai import OpenAI
from io import BytesIO
from typing import List, Optional
import logging
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO)

logging.info("Extracting ingredients from image...")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ExtractIngredientsTool(BaseTool):
    name: str = "Extract Ingredients"
    description: str = "Extracts ingredients from a food item image."
    
    def _run(self, image_input: str):
        """
        Extract ingredients from a food item image.
        
        :param image_input: The image file path (local) or URL (remote).
        :return: A list of ingredients extracted from the image.
        """
        if image_input.startswith("http"):  # Check if input is a URL
            # Download the image from the URL
            response = requests.get(image_input)
            response.raise_for_status()
            image_bytes = BytesIO(response.content)
        else:
            # Open the local image file in binary mode
            if not os.path.isfile(image_input):
                raise FileNotFoundError(f"No file found at path: {image_input}")
            with open(image_input, "rb") as file:
                image_bytes = BytesIO(file.read())

        # Encode the image to a base64 string
        encoded_image = base64.b64encode(image_bytes.read()).decode("utf-8")

        # Call the model with the encoded image
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract ingredients from the food item image"},
                        {"type": "image_url", "url": f"data:image/jpeg;base64,{encoded_image}"}
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content


class FilterIngredientsTool(BaseTool):
    name: str = "Filter Ingredients"
    description: str = "Filters out non-food items or noise from raw ingredient data."
    
    def _run(self, raw_ingredients: str) -> List[str]:
        """
        Processes the raw ingredient data and filters out non-food items or noise.
        
        :param raw_ingredients: Raw ingredients as a string.
        :return: A list of cleaned and relevant ingredients.
        """
        # Example implementation: parse the raw ingredients string into a list
        # This can be enhanced with more sophisticated parsing as needed
        ingredients = [ingredient.strip().lower() for ingredient in raw_ingredients.split(',') if ingredient.strip()]
        return ingredients

class DietaryFilterTool(BaseTool):
    name: str = "Filter Based on Dietary Restrictions"
    description: str = "Filters ingredients based on dietary restrictions (e.g., vegan, gluten-free)."
    
    def _run(self, ingredients: List[str], dietary_restrictions: Optional[str] = None) -> List[str]:
        """
        Uses an LLM model to filter ingredients based on dietary restrictions.

        :param ingredients: List of ingredients.
        :param dietary_restrictions: Dietary restrictions (e.g., vegan, gluten-free). Defaults to None.
        :return: Filtered list of ingredients that comply with the dietary restrictions.
        """
        # If no dietary restrictions are provided, return the original ingredients
        if not dietary_restrictions:
            return ingredients

        # Initialize the OpenAI model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150,
        )

        # Parse the response to return the filtered list
        filtered = response.choices[0].message.content.strip().lower()
        filtered_list = [item.strip() for item in filtered.split(',') if item.strip()]
        return filtered_list

    
class NutrientAnalysisTool(BaseTool):
    name: str = "Analyze Nutritional Values and Calories"
    description: str = "Provides a detailed nutrient breakdown and estimates total calories from an uploaded image."
    
    def _run(self, image_input: str):
        """
        Provide a detailed nutrient breakdown and estimate the total calories of all ingredients from the uploaded image.
        
        :param image_input: The image file path (local) or URL (remote).
        :return: A string with nutrient breakdown (protein, carbs, fat, etc.) and estimated calorie information.
        """
        if image_input.startswith("http"):  # Check if input is a URL
            # Download the image from the URL
            response = requests.get(image_input)
            response.raise_for_status()
            image_bytes = BytesIO(response.content)
        else:
            # Open the local image file in binary mode
            if not os.path.isfile(image_input):
                raise FileNotFoundError(f"No file found at path: {image_input}")
            with open(image_input, "rb") as file:
                image_bytes = BytesIO(file.read())

        # Encode the image to a base64 string
        encoded_image = base64.b64encode(image_bytes.read()).decode("utf-8")

        # Assistant prompt (can be customized)
        assistant_prompt = """
            You are an expert nutritionist. Your task is to analyze the food items displayed in the image and provide a detailed nutritional assessment using the following format:
        1. **Identification**: List each identified food item clearly, one per line.
        2. **Portion Size & Calorie Estimation**: For each identified food item, specify the portion size and provide an estimated number of calories. Use bullet points with the following structure:
        - **[Food Item]**: [Portion Size], [Number of Calories] calories
        Example:
        *   **Salmon**: 6 ounces, 210 calories
        *   **Asparagus**: 3 spears, 25 calories
        3. **Total Calories**: Provide the total number of calories for all food items.
        Example:
        Total Calories: [Number of Calories]
        4. **Nutrient Breakdown**: Include a breakdown of key nutrients such as **Protein**, **Carbohydrates**, **Fats**, **Vitamins**, and **Minerals**. Use bullet points, and for each nutrient provide details about the contribution of each food item.
        Example:
        *   **Protein**: Salmon (35g), Asparagus (3g), Tomatoes (1g) = [Total Protein]
        5. **Health Evaluation**: Evaluate the healthiness of the meal in one paragraph.
        6. **Disclaimer**: Include the following exact text as a disclaimer:
        The nutritional information and calorie estimates provided are approximate and are based on general food data. 
        Actual values may vary depending on factors such as portion size, specific ingredients, preparation methods, and individual variations. 
        For precise dietary advice or medical guidance, consult a qualified nutritionist or healthcare provider.
        Format your response exactly like the template above to ensure consistency.
        """

        # Call the model with the encoded image
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": assistant_prompt},
                        {"type": "image_url", "url": f"data:image/jpeg;base64,{encoded_image}"}
                    ],
                }
            ],
            max_tokens=500,
        )

        return response.choices[0].message.content
