package controllers

import akka.http.scaladsl.model.{ContentTypes, HttpEntity, HttpMethods, HttpRequest}
import akka.http.scaladsl.unmarshalling.Unmarshal
import akka.util.ByteString
import com.google.inject.Inject
import info.mukel.telegrambot4s.api.TelegramBot
import info.mukel.telegrambot4s.methods.SetWebhook
import info.mukel.telegrambot4s.api.Marshalling
import info.mukel.telegrambot4s.models.InputFile.FromByteString
import info.mukel.telegrambot4s.models.Update
import play.api.Logger
import play.api.mvc.{Action, Controller}

import scala.util.{Failure, Success}

class WebHookController @Inject()(configuration: play.api.Configuration) extends Controller
  with TelegramBot {

  import Marshalling._

  run()

  def webHook = Action.async { request =>
    Logger.info("Webhook from telegram " + request)
    val httpRequest = HttpRequest(HttpMethods.POST, entity = HttpEntity(ContentTypes.`application/json`, request.body.asText.get))
    Unmarshal(httpRequest).to[Update].map(handleUpdate).map(_ => Ok(""))
  }

  override def token: String = configuration.underlying.getString("telegram.auth")

  override def run(): Unit = {
    val host = configuration.underlying.getString("host.name")
    val method = routes.WebHookController.webHook().url
    val port = System.getProperty("https.port")
    val hookUrl = s"https://$host:$port$method"
    Logger.info(s"Setting webhook to $hookUrl")
    val cert = getClass.getResourceAsStream("/music_bot_public.pem")
    val certContent = scala.io.Source.fromInputStream(cert).getLines().mkString("\n")
    FromByteString("music_bot_public.pem", ByteString(certContent))
    api.request(SetWebhook(Some(hookUrl))) onComplete {
      case Success(true) => Logger.info("Successfully registered webhook")
      case Success(false) => Logger.error("Can not register webhook")
      case Failure(e) => Logger.error("Exception while regestering webhook", e)
    }
  }
}