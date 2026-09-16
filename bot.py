import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

# 1. വെറുതെ Hi, Hello എന്ന് ആരെങ്കിലും അയക്കുമ്പോൾ ഫ്രണ്ട്ലി ആയി മറുപടി നൽകാൻ (മാറിമാറി വരും)
hi_hello_responses = [
    "Hi bro! പ്ലാനുകളെക്കുറിച്ചോ പേയ്മെന്റിനെക്കുറിച്ചോ അറിയാൻ ഉണ്ടെങ്കിൽ ചോദിക്കൂ.",
    "Hello! എന്താ വിശേഷം? മലയാളം പ്ലാൻ വിവരങ്ങൾ വേണമെന്നുണ്ടെങ്കിൽ പറയാം.",
    "Hey there! സുഖമാണോ? പ്ലാൻ ഡീറ്റെയിൽസ് നോക്കാൻ പറയൂ.",
    "Hi sister! എന്താണ് സഹായം വേണ്ടത്? പ്ലാൻസ് നോക്കുന്നുണ്ടോ?",
    "Hello bro! പ്ലാൻ ഡീറ്റെയിൽസും യുപിഐ ഐഡിയും താഴെ കൊടുക്കാം, വേണമെന്നുണ്ടെങ്കിൽ ചോദിക്കൂ."
]

# 2. മലയാളം പ്ലാനുകൾ ചോദിക്കുമ്പോൾ (മാറിമാറി വരുന്ന ശൈലി)
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
        "ഹലോ bro! മലയാളം പ്ലാനിന്റെ വിവരങ്ങൾ ഇതാ:\n\n"
        "• **10Rs** - 1 Day\n"
        "• **40Rs** - 1 Week\n"
        "• **89Rs** - 1 Month\n\n"
        "✨ **Benefits:** No need to verify, No need to open link, Direct files!\n\n"
        "🔹 **GPay:** `kv048471@okicici`\n"
        "🔹 **PhonePe:** `vijayalakshmik8825@ybl`\n\n"
        "പെയ്മെന്റ് കംപ്ീറ്റ് ചെയ്ത ഉടൻ **സ്ക്രീൻഷോട്ട്** അയക്കാൻ മറക്കരുത്."
    )
]

# 3. Google Pay മാത്രം ചോദിക്കുമ്പോൾ
gpay_responses = [
    "✨ **GPay / Google Pay UPI ID** 👇\n\n`kv048471@okicici`\n\n⚠️ പെയ്മെന്റ് ചെയ്ത ശേഷം സ്ക്രീൻഷോട്ട് അയക്കുക.",
    "ഗൂഗിൾ പേ വഴി ചെയ്യാനാണെങ്കിൽ ഈ യുപിഐ ഐഡി ഉപയോഗിക്കൂ bro 👇\n\n`kv048471@okicici`\n\nപെയ്മെന്റ് കഴിഞ്ഞാൽ സ്ക്രീൻഷോട്ട് ഇവിടെ സെൻഡ് ചെയ്യുക."
]

# 4. PhonePe മാത്രം ചോദിക്കുമ്പോൾ
phonepe_responses = [
    "✨ **PhonePe UPI ID** 👇\n\n`vijayalakshmik8825@ybl`\n\n⚠️ പെയ്മെന്റ് അയച്ച ശേഷം സ്ക്രീൻഷോട്ട് അയക്കുക.",
    "ഫോൺ പേ വഴിയാണ് ചെയ്യുന്നതെങ്കിൽ ഈ യുപിഐ ഐഡിയിലേക്ക് അയക്കൂ 👇\n\n`vijayalakshmik8825@ybl`\n\nപെയ്മെന്റ് സ്ക്രീൻഷോട്ട് ഉടൻ അയക്കുമല്ലോ."
]

# 5. മറ്റ് ഭാഷകളിൽ ചോദിക്കുമ്പോൾ
other_language_responses = [
    "Hello! For this language plan, please wait until the owner comes online. They will talk to you directly soon.",
    "Hi there! Regarding this language, the owner is currently offline. They will reply to you once they are online.",
    "Hey! For languages other than Malayalam, please wait for the owner to come online. They'll assist you shortly."
]

# 6. പെയ്മെന്റ് സ്ക്രീൻഷോട്ട് (ഫോട്ടോ) അയക്കുമ്പോൾ
payment_checking_responses = [
    "⏳ **Payment checking...** സ്ക്രീൻഷോട്ട് കിട്ടിയിട്ടുണ്ട്! പെയ്മെന്റ് ചെക്ക് ചെയ്ത് ഉടൻ പ്രീമിയം ആഡ് ചെയ്തുതരുന്നതാണ്.",
    "Got your screenshot! 👍 പെയ്മെന്റ് ചെക്ക് ചെയ്തുകൊണ്ടിരിക്കുകയാണ്, കുറച്ചു സമയം കാത്തിരിക്കൂ.",
    "Thanks for the screenshot! Checking the payment right now... Premium will be added shortly."
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ഉപയോക്താവ് ഫോട്ടോയാണ് (സ്ക്രീൻഷോട്ട്) അയച്ചതെങ്കിൽ
    if update.message.photo:
        reply_text = random.choice(payment_checking_responses)
        await update.message.reply_text(reply_text, parse_mode="Markdown")
        return

    # ടെക്സ്റ്റ് മെസ്സേജ് ആണെങ്കിൽ
    user_message = update.message.text.lower() if update.message.text else ""
    print(f"Received message: {user_message}")
    
    # വെറുതെ Hi അല്ലെങ്കിൽ Hello എന്ന് മാത്രം അയച്ചാൽ
    if user_message in ['hi', 'hello', 'hey', 'hai', 'ഹായ്', 'ഹലോ']:
        reply_text = random.choice(hi_hello_responses)
    
    # മറ്റ് ഭാഷകൾ ചോദിച്ചാൽ
    elif any(lang in user_message for lang in ['hindi', 'tamil', 'telugu', 'kannada', 'bangla']):
        reply_text = random.choice(other_language_responses)
    
    # Google Pay മാത്രം ചോദിച്ചാൽ
    elif 'gpay' in user_message or 'google pay' in user_message or 'kv048471' in user_message:
        reply_text = random.choice(gpay_responses)
        
    # PhonePe മാത്രം ചോദിച്ചാൽ
    elif 'phonepe' in user_message or 'phone pe' in user_message or 'vijayalakshmi' in user_message:
        reply_text = random.choice(phonepe_responses)
        
    # പ്ലാനുകളെക്കുറിച്ചോ മലയാളം സംബന്ധിച്ചോ ചോദിച്ചാൽ
    elif any(word in user_message for word in ['plan', 'malayalam', 'price', 'details', '10', '40', '89', 'Rs', 'പ്ലാൻ']):
        reply_text = random.choice(malayalam_plan_responses)
        
    # മറ്റെന്തെങ്കിലും സാധാരണ മെസ്സേജുകൾ ആണെങ്കിൽ
    else:
        reply_text = random.choice(malayalam_plan_responses)

    await update.message.reply_text(reply_text, parse_mode="Markdown")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    message_handler = MessageHandler((filters.TEXT | filters.PHOTO) & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    print("Smart Friendly Bot is running on Render...")
    application.run_polling()

if __name__ == '__main__':
    main()
