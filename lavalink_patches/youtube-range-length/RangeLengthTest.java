import java.net.URI;
import org.apache.http.message.BasicHttpResponse;
import org.apache.http.ProtocolVersion;
import org.apache.http.entity.ByteArrayEntity;
import dev.lavalink.youtube.track.YoutubePersistentHttpStream;

class RangeLengthTest {
  static class Stream extends YoutubePersistentHttpStream {
    Stream(long size, String query) { super(null, URI.create("https://example.invalid/audio?"+query), size); }
    void prepare(long offset) { position=offset; getConnectUrl(); }
    long length() { return contentLength; }
  }
  static BasicHttpResponse response(long size) {
    var r=new BasicHttpResponse(new ProtocolVersion("HTTP",1,1),200,"OK");
    r.setHeader("Content-Length",Long.toString(size));
    r.setEntity(new ByteArrayEntity(new byte[0]));
    return r;
  }
  static void check(boolean ok) { if(!ok) throw new AssertionError(); }
  public static void main(String[] args) throws Exception {
    var unknown=new Stream(Long.MAX_VALUE, "itag=18"); unknown.prepare(0);
    var full=response(11862015); unknown.createContentInputStream(full);
    check(unknown.length()==Long.MAX_VALUE && full.getFirstHeader("Content-Length")==null);
    unknown.prepare(20000000);
    var last=response(1024); unknown.createContentInputStream(last);
    check(unknown.length()==20001024);
    var known=new Stream(30000000,"itag=140"); known.prepare(0);
    var chunk=response(11862015); known.createContentInputStream(chunk);
    check(known.length()==30000000 && chunk.getFirstHeader("Content-Length")!=null);
    var streaming=new Stream(Long.MAX_VALUE,"rn=1"); streaming.prepare(0);
    var streamResponse=response(100); streaming.createContentInputStream(streamResponse);
    check(streamResponse.getFirstHeader("Content-Length")!=null);
    System.out.println("PASS: unknown chunk size, final chunk offset, known size, streaming URL.");
  }
}
