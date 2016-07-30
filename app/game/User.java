package game;

/**
 * Created by krotkov on 7/30/2016.
 */
public class User {

    public User(long id, String firstName) {
        this.id = id;
        this.firstName = firstName;
    }

    long id;
    String firstName;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        User user = (User) o;

        return id == user.id;

    }

    @Override
    public int hashCode() {
        return (int) (id ^ (id >>> 32));
    }
}
