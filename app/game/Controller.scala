package game

import java.util.concurrent.ConcurrentHashMap

import bot.ChatImpl
import telegram.TelegramApi

import scala.concurrent.Future

class Controller(api: TelegramApi) {

  private val games = new ConcurrentHashMap[Long, SingleGame]()

  def processMessage(chatId: Long, user: User, text: String): Future[Unit] = {
    if (games.containsKey(chatId)) {
      games.get(chatId).processMessage(user, text)
    } else {
      if (text.startsWith("start")) {
        startGame(chatId, text.substring(6))
      }
    }

    Future.successful(())
  }

  def startGame(chatId: Long, cats: String) {
    try {
      games.put(chatId, new SingleGame(new ChatImpl(chatId, this, api), cats))
    } catch {
      case e: GameNotStartedException => {}
    }
  }

  def finishGame(chatId: Long) {
    games.remove(chatId);
  }

}
