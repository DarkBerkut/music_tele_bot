package telegram
import java.io.File

import info.mukel.telegrambot4s.api.TelegramApiAkka
import info.mukel.telegrambot4s.methods.{SendAudio, SendMessage}
import info.mukel.telegrambot4s.models.InputFile.FromFile
import play.api.Logger

import scala.concurrent.{ExecutionContext, Future}

class TelegramApiImpl(api: TelegramApiAkka)(implicit ec: ExecutionContext) extends TelegramApi {
  override def sendText(chatId: Long, message: String): Future[Unit] = {
    api.request(SendMessage(Left(chatId), message)).map {
      m => Logger.info(s"Got response for $chatId, message: $message. $m")
    }
  }

  override def sendMusic(chatId: Long, filepath: String, title : String): Future[Unit] = {
    api.request(SendAudio(Left(chatId), Left(FromFile(new File(filepath))), title = Option(title))).map {
      m => Logger.info(s"Got response for $chatId, audio: $filepath. $m")
    }
  }
}
