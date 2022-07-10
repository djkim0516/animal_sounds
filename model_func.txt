from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment
from openpyxl.styles import Font
from openpyxl.styles.borders import Border, Side
import numpy as np
import time


def classification(file_id='abcd', audio_file='abcd.wav', is_file_label=True):
    """
    :param file_id: File id
    :param audio_file: Audio file name
    :param is_file_label: whether to write a file info table
    """

    """Model Loading and Classification"""

    # Test results
    classification_results = np.array([[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                                        0.1, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]])
    period_info = np.array([[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]])



    """File writing"""

    wb = Workbook()

    sheet1 = wb.active
    sheet1.title = 'Classification Report'

    y_color = PatternFill(start_color='ffff00', end_color='ffff00', fill_type='solid')

    # Writing a file info table
    if is_file_label:
        sheet1.cell(row=1, column=1).value = '파일ID'
        sheet1.cell(row=1, column=1).fill = y_color
        sheet1.cell(row=1, column=1).alignment = Alignment(horizontal='center')
        sheet1.cell(row=1, column=2).value = '파일명'
        sheet1.cell(row=1, column=2).fill = y_color
        sheet1.cell(row=1, column=2).alignment = Alignment(horizontal='center')

        sheet1.cell(row=2, column=1).value = file_id
        sheet1.cell(row=2, column=1).alignment = Alignment(horizontal='center')
        sheet1.cell(row=2, column=2).value = audio_file
        sheet1.cell(row=2, column=2).alignment = Alignment(horizontal='center')
        sheet1.merge_cells('E2:AB2')
        sheet1['E2'] = '확률값'

        p_color = PatternFill(start_color='ffEB9C', end_color='ffEB9C', fill_type='solid')
        ft = Font(color="FF0000")
        sheet1['E2'].fill = p_color
        sheet1['E2'].font = ft
        sheet1['E2'].alignment = Alignment(horizontal='center')

        start_row = 3
    else:
        start_row = 1

    # Making column labels
    label = ['일련번호', 'class', '시작 시간(시:분:초)', '종료 시간(시:분:초)']
    class_number = 24
    for i in range(1, class_number+1):
        label.append('Class%d' % i)

    # Making column labels
    for i in range(len(label)):
        sheet1.cell(row=start_row, column=(i + 1)).value = label[i]
        sheet1.cell(row=start_row, column=(i + 1)).fill = y_color
        sheet1.cell(row=start_row, column=(i + 1)).alignment = Alignment(horizontal='center')

    # Setting column widths
    sheet1.column_dimensions['B'].width = 16
    sheet1.column_dimensions['C'].width = 18
    sheet1.column_dimensions['D'].width = 18

    # Writing results
    current_row = start_row+1

    for i in range(np.shape(classification_results)[0]):
        if np.argmax(classification_results[i]) == 7:
            sheet1.cell(row=current_row, column=1).value = current_row - start_row
            sheet1.cell(row=current_row, column=1).alignment = Alignment(horizontal='center')

            sheet1.cell(row=current_row, column=2).value = np.argmax(classification_results[i])
            sheet1.cell(row=current_row, column=2).alignment = Alignment(horizontal='center')

            sheet1.cell(row=current_row, column=3).value = time.strftime('%H:%M:%S', time.gmtime(period_info[i, 0]))
            sheet1.cell(row=current_row, column=3).alignment = Alignment(horizontal='center')

            sheet1.cell(row=current_row, column=4).value = time.strftime('%H:%M:%S', time.gmtime(period_info[i, 1]))
            sheet1.cell(row=current_row, column=4).alignment = Alignment(horizontal='center')

            for k in range(class_number):
                sheet1.cell(row=current_row, column=(5+k)).value = classification_results[i, k]
                sheet1.cell(row=current_row, column=(5+k)).alignment = Alignment(horizontal='center')

            current_row = current_row + 1

    wb.save(filename='test.xlsx')
    return


if __name__ == "__main__":
    classification()

