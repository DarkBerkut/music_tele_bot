package bot
import game.Controller
import telegram.TelegramApi

import scala.concurrent.Future

class BotImpl(chatId: Long, controller: Controller, api: TelegramApi) extends Bot {

  override def sendMessage(text: String): Future[Unit] = {
    api.sendText(chatId, text)
  }

  override def sendMusic(filePath: String): Future[Unit] = {
    api.sendMusic(chatId, filePath)
  }

  override def finishGame(): Future[Unit] = Future.successful {
    controller.finishGame(chatId)
  }
}
