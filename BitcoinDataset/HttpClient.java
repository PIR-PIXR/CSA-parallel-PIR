import java.io.IOException;
import java.util.Map;
public interface HttpClient {
    /**
     * Call API with GET method
     *
     * @param resource API path
     * @param params   parameters
     * @return json data
     */
    String get(String resource, Map<String, String> params) throws APIException, IOException;

    /**
     * Call API with GET method
     *
     * @param url      home page url
     * @param resource api path
     * @param params   parameters
     * @return json data
     */
    String get(String url, String resource, Map<String, String> params) throws APIException, IOException;
}
