
# TODO: add colspan if _ after entry

test_table = '''

 <table>
    <thead>
    <tr>
    <th>Floor</th>
    <th align="right">Existing area (SDP)</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td>4</td>
    <td align="right">1,421</td>
    </tr>
    <tr>
    <td>3</td>
    <td align="right">1,468</td>
    </tr>
    <tr>
    <td>2</td>
    <td align="right">1,766</td>
    </tr>
    <tr>
    <td>1</td>
    <td align="right">1,741</td>
    </tr>
    <tr>
    <td>G</td>
    <td align="right">1,763</td>
    </tr>
    <tr>
    <td><strong>TOTAL</strong></td>
    <td align="right"><strong>8,159</strong></td>
    </tr>
    </tbody>
    </table>
    

'''

def remove_unused(str):
    return str.replace(' align="right"', '')

def number_format(str):
    return str.replace('0', '-')


def find_nth(string, substring, n):
    """
    You can find the nth occurrence of a substring in a string by splitting at the substring with max n+1 splits. If the resulting list has a size greater than n+1, it means that the substring occurs more than n times. Its index can be found by a simple formula, length of the original string - length of last splitted part - length of the substring.

    """
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)


def find_nth_row(str, n):
    """first row = 0"""
    row_start = find_nth(str, '<tr', n)
    row_end = str.find('</tr', row_start) + 5
    return str[row_start: row_end], row_start, row_end

def tst_find_nth_row():
    return (find_nth_row(test_table, 2))

def find_nth_col(str, n):
    """first col = 0"""
    col_start = find_nth(str, '<td', n) if find_nth(str, '<th', n) == -1 else find_nth(str, '<th', n)
    # for x in range(n+1):
    #     col_start = str.find('<td') if str.find('<th') == -1 else str.find('<th')
    col_end = str.find('</td', col_start) if str.find('</th', col_start) == -1 else str.find('</th', col_start)
    col_end += 5
    return str[col_start : col_end], col_start, col_end

def tst_find_nth_col():
    str, _, __ = find_nth_row(test_table, 0)
    return (find_nth_col(str, 1))


def find_start_tag(str, tag):
    start = str.find(f'<{tag}')
    end = str.find('>', start)
    return start, end

def find_tag_contents(str, tag):
    """returns what is inside the first instance of the specified tag"""
    _, a = find_start_tag(str, tag)
    b = str.find(f'</{tag}>', a)
    return str[a + 1:b]


def find_val(str, tag):
    """returns the value inside the tag, ie. ignores any qualifying sub tags such as <strong>
    eg. <td align="right"><strong><em>8,159</e></strong></td> returns 8,159"""
    inner = find_tag_contents(str, tag)
    if inner.find('>') > -1:
        st_ref = False
        for c_no, c in enumerate(inner):
            try:
                if c == '>' and inner[c_no + 1] != '<':
                    st_ref = c_no + 1
                    break
            except IndexError:
                break
        end_ref = inner.find('</', st_ref)
        if st_ref == False:
            return None
        else:
            return inner[st_ref:end_ref]
    else:
        return inner

def tst_find_val():
    # return (find_val('<td align="right"><strong><em>23453</e></strong></td>', 'td'))
    return (find_val('<td align="right">1,421</td>', 'td'))


def is_tag_numeric(str, tag):
    val = find_val(str, tag)
    if val is None:
        return False
    if val == '-' or val == '€':
        return True
    val = val.replace('.','').replace(',','').replace(' ','').replace('(','').replace(')','').replace('€', '').replace('m','').replace('M','')
    return val.isnumeric()

def tst_is_tag_numeric():
    return is_tag_numeric('<td align="right">1,421</td>', 'td')

def list_numeric_cols(str):
    title_row_end = str.find('</tr')
    first_row, _, __ = find_nth_row(str[title_row_end :], 0)
    no_cols = first_row.count('<td')
    numeric_cols = []
    st = 0
    for col_no in range(no_cols):
        if is_tag_numeric(first_row[st :], 'td'):
            numeric_cols.append(col_no)
        td_end = first_row.find('</td', st)
        st = td_end + 5
    return numeric_cols, no_cols

def tst_list_numeric_cols():
    return(list_numeric_cols(test_table))


