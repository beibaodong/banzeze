import os
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# 开启日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# --- 关键部分 ---
# 将你想要检测的贴纸的 file_unique_id 放在这里
# 这是从你提供的 JSON 的 message.sticker.file_unique_id 中获取的
TARGET_STICKER_UNIQUE_ID = "AgADfggAAkQFQFQ"

def check_sticker(update: Update, context: CallbackContext) -> None:
    """
    检查收到的消息是否为贴纸，如果是目标贴纸，则进行回复。
    """
    # 确保消息和贴纸对象存在，避免意外错误
    if not update.message or not update.message.sticker:
        return

    # 获取收到的贴纸的 unique_id
    received_sticker_id = update.message.sticker.file_unique_id
    logger.info(f"收到贴纸，file_unique_id: {received_sticker_id}")

    # 检查是否是我们想要的目标贴纸
    if received_sticker_id == TARGET_STICKER_UNIQUE_ID:
        logger.info("检测到目标贴纸！准备回复...")
        # 回复这条消息
        update.message.reply_text("不许啧啧")

def main() -> None:
    """启动机器人"""
    # 从环境变量中获取 Token
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("请设置 TELEGRAM_TOKEN 环境变量!")
        return

    # 创建 Updater 并传入你的 bot 的 token
    updater = Updater(TOKEN)

    # 获取 dispatcher 来注册处理器
    dispatcher = updater.dispatcher

    # --- 关键部分 ---
    # 创建一个 MessageHandler，使用 Filters.sticker 来捕获所有贴纸消息
    # 并将这些消息传递给 check_sticker 函数处理
    dispatcher.add_handler(MessageHandler(Filters.sticker, check_sticker))

    # 启动机器人
    updater.start_polling()
    logger.info("机器人已启动，正在监听贴纸...")

    # 让机器人持续运行
    updater.idle()

if __name__ == '__main__':
    main()