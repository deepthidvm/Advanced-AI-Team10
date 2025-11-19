import gradio as gr
from groq import Groq
import traceback

# -----------------------------------------------------------------------
# 🔑 PUT YOUR GROQ API KEY HERE
# -----------------------------------------------------------------------
API_KEY = ""

client = Groq(api_key=API_KEY)

# -----------------------------------------------------------------------
#  SYSTEM PROMPT — WOMEN'S HEALTH & WELLNESS CHATBOT
# -----------------------------------------------------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a warm, supportive Women's Health & Wellness assistant. "
        "You provide general guidance about menstrual health, PCOS awareness, "
        "nutrition, emotional well-being, stress-relief, women's fitness, "
        "self-care, and hygiene. "
        "You do NOT give medical diagnoses or prescriptions. "
        "You always recommend consulting a doctor for medical concerns."
    )
}

# -----------------------------------------------------------------------
# CHATBOT FUNCTION
# -----------------------------------------------------------------------
def customLLMBot(user_input, history):
    print("FUNCTION CALLED:", repr(user_input))

    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": user_input}
    ]

    try:
        print("Sending request to Groq...")
        resp = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        print("RAW RESPONSE:", resp)

        reply = resp.choices[0].message.content
        print("LLM reply:", reply)

        return reply

    except Exception:
        print("ERROR calling Groq API:")
        traceback.print_exc()
        return "Sorry, I couldn't get a response. Check your API key or internet."

# -----------------------------------------------------------------------
# 🎀 GRADIO CHAT UI
# -----------------------------------------------------------------------
iface = gr.ChatInterface(
    fn=customLLMBot,
    chatbot=gr.Chatbot(type="messages", height=350),
    textbox=gr.Textbox(placeholder="Ask anything about women's health & wellness"),
    title="🌸 Women’s Health & Wellness Assistant",
    description="A warm and caring chatbot for menstrual wellness, PCOS, nutrition, emotions, and women's fitness.",
    examples=[
        "How to reduce period cramps?",
        "What are PCOS symptoms?",
        "Give me a healthy diet for women",
        "How to handle stress?"
    ],
    type="messages",
)

if __name__ == "__main__":
    print("Launching Women's Health & Wellness Chatbot...")
    iface.launch(share=True)
