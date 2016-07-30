package bot
import game.Controller
import telegram.TelegramApi

import scala.concurrent.Future

class ChatImpl(chatId: Long, controller: Controller, api: TelegramApi) extends Chat {

  override def sendMessage(text: String): Future[Unit] = {
    api.sendText(chatId, text)
  }

  override def sendMusic(filePath: String, title: String): Future[Unit] = {
    api.sendMusic(chatId, filePath, title)
  }

  override def finishGame(): Future[Unit] = Future.successful {
    controller.finishGame(chatId)
  }
}
