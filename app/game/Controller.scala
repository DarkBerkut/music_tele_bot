package game

import java.util.concurrent.ConcurrentHashMap

import bot.BotImpl
import telegram.TelegramApi

import scala.concurrent.Future

class Controller(api: TelegramApi) {

  private val games = new ConcurrentHashMap[Long, SingleGame]()

  def processMessage(chatId: Long, user: User, text: String): Future[Unit] = {
    if (text == "start" && !games.containsKey(chatId)) {
      startGame(chatId)
      return Future.successful(())
    }
    if (!games.containsKey(chatId)) {
      return Future.successful(())
    }
    games.get(chatId).processMessage(user, text)
    Future.successful(())
  }

  def startGame(chatId: Long) {
    games.put(chatId, new SingleGame(new BotImpl(chatId, this, api)))
  }

  def finishGame(chatId: Long) {
    games.remove(chatId)
  }

}
