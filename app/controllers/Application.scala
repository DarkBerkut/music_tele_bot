package controllers

import com.google.inject.Inject
import play.api._
import play.api.mvc._
import play.api.Logger

class Application @Inject() (configuration: play.api.Configuration) extends Controller {
  def index = Action {
    Logger.info("Telegram auth is: " + configuration.underlying.getString("telegram.auth"))
    Ok(views.html.index("Your new application is ready."))
  }

}