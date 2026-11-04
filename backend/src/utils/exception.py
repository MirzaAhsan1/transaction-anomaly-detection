import sys  # Ye hume runtime ki information deta hai

def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()
    # exc_info() returns three values that represent the exception type, exception value, and traceback object. We are only interested in the traceback object here.
    file_name = exc_tb.tb_frame.f_code.co_filename  # Ye hume file ka name deta hai jahan error hua hai
    line_number = exc_tb.tb_lineno  # Ye hume line number deta hai jahan error hua hai 
    