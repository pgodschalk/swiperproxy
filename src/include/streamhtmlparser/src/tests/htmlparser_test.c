/* Copyright (c) 2008, Google Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *     * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following disclaimer
 * in the documentation and/or other materials provided with the
 * distribution.
 *     * Neither the name of Google Inc. nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ---
 * Author: Filipe Almeida
 */

#include "config.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <streamhtmlparser/htmlparser.h>

/* Taken from google templates */

#define ASSERT(cond)  do {                                      \
  if (!(cond)) {                                                \
    printf("%s: %d: ASSERT FAILED: %s\n", __FILE__, __LINE__,   \
           #cond);                                              \
    assert(cond);                                               \
    exit(1);                                                    \
  }                                                             \
} while (0)

#define ASSERT_STREQ(a, b)  do {                                          \
  if (strcmp((a), (b))) {                                                 \
    printf("%s: %d: ASSERT FAILED: '%s' != '%s'\n", __FILE__, __LINE__,   \
           (a), (b));                                                     \
    assert(!strcmp((a), (b)));                                            \
    exit(1);                                                              \
  }                                                                       \
} while (0)

#define ASSERT_STRSTR(text, substr)  do {                       \
  if (!strstr((text), (substr))) {                              \
    printf("%s: %d: ASSERT FAILED: '%s' not in '%s'\n",         \
           __FILE__, __LINE__, (substr), (text));               \
    assert(strstr((text), (substr)));                           \
    exit(1);                                                    \
  }                                                             \
} while (0)


/* Process a string using entityfilter_process(). */
void entityfilter_process_str(entityfilter_ctx *filter, const char *in,
                              char *out)
{
  out[0] = '\0';
  while (*in) {
    strcat(out, entityfilter_process(filter, *in));
    ++in;
  }
}

/* Verify that the code still builds with a C compiler. */
void test_c_build()
{
  htmlparser_ctx *html;

#ifdef __cplusplus
  printf("C build test compiled in c++ mode.");
  exit(1);
#endif /* __cplusplus */

  html = htmlparser_new();
  htmlparser_delete(html);
  printf("DONE.\n");
}

/* Entity filter tests. */
void test_entityfilter()
{
  entityfilter_ctx *filter = entityfilter_new();
  char buffer[256];

  entityfilter_process_str(filter, "test", buffer);
  ASSERT_STREQ("test", buffer);

  entityfilter_process_str(filter, "testtest", buffer);
  ASSERT_STREQ("testtest", buffer);

  entityfilter_process_str(filter, "test&apos;test", buffer);
  ASSERT_STREQ("test'test", buffer);

  entityfilter_process_str(filter, "test&#39;test", buffer);
  ASSERT_STREQ("test'test", buffer);

  entityfilter_process_str(filter, "test&#x27;test", buffer);
  ASSERT_STREQ("test'test", buffer);

  entityfilter_process_str(filter, "test&#X27;test", buffer);
  ASSERT_STREQ("test'test", buffer);

  entityfilter_process_str(filter, "A&#65;&#x41;A", buffer);
  ASSERT_STREQ("AAAA", buffer);

  entityfilter_process_str(filter, "A&#65 &#x41 A", buffer);
  ASSERT_STREQ("AAAA", buffer);

  entityfilter_process_str(filter, "test&invalid;test", buffer);
  ASSERT_STREQ("test&invalid;test", buffer);

  entityfilter_process_str(filter, "test&invalid;01234567890123456789", buffer);
  ASSERT_STREQ("test&invalid;01234567890123456789", buffer);

  entityfilter_process_str(filter, "test&incomplete01234567890123456789", buffer);
  ASSERT_STREQ("test&incomplete01234567890123456789", buffer);

  entityfilter_process_str(filter, "test&012345;big", buffer);
  ASSERT_STREQ("test&012345;big", buffer);

  entityfilter_process_str(filter, "test&0123456;big", buffer);
  ASSERT_STREQ("test&0123456;big", buffer);

  entityfilter_process_str(filter, "test&01234567;big", buffer);
  ASSERT_STREQ("test&01234567;big", buffer);

  entityfilter_process_str(filter, "test&012345678;big", buffer);
  ASSERT_STREQ("test&012345678;big", buffer);

  entityfilter_process_str(filter, "test&0123456789;big", buffer);
  ASSERT_STREQ("test&0123456789;big", buffer);

  entityfilter_process_str(filter, "test&01234567890;big", buffer);
  ASSERT_STREQ("test&01234567890;big", buffer);

  entityfilter_process_str(filter, "test&012345678901;big", buffer);
  ASSERT_STREQ("test&012345678901;big", buffer);

  entityfilter_process_str(filter, "test& & & & & & & & & & &", buffer);
  ASSERT_STREQ("test& & & & & & & & & & ", buffer);

  entityfilter_delete(filter);
}

void test_position()
{
  htmlparser_ctx *html;
  html = htmlparser_new();

  ASSERT(htmlparser_get_line_number(html) == 1);

  htmlparser_parse_str(html, "<html>\n<body>\n");
  ASSERT(htmlparser_get_line_number(html) == 3);
  ASSERT(htmlparser_get_column_number(html) == 1);

  htmlparser_parse_str(html, "<h1>blah</h1>");
  ASSERT(htmlparser_get_line_number(html) == 3);
  ASSERT(htmlparser_get_column_number(html) == 14);

  htmlparser_parse_str(html, "<h2>blah</h2>\n\n\n\n\n");
  ASSERT(htmlparser_get_line_number(html) == 8);
  ASSERT(htmlparser_get_column_number(html) == 1);

  htmlparser_set_line_number(html, 2);
  ASSERT(htmlparser_get_line_number(html) == 2);
  ASSERT(htmlparser_get_column_number(html) == 1);

  htmlparser_parse_str(html, "<html>\n<body>\n");
  ASSERT(htmlparser_get_line_number(html) == 4);
  ASSERT(htmlparser_get_column_number(html) == 1);

  htmlparser_set_column_number(html, 4);
  htmlparser_parse_str(html, "<h1>blah</h1>");
  ASSERT(htmlparser_get_line_number(html) == 4);
  ASSERT(htmlparser_get_column_number(html) == 17);

  htmlparser_parse_str(html, "<h2>blah</h2>\n\n\n\n\n");
  ASSERT(htmlparser_get_line_number(html) == 9);

  htmlparser_reset(html);
  ASSERT(htmlparser_get_line_number(html) == 1);

  htmlparser_parse_str(html, "- \n - \n - \n - \n - \n");
  ASSERT(htmlparser_get_line_number(html) == 6);

  htmlparser_reset(html);
  htmlparser_parse_str(html, "- \n\r - \n - \r - \r\n - \r - \n\r");
  ASSERT(htmlparser_get_line_number(html) == 5);

  htmlparser_parse_str(html, "<html>\n<body>\n<a href=");
  ASSERT(htmlparser_get_line_number(html) == 7);
  ASSERT(htmlparser_get_column_number(html) == 9);

  htmlparser_parse_str(html, ">\n</body>\n</html>");
  ASSERT(htmlparser_get_line_number(html) == 9);
  ASSERT(htmlparser_get_column_number(html) == 8);

  htmlparser_delete(html);
}

int main(int argc, char **argv)
{
  test_c_build();
  test_entityfilter();
  test_position();
  printf("DONE.\n");
  return 0;
}
