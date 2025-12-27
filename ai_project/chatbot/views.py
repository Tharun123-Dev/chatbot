import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from google import genai

# Create Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse({"reply": "Please type a message."})

        # ✅ USE FULL MODEL NAME EXACTLY AS LISTED
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=message
        )

        return JsonResponse({"reply": response.text})

    except Exception as e:
        print("REAL ERROR:", e)
        return JsonResponse({"error": str(e)}, status=500)
