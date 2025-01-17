import re
import Util

class CSSPage:
    """
    Used for a CSS stylesheet. Uses the reader function to read a
    block, rewrites that block and writes it to the client using the
    writer function.
    """
    BLKSIZE = 65536

    def __init__(self, config, ssl, reader, writer, remote_host):
        self.config = config
        self.ssl = ssl
        self.reader = reader
        self.writer = writer
        self.input_buffer = ''
        self.output_buffer = ''
        self.remote_host = remote_host

    def rewrite_re(self, m):
        part1 = m.group(1) or ''
        scheme = m.group(6) or ''
        url = m.group(7) or ''
        closer = m.group(9) or ''

        return part1 + Util.rewrite_URL(scheme+"//"+url, self.config, self.ssl,
                                        self.remote_host) + closer

    def rewrite(self):
        pattern = r"(((background(-image)?\s*:)|@import)\s*(url)?\s*[('\"]+\s*)(https?:)?//([^\"')]+)(:\d+)?([)'\"]+)"

        while True:
            s = self.reader(self.BLKSIZE)
            if not s or len(s) == 0:
                # End of file, there may be a left-over in the input
                # buffer.
                self.output_buffer += self.input_buffer
                self.write_output(True)
                break

            self.input_buffer += s

            news = re.sub(pattern, self.rewrite_re, self.input_buffer,
                          re.I|re.M|re.S)

            # It may be the case that the background image string is
            # divided over two blocks. Keep the last 1024 bytes in the
            # input buffer and write everything up to that point to the
            # output buffer
            if len(news) > 1024:
                self.output_buffer += news[:-1024]
                self.input_buffer = news[-1024:]
                self.write_output(False)
            else:
                self.output_buffer += news
                self.input_buffer = ''
                self.write_output(False)

    def write_output(self, final):
        length = len(self.output_buffer)
        for beg in range(0, length, self.BLKSIZE):
            end = beg + self.BLKSIZE
            if end > length:
                if not final:
                    self.output_buffer = self.output_buffer[beg:]
                    return
                end = length
            self.writer(self.output_buffer[beg:end])

        self.output_buffer = ''
