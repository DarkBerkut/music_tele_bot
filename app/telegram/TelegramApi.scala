package telegram

import scala.concurrent.Future

trait TelegramApi {
  def sendText(chatId: Long, message: String): Future[Unit]

  def sendMusic(chatId: Long, filepath: String, title: String): Future[Unit]

  def sendImage(chatId: Long, filepath: String): Future[Unit]
}
