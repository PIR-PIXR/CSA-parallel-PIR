import com.google.gson.annotations.SerializedName;

public class Input {
    @SerializedName(value = "prev_out")
    private final Output previousOutput;
    private final long sequence;
    @SerializedName(value = "script")
    private final String scriptSignature;

    public Input(Output previousOutput, long sequence, String scriptSignature) {
        this.previousOutput = previousOutput;
        this.sequence = sequence;
        this.scriptSignature = scriptSignature;
    }

    public Output getPreviousOutput() {
        return previousOutput;
    }

    public long getSequence() {
        return sequence;
    }

    public String getScriptSignature() {
        return scriptSignature;
    }
}
