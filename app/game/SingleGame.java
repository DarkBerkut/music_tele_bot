package game;

import bot.Chat;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;

/**
 * Created by krotkov on 7/30/2016.
 */
public class SingleGame {
    private Chat chat;

    private Map<User, Integer> results;
    private boolean inQuestion;
    private boolean authorSuccess, trackSuccess;
    private ArrayList<MusicFile> songs;
    private int currentSong;
    private Timer gameTimer;

    public SingleGame(Chat chat) {
        this.chat = chat;
        this.gameTimer = new Timer();
        this.results = new HashMap<>();

        startGame();

    }

    private void scheduleStartQuestion() {
        gameTimer.cancel();
        gameTimer = new Timer();
        gameTimer.schedule(new TimerTask() {

            @Override
            public void run() {
                startQuestion();
            }
        }, 5 * 1000);
    }

    private void startQuestion() {
        chat.sendMessage("Question " + (currentSong + 1) + " out of " + songs.size());
        chat.sendMusic("/home/bot/python/data/music/cut/cut_" + songs.get(currentSong).filePath, "Song #" + (currentSong + 1));
        inQuestion = true;
        authorSuccess = false;
        trackSuccess = false;

        gameTimer.cancel();
        gameTimer = new Timer();
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
        printResults();
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
        currentSong = 0;
        inQuestion = false;

        chat.sendMessage("Preparing the game, please wait...");
        songs = generateSongs();
        chat.sendMessage("Songs prepared! The game will begin soon.");
        scheduleStartQuestion();
    }

    private void finishGame() {
        chat.sendMessage("Game is finished");
        gameTimer.cancel();
        chat.finishGame();
    }

    private ArrayList<MusicFile> generateSongs() {
        ArrayList<MusicFile> result = new ArrayList<>();
        String spoiler = "";

        try {
            Process p = Runtime.getRuntime().exec("python3 /home/bot/python/parse_request.py", null, new File("/home/bot/python"));
            Scanner s = new Scanner(p.getInputStream());
            for (int i = 0; i < 5; i++) {
                result.add(new MusicFile(s.next(), s.next()));
                spoiler = spoiler + result.get(result.size() - 1).toString() + "\n";
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        chat.sendMessage("SPOILER\n" + spoiler);
        return result;
    }

    public void processMessage(User u, String s) {
        if (!inQuestion) {
            return;
        }

        try {
            Process p = Runtime.getRuntime().exec("python3 /home/bot/python/parse_response.py", null, new File("/home/bot/python"));
            PrintWriter out = new PrintWriter(p.getOutputStream());
            Scanner in = new Scanner(p.getInputStream());

            in.useDelimiter("\t");

            out.print(songs.get(currentSong).name + "\t" + (authorSuccess ? 1 : 0) + "\t" + (trackSuccess ? 1 : 0) + "\t" + s + "\t");
            out.flush();

            boolean author = in.nextInt() == 1;
            boolean track = in.nextInt() == 1;
            String result = in.next();
            String spoiler = in.next();

            authorSuccess |= author;
            trackSuccess |= track;

            chat.sendMessage(result);
            chat.sendMessage("Author " + (authorSuccess ? "done" : "not done") + ", track " + (trackSuccess ? "done" : "not done") + ".");

            chat.sendMessage("SPOILER " + spoiler);

            if (authorSuccess && trackSuccess)
                finishQuestion();
        } catch (IOException e) {
            e.printStackTrace();
        }

        /*if (s.equals(songs.get(currentSong).name)) {
            chat.sendMessage("Correct, " + u.firstName + "!");
            results.put(u, results.getOrDefault(u, 0) + 10);
            finishQuestion();
        } else {
            chat.sendMessage("Incorrect, " + u.firstName + "!");
            results.put(u, results.getOrDefault(u, 0) - 2);
        }*/
    }
}
