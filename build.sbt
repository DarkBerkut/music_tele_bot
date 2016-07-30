name := "MusicBot"

version := "1.0"

lazy val `musicbot` = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.11.7"

libraryDependencies ++= Seq( jdbc , cache , ws   , specs2 % Test )

libraryDependencies += "com.github.mukel" %% "telegrambot4s" % "v1.2.1"

libraryDependencies += "org.xerial" % "sqlite-jdbc" % "3.8.6"

unmanagedResourceDirectories in Test <+=  baseDirectory ( _ /"target/web/public/test" )  

resolvers += "scalaz-bintray" at "https://dl.bintray.com/scalaz/releases"

resolvers += "jitpack" at "https://jitpack.io"