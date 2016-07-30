package bot

import scala.concurrent.Future

trait Chat {
  def sendMessage(text: String): Future[Unit]

  def sendMusic(filePath: String, title : String): Future[Unit]

  def finishGame(): Future[Unit]
}
