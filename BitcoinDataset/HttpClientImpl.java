import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Map;

public class HttpClientImpl implements HttpClient {

    private final String API_HOME;
    private int TIMEOUT_MS = 10000;

    public HttpClientImpl(String API_HOME) {
        this.API_HOME = API_HOME;
    }

    public HttpClientImpl(String API_HOME, int TIMEOUT_MS) {
        this.API_HOME = API_HOME;
        this.TIMEOUT_MS = TIMEOUT_MS;
    }

    /**
     * Common API call method
     *
     * @param baseURL       Home page url
     * @param resource      API url
     * @param params        paramaters
     * @param requestMethod POST| GET
     * @return json data
     */
    private String call(String baseURL, String resource, Map<String, String> params, String requestMethod) throws APIException, IOException {
        String encodedParams = Util.urlEncodeParams(params);
        URL url;
        APIException apiException = null;
        IOException ioException = null;

        String result = null;


        if (requestMethod.equals("POST")) {
            url = new URL(baseURL + resource);
        } else {
            // GET method
            if (encodedParams.isEmpty()) {
                url = new URL(baseURL + resource);
            } else {
                url = new URL(baseURL + resource + '?' + encodedParams);
            }
        }

        HttpURLConnection conn = null;

        try {
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod(requestMethod);
            conn.setConnectTimeout(TIMEOUT_MS);

            if (requestMethod.equals("POST")) {
                byte[] postBytes = encodedParams.getBytes(StandardCharsets.UTF_8);
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                conn.setRequestProperty("Content-Length", String.valueOf(postBytes.length));
                conn.getOutputStream().write(postBytes);
                conn.getOutputStream().close();
            }

            if (conn.getResponseCode() != 200) {
                apiException = new APIException(Util.inputStreamToString(conn.getErrorStream()));
            } else {
                result = Util.inputStreamToString(conn.getInputStream());
            }
        } catch (IOException e) {
            ioException = e;
        } finally {
            try {
                if (apiException != null) {
                    conn.getErrorStream().close();
                }
                if (conn != null) {
                    conn.getInputStream().close();
                }
            } catch (Exception ignored) {
            }

            if (ioException != null) {
                throw ioException;
            }

            if (apiException != null) {
                throw apiException;
            }
        }

        return result;
    }


    @Override
    public String get(String resource, Map<String, String> params) throws APIException, IOException {
        return call(API_HOME, resource, params, "GET");
    }

    @Override
    public String get(String url, String resource, Map<String, String> params) throws APIException, IOException {
        return call(url, resource, params, "GET");
    }
}
