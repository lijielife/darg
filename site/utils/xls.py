import xlsxwriter


def save_to_excel_file(filename, rows, header=None):
    """ save two dimensional list to excel file. learned here
    https://goo.gl/h397qZ """
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    start = 0

    # formatting
    header_format = workbook.add_format({'bold': True})

    if header:
        for idx, field in enumerate(header):
            col = xlsxwriter.utility.xl_col_to_name(idx)
            worksheet.write('{}1'.format(col.upper()),
                            field, header_format)
        start = 1

    # Iterate over the data and write it out row by row.
    for ridx, row in enumerate(rows, start):
        for idx, field in enumerate(row):
            worksheet.write(ridx, idx, field)

    workbook.close()