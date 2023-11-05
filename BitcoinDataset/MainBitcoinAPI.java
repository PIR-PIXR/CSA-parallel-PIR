import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeMap;

public class MainBitcoinAPI {

    public static void main(String[] args) throws APIException, IOException {
        BlockChainApi api = new BlockChainApi();
        long totalTxs;
        long average;

        //Latest Block
        LatestBlock latestBlock = api.getLatestBlock();
        System.out.println("Latest Block hash: " + latestBlock.getHash());

        //Single Block (00000000000000000001334ef43cdcfc0b506f4e0309d5386526e2a006b8b121 - 000000000000000000026607814031d366ea84686eb283cf08698ab15b988747 = average 1839 transactions)
        //Block sblock = api.getBlock("00000000000000000001334ef43cdcfc0b506f4e0309d5386526e2a006b8b121");
        Block sblock = api.getBlock(latestBlock.getHash());
        System.out.println("Number of transactions: " + sblock.getTransactions().size());
        //System.out.println("Merkle root: " + sblock.getMerkleRoot());

        //Ordering txs in the Merkle tree
        List<String> txHashList = toList(sblock.getTransactions());
        //Building the latest Merkle tree
        MerkleTrees MT = new MerkleTrees(txHashList);
        MT.merkle_tree();

        if (sblock.getMerkleRoot().equals(MT.getRoot())) {
            System.out.println("Building Merkle tree is correct!");
        }

        totalTxs = sblock.getTransactions().size();
        for (int i = 1; i < 200; i++) {
            sblock = api.getBlock(sblock.getPreviousBlockHash());
            totalTxs += sblock.getTransactions().size();
        }

        System.out.println("First Block hash: " + sblock.getHash());

        average = totalTxs/200;

        System.out.println("Average number of transactions per one Bitcoin block based on 1000 Bitcoin blocks recently: " + average);
    }

    private static TreeMap<Long, String> toTreeMap(List<Transaction> txs) {
        TreeMap<Long, String> txH = new TreeMap<>();
        for (Transaction tx : txs) {
            txH.put(tx.getIndex(), tx.getHash());
        }
        return txH;
    }

    private static List<String> toList(List<Transaction> txs) {
        List<String> txH = new ArrayList<>();
        for (Transaction tx : txs) {
            txH.add(tx.getHash());
        }
        return txH;
    }
}
