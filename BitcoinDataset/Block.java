import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class Block {
    private final long height;
    private final String hash;
    private final long time;
    @SerializedName("main_chain")
    private final boolean mainChain;
    @SerializedName("ver")
    private final long version;
    @SerializedName("prev_block")
    private final String previousBlockHash;
    @SerializedName("next_block")
    private final List<String> nextBlockHashes;
    @SerializedName("mrkl_root")
    private final String merkleRoot;
    private final long bits;
    private final long fee;
    private final long nonce;
    private final long size;
    @SerializedName("block_index")
    private final long index;
    @SerializedName("received_time")
    private final long receivedTime;
    private final String relayedBy;
    @SerializedName("tx")
    private final List<Transaction> transactions;

    public Block(long height, String hash, long time, boolean mainChain, long version, String previousBlockHash, List<String> nextBlockHashes, String merkleRoot, long bits, long fee, long nonce, long size, long index, long receivedTime, String relayedBy, List<Transaction> transactions) {
        this.height = height;
        this.hash = hash;
        this.time = time;
        this.mainChain = mainChain;
        this.version = version;
        this.previousBlockHash = previousBlockHash;
        this.nextBlockHashes = nextBlockHashes;
        this.merkleRoot = merkleRoot;
        this.bits = bits;
        this.fee = fee;
        this.nonce = nonce;
        this.size = size;
        this.index = index;
        this.receivedTime = receivedTime;
        this.relayedBy = relayedBy;
        this.transactions = transactions;
    }

    public long getVersion() {
        return version;
    }

    public String getPreviousBlockHash() {
        return previousBlockHash;
    }

    public String getMerkleRoot() {
        return merkleRoot;
    }

    public long getBits() {
        return bits;
    }

    public long getFee() {
        return fee;
    }

    public long getNonce() {
        return nonce;
    }

    public long getSize() {
        return size;
    }

    public long getIndex() {
        return index;
    }

    public long getReceivedTime() {
        return receivedTime;
    }

    public String getRelayedBy() {
        return relayedBy;
    }

    public List<Transaction> getTransactions() {
        return transactions;
    }

    public List<String> getNextBlockHashes() {
        return nextBlockHashes;
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

    public boolean isMainChain() {
        return mainChain;
    }

    public String toJson() {
        return new Gson().toJson(this);
    }

    @Override
    public String toString() {
        return "Block{" +
                "version=" + version +
                ", previousBlockHash='" + previousBlockHash + '\'' +
                ", nextBlockHashes=" + nextBlockHashes +
                ", merkleRoot='" + merkleRoot + '\'' +
                ", bits=" + bits +
                ", fee=" + fee +
                ", nonce=" + nonce +
                ", size=" + size +
                ", index=" + index +
                ", receivedTime=" + receivedTime +
                ", relayedBy='" + relayedBy + '\'' +
                ", transactions=" + transactions +
                '}';
    }
}
