package game;

import telegram.TelegramApi;

/**
 * Created by krotkov on 7/30/2016.
 */
public class BotImpl implements Bot {
    long chatId;
    Controller controller;
    TelegramApi telegramApi;

    public BotImpl(long chatId, Controller controller, TelegramApi telegramApi) {
        this.chatId = chatId;
        this.controller = controller;
        this.telegramApi = telegramApi;
    }

    @Override
    public void sendMessage(String text) {
        telegramApi.sendText(chatId, text);
    }

    @Override
    public void sendMusic(String filePath) {
        telegramApi.sendMusic(chatId, filePath);
    }

    @Override
    public void finishGame() {
        controller.finishGame(chatId);
    }
}
