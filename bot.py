import os
import random
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "10000"))

# --- Render Port Binding Web Server ---
async def handle_web(request):
    return web.Response(text="Bot is running and alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

# --- 1. MALAYALAM RESPONSES ---
malayalam_plan_responses = [
    (
        "❤️ **AVAILABLE PLANS** ❤️\n\n"
        "**Malayalam Plan 👇**\n"
        "• 10Rs - 1 Day\n"
        "• 40Rs - 1 Week\n"
        "• 89Rs - 1 Month\n\n"
        "🎁 **PREMIUM FEATURES** 🎁\n"
        "○ No need to verify\n"
        "○ No need to open link\n"
        "○ Direct files\n\n"
        "🔵 **GPay UPI ID:** `kv048471@okicici`\n"
        "🟣 **PhonePe UPI ID:** `vijayalakshmik8825@ybl`\n\n"
        "⚠️ പെയ്മെന്റ് അയച്ചതിനു ശേഷം ദയവായി അതിന്റെ **സ്ക്രീൻഷോട്ട്** ഇവിടെ അയക്കുക."
    ),
    (
        "ഹലോ! മലയാളം പ്ലാനിന്റെ വിവരങ്ങൾ ഇതാ:\n\n"
        "• **10Rs** - 1 Day\n"
        "• **40Rs** - 1 Week\n"
        "• **89Rs** - 1 Month\n\n"
        "✨ **Benefits:** No need to verify, No need to open link, Direct files!\n\n"
        "🔹 **GPay:** `kv048471@okicici`\n"
        "🔹 **PhonePe:** `vijayalakshmik8825@ybl`\n\n"
        "പെയ്മെന്റ് കംപ്ീറ്റ് ചെയ്ത ഉടൻ **സ്ക്രീൻഷോട്ട്** അയക്കാൻ മറക്കരുത്."
    )
]

malayalam_hi = [
    "ഹലോ {name}! പ്ലാനുകളെക്കുറിച്ചോ പെയ്മെന്റിനെക്കുറിച്ചോ അറിയാൻ ഉണ്ടെങ്കിൽ ചോദിക്കൂ.",
    "ഹായ് {name}! എന്താ വിശേഷം? മലയാളം പ്ലാൻ വിവരങ്ങൾ വേണമെന്നുണ്ടെങ്കിൽ പറയാം."
]

# --- 2. ENGLISH RESPONSES (Default) ---
english_plan_responses = [
    (
        "❤️ **AVAILABLE PLANS** ❤️\n\n"
        "**Malayalam Plan 👇**\n"
        "• 10Rs - 1 Day\n"
        "• 40Rs - 1 Week\n"
        "• 89Rs - 1 Month\n\n"
        "🎁 **PREMIUM FEATURES** 🎁\n"
        "○ No need to verify\n"
        "○ No need to open link\n"
        "○ Direct files\n\n"
        "🔵 **GPay UPI ID:** `kv048471@okicici`\n"
        "🟣 **PhonePe UPI ID:** `vijayalakshmik8825@ybl`\n\n"
        "⚠️ Please send the **screenshot** here after completing the payment."
    )
]

english_hi = [
    "Hi {name}! If you want to know about our plans or payment details, just let me know.",
    "Hello {name}! How can I help you today?"
]

# --- 3. HINDI RESPONSES ---
hindi_responses = [
    "नमस्ते {name}! यदि आप प्लान या पेमेंट के बारे में जानना चाहते हैं, तो कृपया बताएं。\n\n🔵 **GPay UPI:** `kv048471@okicici`\n🟣 **PhonePe UPI:** `vijayalakshmik8825@ybl`\n\n⚠️ पेमेंट करने के बाद स्क्रीनशॉट यहाँ भेजें।"
]

# --- 4. TELUGU RESPONSES ---
telugu_responses = [
    "హలో {name}! ప్లాన్స్ లేదా పేమెంట్ వివరాల గురించి తెలుసుకోవాలంటే అడగండి。\n\n🔵 **GPay UPI:** `kv048471@okicici`\n🟣 **PhonePe UPI:** `vijayalakshmik8825@ybl`\n\n⚠️ పేమెంట్ చేసిన తర్వాత స్క్రీన్ షాట్ ఇక్కడ పంపండి."
]

# --- 5. TAMIL RESPONSES ---
tamil_responses = [
    "வணக்கம் {name}! பிளான் அல்லது பேமெண்ட் விவரங்கள் பற்றி அறிய விரும்பினால் கேட்கவும்.\n\n🔵 **GPay UPI:** `kv048471@okicici`\n🟣 **PhonePe UPI:** `vijayalakshmik8825@ybl`\n\n⚠️ பேமெண்ட் செய்த பிறகு ஸ்கிரீன்ஷாட்டை இங்கே அனுப்பவும்."
]

# --- 6. PAYMENT SCREENSHOT RESPONSES ---
payment_checking_responses = [
    "⏳ **Payment checking...** സ്ക്രീൻഷോട്ട് കിട്ടിയിട്ടുണ്ട്! പെയ്മെന്റ് ചെക്ക് ചെയ്ത് ഉടൻ പ്രീമിയം ആഡ് ചെയ്തുതരുന്നതാണ്.",
    "⏳ **Payment checking...** Got your screenshot! Verifying your payment, premium will be added soon."
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_name = "Friend"
    if update.message.from_user and update.message.from_user.first_name:
        user_name = update.message.from_user.first_name

    # If user sends a screenshot (Photo)
    if update.message.photo:
        reply_text = random.choice(payment_checking_responses)
        await update.message.reply_text(reply_text, parse_mode="Markdown")
        return

    if not update.message.text:
        return

    user_message = update.message.text.lower()
    print(f"Received message from {user_name} ({user_message})")

    # Language Detection & Matching Logic
    if any(word in user_message for word in ['malayalam', 'പ്ലാൻ', 'എങ്ങനെ', 'വില', 'അയച്ചു', 'രൂപ', 'rs', '10', '40', '89']) or \
       any(char >= '\u0d00' and char <= '\u0d7f' for char in user_message):
        
        if user_message in ['hi', 'hello', 'hey', 'hai']:
            reply_text = random.choice(malayalam_hi).format(name=user_name)
        else:
            reply_text = random.choice(malayalam_plan_responses)

    elif any(word in user_message for word in ['hindi', 'kaise', 'kya', 'price', 'payment', 'नमस्ते']) or \
         any(char >= '\u0900' and char <= '\u097f' for char in user_message):
        reply_text = random.choice(hindi_responses).format(name=user_name)

    elif any(word in user_message for word in ['telugu', 'ela', 'enti', 'namaskaram']) or \
         any(char >= '\u0c00' and char <= '\u0c7f' for char in user_message):
        reply_text = random.choice(telugu_responses).format(name=user_name)

    elif any(word in user_message for word in ['tamil', 'epdi', 'vanakkam', 'enna']) or \
         any(char >= '\u0b00' and char <= '\u0b7f' for char in user_message):
        reply_text = random.choice(tamil_responses).format(name=user_name)

    else:
        if user_message in ['hi', 'hello', 'hey', 'hai', 'start']:
            reply_text = random.choice(english_hi).format(name=user_name)
        elif 'gpay' in user_message or 'google pay' in user_message or 'kv048471' in user_message:
            reply_text = "✨ **GPay / Google Pay UPI ID** 👇\n\n`kv048471@okicici`\n\n⚠️ Please send the screenshot after payment."
        elif 'phonepe' in user_message or 'phone pe' in user_message or 'vijayalakshmi' in user_message:
            reply_text = "✨ **PhonePe UPI ID** 👇\n\n`vijayalakshmik8825@ybl`\n\n⚠️ Please send the screenshot after payment."
        else:
            reply_text = random.choice(english_plan_responses)

    await update.message.reply_text(reply_text, parse_mode="Markdown")

def main():
    import asyncio
    loop = asyncio.get_event_loop()
    
    # Start Render Web Server and Telegram Bot together smoothly
    loop.run_until_complete(start_web_server())

    application = ApplicationBuilder().token(TOKEN).build()
    message_handler = MessageHandler((filters.TEXT | filters.PHOTO) & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    print("Port-bound Multilingual Bot is running successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
