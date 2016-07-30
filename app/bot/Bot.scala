package bot

import scala.concurrent.Future

trait Bot {
  def sendMessage(text: String): Future[Unit]

  def sendMusic(filePath: String): Future[Unit]

  def finishGame(): Future[Unit]
}
