import google.generativeai as genai

genai.configure(api_key="AIzaSyAjCADin98tsYfwEoF6_FhfRtEE3hBMuXc")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)