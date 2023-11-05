import com.google.gson.Gson;

import java.util.List;

public class BlockAtHeight {
    private final List<Block> blocks;

    public BlockAtHeight(List<Block> blocks) {
        this.blocks = blocks;
    }

    public List<Block> getBlocks() {
        return blocks;
    }


    public String toJson() {
        return new Gson().toJson(this);
    }

    @Override
    public String toString() {
        return "BlockAtHeight{" +
                "blocks=" + blocks +
                '}';
    }
}
