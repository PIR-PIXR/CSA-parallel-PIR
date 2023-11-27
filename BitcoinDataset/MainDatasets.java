import java.io.*;
import java.util.*;
import com.google.gson.*;
import java.security.SecureRandom;
import java.security.NoSuchAlgorithmException;

//-------------------------------------------Color-Spliting-Algorithm (CSA) Main class----------------------------------------
public class MainDatasets {

    public static void main(String[] args) throws APIException, IOException, NoSuchAlgorithmException {

        final String PATH = "/Path/to/Datasets/";

        ColorSplittingAlgorithm CSA = new ColorSplittingAlgorithm();
        BlockChainApi api = new BlockChainApi();

        //Array of balanced/unbalanced sets
        NodesSet[] NodesSets;
        //List of color sequence c = [c1,...,ch]
        List<NumColor> c = new ArrayList<>();

        byte h; //h is the height of a tree
        char[] color = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'
                , 'R','S', 'T', 'U', 'V','W', 'X', 'Y', 'Z','0', '1', '2', '3', '4', '5', '6', '7','8', '9'};

        //Latest Block
        LatestBlock latestBlock = api.getLatestBlock();
        System.out.println("Latest Block hash: " + latestBlock.getHash());
        Block sblock = api.getBlock(latestBlock.getHash());
        //Single Block
        //Block sblock = api.getBlock("00000000000000000001334ef43cdcfc0b506f4e0309d5386526e2a006b8b121");

