import java.security.MessageDigest;
import java.util.*;

public class MerkleTrees {
    //List of transactions
    private static List<String> txList;
    // Merkle Root
    private String root;

    //constructor
    public MerkleTrees(List<String> txList) {
        this.txList = txList;
        root = "";
    }

    /**
     * execute full merkle_tree and set root.
     */
    public void merkle_tree() {
        List<String> tempTxList = new ArrayList<>(txList);

        List<String> newTxList = getNewTxList(tempTxList);

        //Execute the loop until only one hash value is left
        while (newTxList.size() != 1) {
            newTxList = getNewTxList(newTxList);
        }

        this.root = newTxList.get(0);
    }

    /**
     * execute perfect merkle_tree and return HashMap to all the node in the tree.
     */
    public Map<Integer, String> perfect_merkle_tree(int h) {
        Map<Integer, String> tree = new HashMap<>();
        List<String> tempTxList = new ArrayList<>(txList);
        int startID = (int) Math.pow(2, h);

        //Put the leaves nodes on the tree
        for (String valueHash : tempTxList) {
            tree.put(startID, valueHash);
            startID++;
        }

        h--;
        startID = (int) Math.pow(2, h);
        List<String> newTxList = getNewTxList(tempTxList);
        for (String valueHash : newTxList) {
            tree.put(startID, valueHash);
            startID++;
        }

        //Execute the loop until only one hash value is left
        while (newTxList.size() != 1) {
            h--;
            startID = (int) Math.pow(2, h);
            newTxList = getNewTxList(newTxList);
            for (String valueHash : newTxList) {
                tree.put(startID, valueHash);
                startID++;
            }
        }
        this.root = newTxList.get(0);

        return tree;
    }

    /**
     * return New Hash List.
     */
    private static List<String> getNewTxList(List<String> tempTxList) {

        List<String> newTxList = new ArrayList<>();
        //hashing range of pairs nodes
        for (int i = 0; i < tempTxList.size() - 1; i = i + 2){
            String parentHash = rStrInHex(getSHA256(tempTxList.get(i), tempTxList.get(i + 1)));
            newTxList.add(parentHash);
        }
        //hashing the final odd node if appeared
        if (tempTxList.size() % 2 == 1) {
            // sha2 hex value
            String parentHash = rStrInHex(getSHA256(tempTxList.get(tempTxList.size() - 1), tempTxList.get(tempTxList.size() - 1)));
            newTxList.add(parentHash);
            //System.out.println("odd: " + parentHash);
        }

        return newTxList;
    }

    /**
     * Return hash value from two leaves
     */
    public static String getSHA256(String strInHexLeft, String strInHexRight) {
        try{
            //System.out.println("input: " + strInHex);
            MessageDigest md = MessageDigest.getInstance("SHA-256");

            String rStrLeftInHex = rStrInHex(strInHexLeft);
            String rStrRightInHex = rStrInHex(strInHexRight);
            String rStrcombine = rStrLeftInHex + rStrRightInHex;

            byte[] rStrInByte;
            rStrInByte = StrInByte(rStrcombine);

            //hashing a string in Hex value (sha256)
            byte[] digest = md.digest(md.digest(rStrInByte));

            //Convert Hex to String
            //bytes to hex
            StringBuilder sb = new StringBuilder(2 * digest.length);
            for(byte b: digest) {
                sb.append(String.format("%02x", b) );
            }
            return sb.toString();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "";
    }

    public String getRoot() {
        return this.root;
    }

    //reverse input hash value (str)
    private static String rStrInHex(String str){
        int index = str.length() - 2;
        StringBuilder rStr = new StringBuilder();

        while (index >= 0){
            rStr.append(str, index, index + 2);
            index -= 2;
        }
        return rStr.toString();
    }

    //Decode String hash to byte
    private static byte[] StrInByte(String strInHex){

        int index = 0;
        int j = 0;
        byte[] rStrInByte = new byte[strInHex.length()/2];
        StringBuilder rStrInHex = new StringBuilder();

        while (index < strInHex.length()){
            String tmp;
            tmp = strInHex.substring(index ,index+2);
            rStrInHex.append(tmp);

            int firstDigit = Character.digit(tmp.charAt(0), 16);
            int secondDigit = Character.digit(tmp.charAt(1), 16);
            rStrInByte[j++] = (byte) ((firstDigit << 4) + secondDigit);
            index += 2;
        }

        return rStrInByte;
    }
}
