package game;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by krotkov on 7/30/2016.
 */
public class Controller {

    private Map<Long, SingleGame> games;

    Controller() {
        games = new HashMap<>();
    }

    public void processMessage(long chatId, User user, String text) {
        if (text.equals("start") && !games.containsKey(chatId)) {
            startGame(chatId);
            return;
        }

        if (!games.containsKey(chatId)) {
            return;
        }

        games.get(chatId).processMessage(user, text);
    }

    public void startGame(long chatId) {
        games.put(chatId, new SingleGame(new BotImpl(chatId, this)));
    }

    public void finishGame(long chatId) {
        games.remove(chatId);
    }
}
