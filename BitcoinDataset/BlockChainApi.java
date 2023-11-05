import com.google.gson.GsonBuilder;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class BlockChainApi {
    private final String apiCode;
    private final GsonBuilder gson = new GsonBuilder();
    private final HttpClient client = new HttpClientImpl("https://blockchain.info/");
    private final StringBuilder blockQueryPathBuilder = new StringBuilder("rawblock/");
    private final StringBuilder txQueryPathBuilder = new StringBuilder("rawtx/");
    private final StringBuilder blockHeightQueryPathBuilder = new StringBuilder("block-height/");
    private static final String latestBlockPath = "latestblock/";

    public BlockChainApi() {
        apiCode = null;
    }

    public BlockChainApi(String apiCode) {
        this.apiCode = apiCode;
    }

    /**
     * Gets a single block based on a block index.
     *
     * @param blockIndex Block index
     * @return An instance of the {@link Block} class
     * @throws APIException If the server returns an error
     */
    public Block getBlock(long blockIndex) throws APIException, IOException {
        return getBlock(String.valueOf(blockIndex));
    }

    /**
     * Gets a single block based on a block hash.
     *
     * @param blockHash Block hash
     * @return An instance of the {@link Block} class
     * @throws APIException If the server returns an error
     */
    public Block getBlock(String blockHash) throws APIException, IOException {
        String response = client.get(blockQueryPathBuilder.append(blockHash).toString(), buildBasicRequest());
        return gson.create().fromJson(response, Block.class);
    }

    /**
     * Gets a list of blocks at the specified height. Normally, only one block will be
     * returned, but in case of a chain fork, multiple blocks may be present.
     *
     * @param height Block height
     * @return A list of blocks at the specified height
     * @throws APIException If the server returns an error
     */
    public BlockAtHeight getBlocksAtHeight(long height) throws APIException, IOException {

        String response = client.get(blockHeightQueryPathBuilder.append(height).toString(), buildBasicRequest());
        return gson.create().fromJson(response, BlockAtHeight.class);
    }

    /**
     * Gets the latest block on the main chain (simplified representation).
     *
     * @return An instance of the {@link LatestBlock} class
     * @throws APIException If the server returns an error
     */
    public LatestBlock getLatestBlock() throws APIException, IOException {
        String response = client.get(latestBlockPath, buildBasicRequest());
        return gson.create().fromJson(response, LatestBlock.class);
    }

    /**
     * Gets a single transaction based on a transaction index.
     *
     * @param txIndex Transaction index
     * @return An instance of the {@link Transaction} class
     * @throws APIException If the server returns an error
     * @deprecated As of 1.1.5, will be removed in future releases
     */
    @Deprecated
    public Transaction getTransaction(long txIndex) throws APIException, IOException {
        return getTransaction(String.valueOf(txIndex));
    }

    /**
     * Gets a single transaction based on a transaction hash.
     *
     * @param txHash Transaction hash
     * @return An instance of the {@link Transaction} class
     * @throws APIException If the server returns an error
     */
    public Transaction getTransaction(String txHash) throws APIException, IOException {
        String response = client.get(txQueryPathBuilder.append(txHash).toString(), buildBasicRequest());
        return gson.create().fromJson(response, Transaction.class);
    }

    private Map<String, String> buildBasicRequest() {
        Map<String, String> params = new HashMap<>();

        params.put("format", "json");
        if (apiCode != null) {
            params.put("api_code", apiCode);
        }

        return params;
    }
}
