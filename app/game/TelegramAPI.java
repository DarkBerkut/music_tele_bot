package game;

import java.io.IOException;

/**
 * Created by krotkov on 7/30/2016.
 */
public class TelegramAPI {
    public static void sendText(long chatId, String text) {
        try {
            Runtime.getRuntime().exec("/home/bot/scripts/send-text.sh " + chatId + " " + text);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void sendMusic(long chatId, String filePath){
        try {
            Runtime.getRuntime().exec("/home/bot/scripts/send-music.sh " + chatId + " " + filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
