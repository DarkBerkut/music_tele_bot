package game;

/**
 * Created by krotkov on 7/30/2016.
 */
public class BotImpl implements Bot {
    long chatId;
    Controller controller;

    public BotImpl(long chatId, Controller controller) {
        this.chatId = chatId;
        this.controller = controller;
    }

    @Override
    public void sendMessage(String text) {
        TelegramAPI.sendText(chatId, text);
    }

    @Override
    public void sendMusic(String filePath) {
        TelegramAPI.sendMusic(chatId, filePath);
    }

    @Override
    public void finishGame() {
        controller.finishGame(chatId);
    }
}
