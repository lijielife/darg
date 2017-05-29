import xlsxwriter


def save_to_excel_file(filename, rows, header=None, formats={}, response=None):
    """ save two dimensional list to excel file. learned here
    https://goo.gl/h397qZ

    formats param gives zeroindex col idx and format identifier just like
    `percent_format`

    pass `response` to return response in view
    """
    # Create a workbook and add a worksheet.
    if not response:
        workbook = xlsxwriter.Workbook(filename)
    else:
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    start = 0

    # formatting
    header_format = workbook.add_format({'bold': True})
    percent_format = workbook.add_format({'num_format': '0.0000%'})  # NOQA
    money_format = workbook.add_format({'num_format': '"CHF" #,##0'})  # NOQA

    if header:
        for idx, field in enumerate(header):
            col = xlsxwriter.utility.xl_col_to_name(idx)
            worksheet.write('{}1'.format(col.upper()),
                            field, header_format)
        start = 1

    # Iterate over the data and write it out row by row.
    for ridx, row in enumerate(rows, start):
        for idx, field in enumerate(row):
            # if we have a format specified
            if str(idx) in formats.keys():
                fmt = locals()[formats[str(idx)]]
                worksheet.write(ridx, idx, field, fmt)
            else:
                worksheet.write(ridx, idx, field)

    workbook.close()
