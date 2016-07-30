package game;

/**
 * Created by krotkov on 7/30/2016.
 */
public class MusicFile {

    public MusicFile(String name, String filePath) {
        this.name = name;
        this.filePath = filePath;
    }

    @Override
    public String toString() {
        return "MusicFile{" +
                "name='" + name + '\'' +
                ", filePath='" + filePath + '\'' +
                '}';
    }

    String name;
    String filePath;
}
