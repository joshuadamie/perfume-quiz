from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

questions = [
    {
        "text": "1. Your weekend vibe is:",
        "options": ["A: Party 🕺🏾", "B: Netflix & chill 🍿", "C: Beach hangout 🌴", "D: Lunch & selfies 📸"],
        "scores": ["Oriental", "Woody", "Fresh", "Floral"]
    },
    {
        "text": "2. Your scent preference?",
        "options": ["A: Sweet & candy 🍬", "B: Woody & natural 🌲", "C: Clean & citrusy 🍋", "D: Spicy & warm 🔥"],
        "scores": ["Gourmand", "Woody", "Fresh", "Oriental"]
    },
    {
        "text": "3. Your vibe?",
        "options": ["A: Star girl/boy ✨", "B: Classy 👑", "C: Fun & funny 😂", "D: Calm, no noise 😌"],
        "scores": ["Oriental", "Floral", "Gourmand", "Woody"]
    },
    {
        "text": "4. Favorite time of day?",
        "options": ["A: Morning 🌅", "B: Golden hour 📸", "C: Night 🌃", "D: Afternoon ☀️"],
        "scores": ["Fresh", "Floral", "Oriental", "Gourmand"]
    },
    {
        "text": "5. Go-to drip?",
        "options": ["A: Ankara + sneakers 👟", "B: Crop top + lashes 💁🏾‍♀️", "C: Casual + cute 💖",
                    "D: Colourful & vibey 🌈"],
        "scores": ["Woody", "Oriental", "Floral", "Gourmand"]
    },
    {
        "text": "6. Dream vacation?",
        "options": ["A: Olumo Rock 🌿", "B: Zanzibar 🌊", "C: Dubai 🌆", "D: Paris 📸"],
        "scores": ["Woody", "Fresh", "Oriental", "Floral"]
    },
    {
        "text": "7. Pick a dessert:",
        "options": ["A: Small chops 🍥", "B: Zobo or Chapman 🍹", "C: Chin chin 🥥", "D: Suya 🌶️"],
        "scores": ["Gourmand", "Fresh", "Floral", "Oriental"]
    },
    {
        "text": "8. Favourite season?",
        "options": ["A: Rainy 🌧️", "B: Detty December 🔥", "C: Sunny beach ☀️", "D: Harmattan 🧴"],
        "scores": ["Woody", "Oriental", "Fresh", "Floral"]
    },
    {
        "text": "9. Everyday energy?",
        "options": ["A: Focus 🎧", "B: Always glowing 🌟", "C: Joy supplier 😂", "D: Silent baddie 🖤"],
        "scores": ["Woody", "Floral", "Gourmand", "Oriental"]
    },
    {
        "text": "10. Pick an accessory:",
        "options": ["A: Waist beads 🌺", "B: Sunglasses 🦋", "C: Earrings 🎀", "D: Bucket hat 🎨"],
        "scores": ["Woody", "Oriental", "Floral", "Gourmand"]
    }
]

perfume_recommendations = {
    "Floral": ["Gucci Bloom", "Chanel Chance Eau Tendre", "Yves Rocher Oui à l’Amour"],
    "Oriental": ["YSL Black Opium", "Dior Hypnotic Poison", "Zara Red Vanilla"],
    "Woody": ["Le Labo Santal 33", "Armaf Club de Nuit Intense", "Oud for Glory by Lattafa"],
    "Fresh": ["D&G Light Blue", "Versace Dylan Blue", "Davidoff Cool Water"],
    "Gourmand": ["Prada Candy", "Ariana Grande Cloud", "Lattafa Yara"]
}

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_data[user_id] = {"index": 0, "scores": {"Floral": 0, "Oriental": 0, "Woody": 0, "Fresh": 0, "Gourmand": 0}}
    await update.message.reply_text("🌸 Welcome to the Perfume Personality Quiz 🌸")
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    index = user_data[user_id]["index"]
    q = questions[index]
    markup = ReplyKeyboardMarkup([[opt] for opt in q["options"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(q["text"], reply_markup=markup)

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text
    if user_id not in user_data:
        await update.message.reply_text("Send /start to begin the quiz.")
        return

    index = user_data[user_id]["index"]
    if index >= len(questions):
        return

    options = questions[index]["options"]
    if text not in options:
        await update.message.reply_text("Please choose one of the options.")
        return

    selected = options.index(text)
    fragrance = questions[index]["scores"][selected]
    user_data[user_id]["scores"][fragrance] += 1
    user_data[user_id]["index"] += 1

    if user_data[user_id]["index"] < len(questions):
        await send_question(update, context)
    else:
        await send_result(update, context)
        del user_data[user_id]

async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    scores = user_data[user_id]["scores"]
    best = max(scores, key=scores.get)
    perfumes = perfume_recommendations[best]

    result_text = f"🔥 Your fragrance type is: *{best}* 🔥\n\nRecommended perfumes:\n"
    for p in perfumes:
        result_text += f"• {p}\n"

    await update.message.reply_text(result_text, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_response))
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()