package game;

import java.util.*;
import bot.Bot;

import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

/**
 * Created by krotkov on 7/30/2016.
 */
public class SingleGame {
    private Bot chat;


    private Map<User, Integer> results;
    private boolean inQuestion;
    private ArrayList<MusicFile> songs;
    private int currentSong;
    private Timer gameTimer;

    public SingleGame(Bot chat) {
        this.chat = chat;
        this.gameTimer = new Timer();
        this.results = new HashMap<>();

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
            return;
        }

        scheduleStartQuestion();
    }

    private void printResults() {
        String resultsToPrint = "";
        for (User u : results.keySet()) {
            resultsToPrint = resultsToPrint + u.firstName + " " + results.get(u) + "\n";
        }
        chat.sendMessage(resultsToPrint);
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
        ArrayList<MusicFile> result = new ArrayList<>();
        result.add(new MusicFile("a", "/home/bot/mp3/a.mp3"));
        result.add(new MusicFile("b", "/home/bot/mp3/a.mp3"));

        return result;
    }

    public void processMessage(User u, String s) {
        if (!inQuestion) {
            return;
        }
        if (s.equals(songs.get(currentSong).name)) {
            chat.sendMessage("Correct, " + u.firstName + "!");
            gameTimer.cancel();
            results.put(u, results.getOrDefault(u, 0) + 10);
            finishQuestion();
        } else {
            chat.sendMessage("Incorrect, " + u.firstName + "!");
            results.put(u, results.getOrDefault(u, 0) - 2);
        }
    }
}
