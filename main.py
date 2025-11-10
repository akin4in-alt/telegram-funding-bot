TELEGRAM_TOKEN = '8569146023:AAF7TYji1L_knFqOoTSdIMg4UbD2bXaMgI8'
CHAT_ID = 342441148  # Целое число, а не строка
https://github.com/akin4in-alt/telegram-funding-bot/tree/main
def fetch_funding_rates():
    url = 'https://api-dev.goldlink.io/?method=goldlink/getAllMarketOneHourFunding'
    res = requests.get(url).json()
    data = res.get('result', [])
    lines = []
    for item in data:
        market = item['market']
        rate = int(item['funding_rate']) / 1e30 * 100
        lines.append(f"{market}: {rate:.6f}%")
    return "\n".join(lines)

def send_funding(context):
    msg = fetch_funding_rates()
    context.bot.send_message(chat_id=CHAT_ID, text=msg[:4000])

def main():
    updater = Updater(TELEGRAM_TOKEN)
    job_queue = updater.job_queue
    # Запускаем задачу сразу и повторяем каждый час
    job_queue.run_repeating(send_funding, interval=3600, first=0)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
