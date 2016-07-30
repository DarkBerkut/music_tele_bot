package game;

import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

/**
 * Created by krotkov on 7/30/2016.
 */
public class SingleGame {


    private Chat chat;

    private boolean inQuestion;
    private ArrayList<MusicFile> songs;
    private int currentSong;
    private Timer gameTimer;

    public SingleGame(Chat chat) {
        this.chat = chat;
        this.gameTimer = new Timer();

        startGame();
    }

    private void scheduleStartQuestion() {
        gameTimer.schedule(new TimerTask() {

            @Override
            public void run() {
                startQuestion();
            }
        }, 5 * 1000);
    }

    private void startQuestion() {
        chat.sendMessage("Question " + (currentSong + 1) + " out of " + songs.size());
        chat.sendMusic(songs.get(currentSong).filePath);
        inQuestion = true;

        gameTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                finishQuestion();
            }
        }, 60 * 1000);
    }

    private void finishQuestion() {
        chat.sendMessage("Question is finished.");
        inQuestion = false;
        currentSong++;
        if (currentSong == songs.size()) {
            finishGame();
        }

        scheduleStartQuestion();
    }

    private void startGame() {
        songs = generateSongs();
        currentSong = 0;
        inQuestion = false;

        chat.sendMessage("Starting the game!");

        scheduleStartQuestion();
    }

    private void finishGame() {
        chat.sendMessage("Game is finished");
        chat.finishGame();
    }

    private ArrayList<MusicFile> generateSongs() {
        return new ArrayList<>();
    }

    public void processMessage(User u, String s) {
        if (!inQuestion) {
            return;
        }
        if (s.equals(songs.get(currentSong))) {
            chat.sendMessage("Correct, " + u.firstName + "!");
            gameTimer.cancel();
            finishQuestion();
        } else {
            chat.sendMessage("Incorrect, " + u.firstName + "!");
        }
    }
}
