import os
import logging
import random # 1. 导入 random 模块
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# 开启日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# 目标贴纸的 unique_id
TARGET_STICKER_UNIQUE_ID = "AgADfggAAkQFQFQ"

# 2. 创建一个回复内容的列表（List）
REPLY_MESSAGES = [
    "不许啧啧",
    "啧啧怪又来了",
    "打倒啧啧怪！",
    "再啧啧就把你抓起来",
    "不要再啧啧了"
]

def check_sticker(update: Update, context: CallbackContext) -> None:
    """
    检查收到的消息是否为目标贴纸，如果是，则从列表中随机选择一条消息进行回复。
    """
    if not update.message or not update.message.sticker:
        return

    received_sticker_id = update.message.sticker.file_unique_id
    logger.info(f"收到贴纸，file_unique_id: {received_sticker_id}")

    if received_sticker_id == TARGET_STICKER_UNIQUE_ID:
        logger.info("检测到目标贴纸！准备随机回复...")
        
        # 3. 使用 random.choice() 从列表中随机选择一条消息
        random_reply = random.choice(REPLY_MESSAGES)
        
        # 回复这条随机选择的消息
        update.message.reply_text(random_reply)
        logger.info(f"已回复: '{random_reply}'")


def main() -> None:
    """启动机器人"""
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("请设置 TELEGRAM_TOKEN 环境变量!")
        return

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(MessageHandler(Filters.sticker, check_sticker))

    updater.start_polling()
    logger.info("机器人已启动，正在监听贴纸...")
    
    updater.idle()

if __name__ == '__main__':
    main()

