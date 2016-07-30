package game;

/**
 * Created by krotkov on 7/30/2016.
 */
public interface Bot {

    public void sendMessage(String text);

    public void sendMusic(String filePath, String s);

    public void finishGame();
}
