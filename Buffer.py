# Copyright (c) 2014-2015 SwiperProxy Team
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish
# distribute, sublicense and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class Buffer(object):
    MAX_BUFFER = 1024 * 32
    def __init__(self, max_size=MAX_BUFFER):
        self.buffers = []
        self.max_size = max_size
        self.closing = False
        self.eof = False
        self.read_pos = 0
        self.write_pos = 0

    def write(self, data):
        try:
            if not self.buffers:
                self.buffers.append(StringIO())
                self.write_pos = 0
            buffer = self.buffers[-1]
            buffer.seek(self.write_pos)
            buffer.write(data)
            if buffer.tell() >= self.max_size:
                buffer = StringIO()
                self.buffers.append(buffer)
            self.write_pos = buffer.tell()
        finally:
            pass

    def read(self, length=-1):
        read_buf = StringIO()
        try:
            remaining = length
            while True:
                if not self.buffers:
                    break
                buffer = self.buffers[0]
                buffer.seek(self.read_pos)
                read_buf.write(buffer.read(remaining))
                self.read_pos = buffer.tell()
                if length == -1:
                    # We did not limit the read, we exhausted the
                    # buffer, so delete it and keep reading from
                    # remaining buffers.
                    del self.buffers[0]
                    self.read_pos = 0
                else:
                    # We limited the read so either we exhausted the
                    # buffer or not:
                    remaining = length - read_buf.tell()
                    if remaining > 0:
                        # Exhausted, remove buffer, read more. Keep
                        # reading from remaining buffers.
                        del self.buffers[0]
                        self.read_pos = 0
                    else:
                        # Did not exhaust buffer, but read all that
                        # was requested. Break to stop reading and
                        # return data of requested length.
                        break
        finally:
            pass
        return read_buf.getvalue()

    def flush(self):
        pass

    def __len__(self):
        len = 0
        try:
            for buffer in self.buffers:
                buffer.seek(0, 2)
                if buffer == self.buffers[0]:
                    len += buffer.tell() - self.read_pos
                else:
                    len += buffer.tell()
            return len
        finally:
            pass

    def close(self):
        self.eof = True
