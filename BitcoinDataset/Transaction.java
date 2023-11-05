import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class Transaction {
    @SerializedName("double_spend")
    private final boolean doubleSpend;
    @SerializedName("block_height")
    private final long blockHeight;
    @SerializedName("block_index")
    private final long blockIndex;
    private final long time;
    @SerializedName("lock_time")
    private final long lockTime;
    @SerializedName("relayed_by")
    private final String relayedBy;
    private final String hash;
    @SerializedName("tx_index")
    private final long index;
    private final long version;
    private final long size;
    private final List<Input> inputs;
    @SerializedName("out")
    private final List<Output> outputs;

    public Transaction(boolean doubleSpend, long blockHeight, long blockIndex, long time, long lockTime, String relayedBy, String hash, long index, long version, long size, List<Input> inputs, List<Output> outputs) {
        this.doubleSpend = doubleSpend;
        this.blockHeight = blockHeight;
        this.blockIndex = blockIndex;
        this.time = time;
        this.lockTime = lockTime;
        this.relayedBy = relayedBy;
        this.hash = hash;
        this.index = index;
        this.version = version;
        this.size = size;
        this.inputs = inputs;
        this.outputs = outputs;
    }

    public boolean isDoubleSpend() {
        return doubleSpend;
    }

    public long getBlockHeight() {
        return blockHeight;
    }

    public long getTime() {
        return time;
    }

    public long getLockTime() {
        return lockTime;
    }

    public String getRelayedBy() {
        return relayedBy;
    }

    public String getHash() {
        return hash;
    }

    public long getIndex() {
        return index;
    }

    public long getVersion() {
        return version;
    }

    public long getSize() {
        return size;
    }

    public List<Input> getInputs() {
        return inputs;
    }

    public List<Output> getOutputs() {
        return outputs;
    }

    public long getBlockIndex() {
        return blockIndex;
    }

    public String toJson() {
        return new Gson().toJson(this);
    }

    @Override
    public String toString() {
        return "Transaction{" +
                "doubleSpend=" + doubleSpend +
                ", blockHeight=" + blockHeight +
                ", blockIndex=" + blockIndex +
                ", time=" + time +
                ", lockTime=" + lockTime +
                ", relayedBy='" + relayedBy + '\'' +
                ", hash='" + hash + '\'' +
                ", index=" + index +
                ", version=" + version +
                ", size=" + size +
                ", inputs=" + inputs +
                ", outputs=" + outputs +
                '}';
    }
}
