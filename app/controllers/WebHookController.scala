package controllers

import akka.http.scaladsl.model.{ContentTypes, HttpEntity, HttpMethods, HttpRequest}
import akka.http.scaladsl.unmarshalling.Unmarshal
import com.google.inject.Inject
import info.mukel.telegrambot4s.api.{Marshalling, TelegramBot}
import info.mukel.telegrambot4s.models.{Message, Update, User}
import play.api.Logger
import play.api.mvc.{Action, Controller}

class WebHookController @Inject()(configuration: play.api.Configuration) extends Controller
  with TelegramBot {

  val controller = new game.Controller()

  import Marshalling._

  def webHook = Action.async { request =>
    Logger.info("Body is: " + request.body)
    Logger.info("Webhook from telegram " + request)
    request.body
    val json = request.body.asJson.get.toString()
    val httpRequest = HttpRequest(HttpMethods.POST, entity = HttpEntity(ContentTypes.`application/json`, json))
    Unmarshal(httpRequest).to[Update].map(handleUpdate).map(_ => Ok(""))
  }

  override def handleMessage(message: Message): Unit = {
    val rawUser: User = message.from.get
    val user = new game.User(rawUser.id, rawUser.firstName)
    controller.processMessage(message.chat.id, user, message.text.getOrElse(""))
  }

  override def token: String = configuration.underlying.getString("telegram.auth")

  override def run(): Unit = {
  }
}