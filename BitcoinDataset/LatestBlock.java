import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class LatestBlock {

    private final long height;
    private final String hash;
    private final long time;
    @SerializedName("block_index")
    private final long index;
    @SerializedName("txIndexes")
    private final List<Long> transactionIndexes;

    public LatestBlock(long height, String hash, long time, long index, List<Long> transactionIndexes) {
        this.height = height;
        this.hash = hash;
        this.time = time;
        this.index = index;
        this.transactionIndexes = transactionIndexes;
    }

    public long getHeight() {
        return height;
    }

    public String getHash() {
        return hash;
    }

    public long getTime() {
        return time;
    }

    public long getIndex() {
        return index;
    }

    public List<Long> getTransactionIndexes() {
        return transactionIndexes;
    }

    public String toJson() {
        return new Gson().toJson(this);
    }

    @Override
    public String toString() {
        return "LatestBlock{" +
                "height=" + height +
                ", hash='" + hash + '\'' +
                ", time=" + time +
                ", index=" + index +
                ", transactionIndexes=" + transactionIndexes +
                '}';
    }
}
