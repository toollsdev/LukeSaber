package dev.lavalink.youtube.track;

import com.sedmelluq.discord.lavaplayer.tools.io.HttpClientTools;
import com.sedmelluq.discord.lavaplayer.tools.io.HttpInterface;
import com.sedmelluq.discord.lavaplayer.tools.io.PersistentHttpStream;
import org.apache.http.client.utils.URIBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URISyntaxException;

/**
 * A persistent HTTP stream implementation that uses the range parameter instead of HTTP headers for specifying
 * the start position at which to start reading on a new connection.
 */
public class YoutubePersistentHttpStream extends PersistentHttpStream {
    private static final Logger log = LoggerFactory.getLogger(YoutubePersistentHttpStream.class);

    // Valid range for requesting without throttling is 0-11862014
    private static final long BUFFER_SIZE = 11862014;

    private long rangeEnd;

    /**
     * @param httpInterface The HTTP interface to use for requests
     * @param contentUrl The URL of the resource
     * @param contentLength The length of the resource in bytes
     */
    public YoutubePersistentHttpStream(HttpInterface httpInterface, URI contentUrl, long contentLength) {
        super(httpInterface, contentUrl, contentLength);
    }

    @Override
    public InputStream createContentInputStream(org.apache.http.HttpResponse response) throws IOException {
        // A range response reports the chunk size, not the resource size.
        // PersistentHttpStream would otherwise treat the first chunk as EOF
        // when YouTube omits contentLength (notably with legacy format 18).
        if (contentLength == Long.MAX_VALUE && rangeEnd != 0 && !contentUrl.toString().contains("rn=")) {
            org.apache.http.Header header = response.getFirstHeader("Content-Length");
            if (header != null) {
                long chunkLength = Long.parseLong(header.getValue());
                long requestedLength = rangeEnd - position + 1;
                if (chunkLength < requestedLength) {
                    contentLength = position + chunkLength;
                } else {
                    response.removeHeaders("Content-Length");
                }
            }
        }
        return super.createContentInputStream(response);
    }

    @Override
    protected URI getConnectUrl() {
        if (!contentUrl.toString().contains("rn=")) {
            URI rangeUrl = getNextRangeUrl();

            log.debug("Range URL: {}", rangeUrl.toString());

            return rangeUrl;
        } else {
            return contentUrl;
        }
    }

    @Override
    protected int internalRead(byte[] b, int off, int len, boolean attemptReconnect) throws IOException {
        connect(false);
        long nextExpectedPosition = position + len + (len / 2);

        try {
            int result;
            if (nextExpectedPosition >= rangeEnd && rangeEnd != 0) {
                if (rangeEnd == contentLength) {
                    result = currentContent.read(b, off, len);
                    position += result;
                } else {
                    result = 0;
                    handleRangeEnd(null, attemptReconnect);
                }
            } else {
                result = currentContent.read(b, off, len);
                if (result >= 0) {
                    position += result;
                    if (position >= rangeEnd && !contentUrl.toString().contains("rn=")) {
                        handleRangeEnd(null, attemptReconnect);
                    }
                }
            }

            return result;
        } catch (IOException e) {
            handleRangeEnd(e, attemptReconnect);
            return internalRead(b, off, len, false);
        }
    }

    @Override
    protected long internalSkip(long n, boolean attemptReconnect) throws IOException {
        connect(false);
        long nextExpectedPosition = position + n;

        try {
            long result;
            if (nextExpectedPosition >= rangeEnd && rangeEnd != 0) {
                if (rangeEnd == contentLength) {
                    result = currentContent.skip(n);
                    position += result;
                } else {
                    result = n;
                    position += n;
                    handleRangeEnd(null, attemptReconnect);
                }
            } else {
                result = currentContent.skip(n);
                position += result;
                if (position >= rangeEnd && !contentUrl.toString().contains("rn=")) {
                    handleRangeEnd(null, attemptReconnect);
                }
            }

            return result;
        } catch (IOException e) {
            handleRangeEnd(e, attemptReconnect);
            return internalSkip(n, false);
        }
    }

    private URI getNextRangeUrl() {
        rangeEnd = position + BUFFER_SIZE;

        if (rangeEnd > contentLength) {
            rangeEnd = contentLength;
        }

        try {
            return new URIBuilder(contentUrl).addParameter("range", position + "-" + rangeEnd).build();
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }

    private void handleRangeEnd(IOException exception, boolean attemptReconnect) throws IOException {
        if (!attemptReconnect || (!HttpClientTools.isRetriableNetworkException(exception) && exception != null)) {
            throw exception;
        }

        close();
    }

    @Override
    protected boolean useHeadersForRange() {
        return false;
    }

    @Override
    public boolean canSeekHard() {
        return true;
    }
}
