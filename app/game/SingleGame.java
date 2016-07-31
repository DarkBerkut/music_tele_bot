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

    public SingleGame(Chat chat, String cats) throws GameNotStartedException {
        this.chat = chat;
        this.gameTimer = new Timer();
        this.results = new HashMap<>();

        startGame(cats);

    }

    private void scheduleStartQuestion() {
        gameTimer.cancel();
        gameTimer = new Timer();
        gameTimer.schedule(new TimerTask() {

            @Override
            public void run() {
                startQuestion();
            }
        }, 1 * 1000);
    }

    private void startQuestion() {
//        chat.sendMessage("Question " + (currentSong + 1) + " out of " + songs.size());
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
        String resultsToPrint = "Текущие реультаты\n";
        for (User u : results.keySet()) {
            resultsToPrint = resultsToPrint + u.firstName + " " + results.get(u) + "\n";
        }
        chat.sendMessage(resultsToPrint);
    }

    private void startGame(String cats) throws GameNotStartedException {
        currentSong = 0;
        inQuestion = false;

        songs = generateSongs(cats);
        if (songs == null) {
            throw new GameNotStartedException();
        }
        chat.sendMessage("Игра готова!");
        scheduleStartQuestion();
    }

    private void finishGame() {
        chat.sendMessage("Игра окончена!");
        gameTimer.cancel();
        chat.finishGame();
    }

    private ArrayList<MusicFile> generateSongs(String cats) {
        ArrayList<MusicFile> result = new ArrayList<>();
        String spoiler = "";

        try {
            Process p = Runtime.getRuntime().exec("python3 /home/bot/python/parse_request.py", null, new File("/home/bot/python"));
            PrintWriter out = new PrintWriter(p.getOutputStream());
            out.println(cats);
            out.flush();
            Scanner s = new Scanner(p.getInputStream());
            String status = s.next();
            String comment = s.nextLine();
            if (status.equals("UNK")) {
                chat.sendMessage(comment);
                return null;
            }
            chat.sendMessage(comment + "\n" + "Игра загружается, осталось совсем немного...");
            for (int i = 0; i < 5; i++) {
                result.add(new MusicFile(s.next(), s.next()));
                spoiler = spoiler + result.get(result.size() - 1).toString() + "\n";
                if (!s.hasNext()) {
                    break;
                }
            }
            out.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    private void log(String s) {
        System.err.println(s);
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

            out.println(songs.get(currentSong).name + "\t" + (authorSuccess ? 1 : 0) + "\t" + (trackSuccess ? 1 : 0) + "\t" + s + "\n");
            out.flush();
            boolean author = in.nextInt() == 1;
            boolean track = in.nextInt() == 1;
            String result = in.next();
            String spoiler = in.next();
            in.close();
            out.close();

            int score = 0;
            if (!authorSuccess && author) {
                score += 5;
            }
            if (!trackSuccess && track) {
                score += 5;
            }

            if (score == 0 && !author && !track)
                score -= 2;

            authorSuccess |= author;
            trackSuccess |= track;

            chat.sendMessage(u.firstName + " " + (score > 0 ? "+" : "") + score +  (score >= 0 ? "очков" : "очка") + "\n" +
                    result + "\n" +
                    "Автор " + (authorSuccess ? "отгадан" : "не отгадан") + ", название " + (trackSuccess ? "отгадано" : "не отгадано") + "." + "\n" +
                    "SPOILER " + spoiler);

            results.put(u, results.getOrDefault(u, 0) + score);

            if (authorSuccess && trackSuccess)
                finishQuestion();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