        //Loop to generate datasets from 2^10 to 2^20
        for (h = 10; h < 21; h += 2) {
            System.gc(); //runs the garbage collector
            int height = h;

            //Building the latest Perfect Merkle tree with adding random leaves
            List<String> txHashListPerfect = perfectList(sblock, (int) Math.pow(2, h));

            //Building the latest Merkle tree
            MerkleTrees PMT = new MerkleTrees(txHashListPerfect);
            Map<Integer, String> perfectMT = PMT.perfect_merkle_tree(height);

            c = CSA.balancedColorSequence(h);
            Collections.sort(c);

            System.out.println("Generating datasets with the tree height, h = " + h + ", take some time ...");
            //Color-Splitting Algorithm
            NodesSets = CSA.ColorSplitting(h, c);

            //Stored sub-databases/Color classes and stored them in JSON files for CSA
            genColoringDatabase(NodesSets, perfectMT, height, PATH);
            //Stored a whole database (a Verkle tree)
            genWholeTreeDatabase(perfectMT, height, PATH);
            //Stored a layer-by-layer database
            genLayerDatabase(perfectMT, height, PATH);
            //Stored a proof-as-element database
            genProofasElementDatabase(perfectMT, height, PATH);
            //Stored a PBC database
            genPBCDatabase(perfectMT, height, PATH);

            c.clear();
        }
    }

    //Method to collect n leaves/transactions in a Bitcoin
    private static List<String> perfectList(Block sblock, int n) throws NoSuchAlgorithmException, APIException, IOException {
        BlockChainApi api = new BlockChainApi();
        List<String> txH = new ArrayList<>();
        List<Transaction> txnew;
        List<Transaction> txs = sblock.getTransactions();

        while (txs.size() < n) {
            sblock = api.getBlock(sblock.getPreviousBlockHash());
            txnew = sblock.getTransactions();
            txs.addAll(txnew);
        }

        for (int i = 0; i < n; i++) {
            txH.add(txs.get(i).getHash());
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

    // Method to generate a random string of a specified length
    private static String RandomHexString(int length) {
        SecureRandom secureRandom = new SecureRandom();
        byte[] randomBytes = new byte[length];
        secureRandom.nextBytes(randomBytes);

        StringBuilder result = new StringBuilder();
        for (byte b : randomBytes) {
            result.append(String.format("%02X", b));
        }

        return result.toString();
    }

    // Method to generate Coloring databases
    private static void genColoringDatabase(NodesSet[] NodesSets, Map<Integer, String> perfectMT, int height, String PATH) {
        Gson gson = new Gson();
        Arrays.stream(NodesSets).forEach(s -> {
            // Create a JSON array to hold NodeID-value pairs
            JsonArray nodeValueArray = new JsonArray();
            JsonObject nodeValueObject = new JsonObject();
            Arrays.stream(s.getAddNodes()).forEach(r -> nodeValueObject.addProperty(String.valueOf(r), perfectMT.get(r)));
            nodeValueArray.add(nodeValueObject);

            // Serialize the JSON array to a string
            String jsonString = gson.toJson(nodeValueArray);

            // Specify the file path where you want to write the JSON data
            String filePath = PATH + "color" + s.getColorSet() + "_" + height + ".json";
            // Write the JSON data to the file
            try (FileWriter fileWriter = new FileWriter(filePath)) {
                fileWriter.write(jsonString);
                System.out.println("JSON data written to " + filePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }

    // Method to generate a whole database (a Verkle tree)
    private static void genWholeTreeDatabase(Map<Integer, String> perfectMT, int height, String PATH) {
        Gson gson = new Gson();

        // Create a JSON array to hold key-value pairs
        JsonArray valueArray = new JsonArray();
        JsonObject valueObject = new JsonObject();

        perfectMT.forEach((key, value) -> {
            if (key >= 2) {
                valueObject.addProperty(String.valueOf(key), value);
            }
        });

        valueArray.add(valueObject);
        // Serialize the JSON array to a string
        String jsonString = gson.toJson(valueArray);

        // Specify the file path where you want to write the JSON data
        String filePath = PATH + "wholeTree" + "_" + height + ".json";
        // Write the JSON data to the file
        try (FileWriter fileWriter = new FileWriter(filePath)) {
            fileWriter.write(jsonString);
            System.out.println("JSON data written to " + filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Method to generate a layer-based database
    private static void genLayerDatabase(Map<Integer, String> perfectMT, int height, String PATH) {
        // Initialize Gson
        Gson gson = new Gson();
        int nodeID = 1;

        for (int i = 0; i < height; i++) {
            // Create a JSON array to hold key-value pairs
            JsonArray valueArray = new JsonArray();
            JsonObject valueObject = new JsonObject();

            for (int j = 0; j < (int) Math.pow(2, i + 1); j++) {
                nodeID++;
                valueObject.addProperty(String.valueOf(nodeID), perfectMT.get(nodeID));
            }
            valueArray.add(valueObject);
            // Serialize the JSON array to a string
            String jsonString = gson.toJson(valueArray);
            //System.out.println(jsonString);

            int l = i + 1;
            // Specify the file path where you want to write the JSON data
            String filePath = PATH + "layer" + l + "_" + height + ".json";
            // Write the JSON data to the file
            try (FileWriter fileWriter = new FileWriter(filePath)) {
                fileWriter.write(jsonString);
                System.out.println("JSON data written to " + filePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // Method to generate a proof-as-element database
    private static void genProofasElementDatabase(Map<Integer, String> perfectMT, int height, String PATH) {
        // Initialize Gson
        Gson gson = new Gson();
        // Create a JSON array to hold key-value pairs
        JsonArray valueArray = new JsonArray();
        JsonObject valueObject = new JsonObject();
        int j = 0;

        for (int i = (int) Math.pow(2, height); i < (int) Math.pow(2, height + 1); i++) {
            int nodeID = i;
            String proof = "";
            do {
                proof += perfectMT.get(nodeID);
                nodeID = nodeID / 2;
            } while (nodeID != 1);
            j++;
            valueObject.addProperty(String.valueOf(j), proof);
        }
        valueArray.add(valueObject);

        // Serialize the JSON array to a string
        String jsonString = gson.toJson(valueArray);

        // Specify the file path where you want to write the JSON data
        String filePath = PATH + "proofAsElement" + "_" + height + ".json";
        // Write the JSON data to the file
        try (FileWriter fileWriter = new FileWriter(filePath)) {
            fileWriter.write(jsonString);
            System.out.println("JSON data written to " + filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Method to generate a PBC database
    private static void genPBCDatabase(Map<Integer, String> perfectMT, int height, String PATH) {
        // Initialize Gson
        Gson gson = new Gson();
        Random rand = new Random();
        int numbuckets = (int) Math.ceil(1.5 * height);
        List<List<Integer>> buckets = new ArrayList<>();
        // Initialize the buckets
        for (int i = 0; i < numbuckets; i++) {
            buckets.add(new ArrayList<>());
        }

        for (int i = 2; i < (int) Math.pow(2, height + 1); i++) {
            for (int j = 0; j < 3; j++) {
                int b = rand.nextInt(numbuckets);
                while (buckets.get(b).contains(i)) {
                    b = rand.nextInt(numbuckets);
                }
                buckets.get(b).add(i);
            }
        }

        for (int i = 0; i < buckets.size(); i++) {
            // Create a JSON array to hold key-value pairs
            JsonArray valueArray = new JsonArray();
            JsonObject valueObject = new JsonObject();

            List<Integer> bucket = buckets.get(i);
            for (int j = 0; j < bucket.size(); j++) {
                valueObject.addProperty(String.valueOf(bucket.get(j)), perfectMT.get(bucket.get(j)));
            }
            valueArray.add(valueObject);
            // Serialize the JSON array to a string
            String jsonString = gson.toJson(valueArray);
            int m = i + 1;
            // Specify the file path where you want to write the JSON data
            String filePath = PATH + "PBC" + m + "_" + height + ".json";
            // Write the JSON data to the file
            try (FileWriter fileWriter = new FileWriter(filePath)) {
                fileWriter.write(jsonString);
                System.out.println("JSON data written to " + filePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}


//-----------------------------------------Color-Splitting Algorithm class----------------------------------------------
class ColorSplittingAlgorithm {

    NodesSet[] NodesSets;
    HashMap<List<NumColor>, List<NumColor>> C = new HashMap<>();
    char[] color = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'
            , 'R','S', 'T', 'U', 'V','W', 'X', 'Y', 'Z','0', '1', '2', '3', '4', '5', '6', '7','8', '9'};

    //Given a feasible sequence 𝑐 = [𝑐1, . . . , 𝑐ℎ], the algorithm finds a 𝑐-coloring of 𝑇 (ℎ)
    public NodesSet[] ColorSplitting(byte h, List<NumColor> c) {
        //the root of 𝑇 (ℎ) is 1
        int R = 1;
        NodesSets = new NodesSet [h];

        for (byte q = 0; q < h; q++) {
            int size = c.get(q).getSize();
            NodesSets[q] = new NodesSet(c.get(q).getColor(), size);
        }

        ColorSplittingRecursive(R, h, c);

        return NodesSets;
    }

    //𝑅 is the root node of the current subtree 𝑇 (ℎ) of height ℎ
    //Either 𝑅 needs no color (𝑅 = 1) or 𝑅 has already been colored in the previous call
    //𝑐 = [𝑐1, . . . , 𝑐ℎ] is a feasible color sequence, which implies that 2 ≤ 𝑐1 ≤ 𝑐2 ≤ · · · ≤ 𝑐ℎ
    //This procedure colors the two children of 𝑅 and create feasible color sequences for its
    //left and right subtrees
    public void ColorSplittingRecursive(int R, byte h, List<NumColor> c) {
        int A, B;
        List<NumColor> a = new ArrayList<>(h - 1);
        List<NumColor> b = new ArrayList<>(h - 1);
        C.clear();

        if (h > 0) {
            A = 2 * R; //left child of 𝑅
            B = 2 * R + 1; //right child of 𝑅

            //Assign Color 1 to both 𝐴 and 𝐵; And add A and B to the same set.
            if (c.get(0).getSize() == 2) {
                for (NodesSet s : NodesSets) {
                    if (s.getColorSet() == c.get(0).getColor()) {
                        s.addNode(A);
                        s.addNode(B);
                    }
                }
            }
            //Assign Color 1 to 𝐴 and Color 2 to 𝐵; And add A and B to 2 different sets.
            else {
                for (NodesSet s : NodesSets) {
                    if (s.getColorSet() == c.get(0).getColor()) {
                        s.addNode(A);
                    }
                    if (s.getColorSet() == c.get(1).getColor()) {
                        s.addNode(B);
                    }
                }
            }

            //Split the feasible sequence c to a feasible sequence a and a feasible sequence b
            if (h > 1) {
                C = FeasibleSplit(h, c);
                C.forEach((n, m) -> {
                    a.addAll(n);
                    b.addAll(m);
                });

                Collections.sort(a);
                ColorSplittingRecursive(A, (byte) (h - 1), a);

                Collections.sort(b);
                ColorSplittingRecursive(B, (byte) (h - 1), b);
            }
        }
    }

    /* This algorithm splits a ℎ-feasible sequence into two (ℎ − 1)-feasible ones, which will be used for coloring the subtrees; only works when ℎ ≥ 2.
    Note that the splitting rule (see FeasibleSplit(ℎ, 𝑐)) ensures that if Color 𝑖 is used for a node then it will no longer be used in the subtree rooted at that node,
    hence guaranteeing the Ancestral Property.*/
    //key = a; value = b which are two (ℎ − 1)-feasible of two subtrees following "Procedure FeasibleSplit(ℎ, 𝑐)"
    public HashMap<List<NumColor>, List<NumColor>> FeasibleSplit(byte h, List<NumColor> c) {
        List<NumColor> a = new ArrayList<>(h - 1);
        List<NumColor> b = new ArrayList<>(h - 1);
        C.clear();

        if (h == 2) {
            byte i = 1; //Position 2
            int aValue, bValue;

            if (c.get(0).getSize() == 2) {
                aValue = c.get(i).getSize() / 2;
                bValue = c.get(i).getSize() / 2;
                a.add(new NumColor(c.get(1).getColor(), aValue));
                b.add(new NumColor(c.get(1).getColor(), bValue));
            }
            else {
                aValue = c.get(i).getSize() - 1;
                bValue = c.get(0).getSize() - 1;
                a.add(new NumColor(c.get(1).getColor(), aValue));
                b.add(new NumColor(c.get(0).getColor(), bValue));
            }

            Collections.sort(a);
            Collections.sort(b);
            C.put(a, b);

            return C;
        }
        else if (h > 2) {
            //Case 1: 𝑐1 = 2
            if (c.get(0).getSize() == 2) {
                byte i = 1; //Position 2
                int aValue = (int) Math.floor(c.get(i).getSize() / 2.0);
                int bValue = (int) Math.ceil(c.get(i).getSize() / 2.0);
                a.add(new NumColor(c.get(i).getColor(), aValue));
                b.add(new NumColor(c.get(i).getColor(), bValue));
                int Sa = aValue; //Left sum
                int Sb = bValue; //Right sum
                i++;
                //change for original algorithm
                while (i < h) {
                    if (Sa < Sb) {
                        aValue = (int) Math.ceil(c.get(i).getSize() / 2.0);
                        bValue = (int) Math.floor(c.get(i).getSize() / 2.0);
                    }
                    else {
                        aValue = (int) Math.floor(c.get(i).getSize() / 2.0);
                        bValue = (int) Math.ceil(c.get(i).getSize() / 2.0);
                    }
                    a.add(new NumColor(c.get(i).getColor(), aValue));
                    b.add(new NumColor(c.get(i).getColor(), bValue));
                    Sa += aValue;
                    Sb += bValue;
                    i++;
                }
            }
            //Case 2: 𝑐1 > 2; note that 𝑐1 ≥ 2 due to the feasibility of 𝑐;
            else {
                byte i = 1; //Position 2
                int aValue = c.get(i).getSize() - 1;
                int bValue = c.get(0).getSize() - 1;
                a.add(new NumColor(c.get(1).getColor(), aValue));
                b.add(new NumColor(c.get(0).getColor(), bValue));
                int Sa = aValue; //Left sum
                int Sb = bValue; //Right sum
                i++;
                aValue = (int) Math.ceil((c.get(i).getSize() + c.get(0).getSize() - c.get(i - 1).getSize()) / 2.0);
                bValue = c.get(i - 1).getSize() - c.get(0).getSize() + (int) Math.floor((c.get(i).getSize() + c.get(0).getSize() - c.get(i - 1).getSize()) / 2.0);
                a.add(new NumColor(c.get(i).getColor(), aValue));
                b.add(new NumColor(c.get(i).getColor(), bValue));
                Sa += aValue;
                Sb += bValue;
                i++;
                while (i < h) {
                    if (Sa < Sb) {
                        aValue = (int) Math.ceil(c.get(i).getSize() / 2.0);
                        bValue = (int) Math.floor(c.get(i).getSize() / 2.0);
                    }
                    else {
                        aValue = (int) Math.floor(c.get(i).getSize() / 2.0);
                        bValue = (int) Math.ceil(c.get(i).getSize() / 2.0);
                    }
                    a.add(new NumColor(c.get(i).getColor(), aValue));
                    b.add(new NumColor(c.get(i).getColor(), bValue));

                    Sa += aValue;
                    Sb += bValue;
                    i++;
                }
            }
            Collections.sort(a);
            Collections.sort(b);
            C.put(a, b);
            return C;
        }
        else {
            System.out.println("Warming! h should be greater than or equal 2"); //𝑐 ≥ 2 due to the feasibility of 𝑐;
            return null;
        }
    }

    //Corollary 2.12 (Balanced Color sequence) return 𝑐 = [𝑐1, 𝑐2, . . . , 𝑐ℎ]
    public List<NumColor> balancedColorSequence(byte h) {
        int cValue;
        byte u = (byte) ((Math.pow(2, h + 1) - 2) % h);
        List<NumColor> c = new ArrayList<>(h);

        for (byte i = 0; i < h; i++) {
            double a = (Math.pow(2, h + 1) - 2) / h;
            if (i < (h - u)) {
                cValue = (int) Math.floor(a);
                c.add(new NumColor(color[i], cValue));
            }
            else {
                cValue = (int) Math.ceil(a);
                c.add(new NumColor(color[i], cValue));
            }
        }

        return c;
    }
}


//-----------------------------------------Set of Nodes have the same color class------------------------------------------------------------
/* An example of a perfect binary tree with h = 2
                       1
                    /    \
                  2       3
                /  \    /  \
               4   5   6    7
*/
//Each set will contain all node with the same color
class NodesSet {

    private int count = 0;
    private final char colorSet;
    //Array of node IDs (R)
    private final int [] addNodes;

    public NodesSet(char colorSet, int size) {
        this.colorSet = colorSet;
        addNodes = new int [size];
    }

    public void addNode(int root) {
        //array start from 0, whereas node colored start from 2
        addNodes[count] = root;
        count++;
    }

    public int [] getAddNodes() {
        return addNodes;
    }

    public char getColorSet() {
        return colorSet;
    }

    public int getSize() {
        return count;
    }

    @Override
    public String toString() {
        StringBuilder roots = new StringBuilder();
        for (int addNode : addNodes) {
            roots.append(addNode).append(" ");
        }

        return roots.toString();
    }
}


//-----------------------------------------NumColor class---------------------------------------------------------------
//Stored and Sorted vector c.
class NumColor implements Comparable<NumColor> {

    private final int size;
    private final char color;

    public NumColor(char color, int size) {
        this.color = color;
        this.size = size;
    }

    public char getColor() {
        return color;
    }

    public int getSize() {
        return size;
    }

    @Override
    public int compareTo(NumColor otherNumColor) {
        return Integer.compare(getSize(), otherNumColor.getSize());
    }
}