def list_bold_rows(str):
    num_rows = str.count('<tr')
    st = 0
    bold_rows = []
    for row_num in range(num_rows):
        row_start = str.find('<tr', st)
        row_end = str.find('</tr', row_start + 4)
        row = str[row_start : row_end + 5]
        st = row_end + 5
        val = find_val(row, 'td')
        if val is not None:
            val = val.upper()
            if 'TOT' in val:
                bold_rows.append(row_num)
    return bold_rows




def process_html(html_str):
    """

    formats tables so all columns with a number in the first row are aligned right
    and
    total row is bold

    classes:
    al-r = right align
    bld = bold

    :param html_str: html string
    :return: processed html
    """
    html_str = remove_unused(html_str)
    st = 0
    no_tables = html_str.count('<table')
    st = 0
    for tbl in range(no_tables):
        tbl_st = html_str.find('<table', st)
        tbl_end = html_str.find('</table>', tbl_st) + 8
        table_str = html_str[tbl_st : tbl_end]
        st = tbl_end + 1
        numeric_cols, num_cols = list_numeric_cols(table_str)
        # print('numeric cols:',numeric_cols)
        num_rows = table_str.count('<tr')
        bold_rows = list_bold_rows(table_str)
        # print('bold rows:', bold_rows)

        # Format table
        for row_num in range(num_rows):
            row, row_start, row_end = find_nth_row(table_str, row_num)
            # print('old row', row.replace('\n', ''))
            stc = 0
            for col_num in range(num_cols):
                cell_contents, col_start, col_end = find_nth_col(row, col_num)

                if col_num in numeric_cols and row_num in bold_rows:
                    cls = 'tot al-r'
                    stc += 17
                elif row_num in bold_rows:
                    cls = 'tot'
                    stc += 12
                elif col_num in numeric_cols:
                    cls = 'al-r'
                    stc += 13
                    # print('row', row_num, 'col', col_num)
                else:
                    cls = False

                if cls:
                    edited_col_contents = cell_contents[ : 3] + f' class="{cls}"' + cell_contents[3 : ]
                    # print(edited_col_contents)

                    row = f'{row[0: col_start -1]}{edited_col_contents}{row[col_end:]}'
            row = row.replace('\n', '') + '\n'
            # print('new row:', row)

            table_str = table_str[ : row_start -1] + row + table_str[row_end : ]


        html_str = html_str[ : tbl_st -1] + table_str + html_str[tbl_end : ]

    return html_str



if __name__ == "__main__":
    test_str = '''



<table>
<thead>
<tr>
<th>Floor</th>
<th align="right">Existing area (SDP)</th>
</tr>
</thead>
<tbody>
<tr>
<td>4</td>
<td align="right">1,421</td>
</tr>
<tr>
<td>3</td>
<td align="right">1,468</td>
</tr>
<tr>
<td>2</td>
<td align="right">1,766</td>
</tr>
<tr>
<td>1</td>
<td align="right">1,741</td>
</tr>
<tr>
<td>G</td>
<td align="right">1,763</td>
</tr>
<tr>
<td><strong>TOTAL</strong></td>
<td align="right"><strong>8,159</strong></td>
</tr>
</tbody>
</table>

    <table>
    <tr><th>one</th><th>two</th><th>three</th><th>four</th><th>five</th><th>six</th></tr>
    <tr><td>text</td><td>8,789</td><td>text</td><td>535,546</td><td>text</td><td>text</td></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>TOTAL</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    </table>

    '''
    # print(tst_is_tag_numeric())
    # print(tst_list_numeric_cols())
    # print(tst_find_val())
    # print(tst_find_nth_row())
    print(tst_find_nth_col())
    #
    print(process_html(test_str))
    # process_html(test_str)
    #
    # print(is_tag_numeric('<td align="right">17.62</td>', 'td'))
    # print(find_val('<td align="right">17.62</td>', 'td'))


    '''
        
    <p> some tjns</p>
    
    swd
    
    wd
    
    <table>
    <tr><th>one</th><th>two</th><th>three</th><th>four</th><th>five</th><th>six</th></tr>
    <tr><td>text</td><td>8,789</td><td>text</td><td>535,546</td><td>text</td><td>text</td></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>TOTAL</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    </table>
    <table>
    <tr><th>one</th><th>two</th><th>three</th><th>four</th><th>five</th><th>six</th></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>text</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    <tr><td>TOTAL/AV</td><td>8789</td><td>text</td><td>text</td><td>text</td><td>text</td></tr>
    </table>
    
    '''