package game

import java.util.concurrent.ConcurrentHashMap

import bot.ChatImpl
import telegram.TelegramApi

import scala.concurrent.Future

class Controller(api: TelegramApi) {

  private val games = new ConcurrentHashMap[Long, SingleGame]()

  def processMessage(chatId: Long, user: User, text: String): Future[Unit] = {
    Option(games.get(chatId)) match {
      case Some(game) =>
        game.processMessage(user, text)
      case None =>
        if (text.startsWith("start")) {
          startGame(chatId, text.substring(6))
        }
    }
    Future.successful(())
  }

  def startGame(chatId: Long, cats: String) {
    games.put(chatId, new SingleGame(new ChatImpl(chatId, this, api), cats))
  }

  def finishGame(chatId: Long) {
    games.remove(chatId)
  }

}
