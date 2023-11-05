import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

public class Util {

    /**
     * Parse hex string to binary string
     *
     * @param hex hex string
     * @return binary string
     */
    public static String parseHex2Binary(String hex) {
        String digits = "0123456789ABCDEF";
        String[] bin = {"0000", "0001", "0010", "0011",
                "0100", "0101", "0110", "0111",
                "1000", "1001", "1010", "1011",
                "1100", "1101", "1110", "1111"};
        hex = hex.toUpperCase();
        StringBuilder binaryString = new StringBuilder();

        for (int i = 0; i < hex.length(); i++) {
            char c = hex.charAt(i); // get corresponding hex code
            int d = digits.indexOf(c); // convert to decimal
            binaryString.append(bin[d]);
        }
        return binaryString.toString();
    }

    //

    /**
     * Function to extract k bits from p position and returns the extracted value as integer
     *
     * @param number target number
     * @param k      k bits want to extract
     * @param p      position
     * @return k bits as integer
     */
    public static int bitsExtracted(int number, int k, int p) {
        return (((1 << k) - 1) & (number >> (p - 1)));
    }

    /**
     * Read string from input stream
     *
     * @param is input stream
     * @return string
     */
    public static String inputStreamToString(InputStream is) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));

        StringBuilder responseStringBuilder = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            responseStringBuilder.append(line);
        }

        reader.close();

        return responseStringBuilder.toString();
    }

    /**
     * Build a params string with UTF-8 encoding
     *
     * @param params params map
     * @return params string
     */
    public static String urlEncodeParams(Map<String, String> params) {
        String result = "";

        if (params != null && params.size() > 0) {
            StringBuilder data = new StringBuilder();
            for (Map.Entry<String, String> kvp : params.entrySet()) {
                if (data.length() > 0) {
                    data.append('&');
                }

                data.append(URLEncoder.encode(kvp.getKey(), StandardCharsets.UTF_8));
                data.append('=');
                data.append(URLEncoder.encode(kvp.getValue(), StandardCharsets.UTF_8));
            }
            result = data.toString();
        }

        return result;
    }

    /**
     * calculate log2 n indirectly using log() method
     *
     * @param n number
     * @return log2(n)
     */

    public static int log2(int n) {
        return (int) (Math.log(n) / Math.log(2));
    }

    /**
     * Compute standard deviation
     *
     * @param m list of value
     * @return std value
     */
    public static double computeSD(Map<String, Double> m) {
        List<Double> x = new ArrayList<>(m.values());
        double total = x.stream().mapToDouble(y -> y).sum();
        double mean = total / x.size();
        double sum = x.stream().mapToDouble(y -> Math.pow(y - mean, 2)).sum();
        return Math.sqrt(sum / x.size());
    }

    /**
     * Sort by values
     *
     * @param m input map
     * @return sorted map
     */
    public static HashMap<String, Integer> sortByValue(HashMap<String, Integer> m) {
        return m.entrySet()
                .stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue())
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));
    }
}
