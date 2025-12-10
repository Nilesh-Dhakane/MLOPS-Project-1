import traceback
import sys


import os
import traceback

class CustomException(Exception):

    def __init__(self, error_message: str, error: Exception = None):
        super().__init__(error_message)

        self.error_message = self.get_detailed_error_message(
            error_message, error
        )

    @staticmethod
    def get_detailed_error_message(error_message, error: Exception):

        if error is not None:
            tb = error.__traceback__

            if tb is not None:
                filename = os.path.basename(tb.tb_frame.f_code.co_filename)
                line_number = tb.tb_lineno
            else:
                filename = "Unknown File"
                line_number = "Unknown Line"

            original_error = str(error)
        else:
            filename = "Unknown File"
            line_number = "Unknown Line"
            original_error = "No original exception provided"

        return (
            f"Error Occurred in file [{filename}] "
            f"at line [{line_number}]. "
            f"Error Message: {error_message}. "
            f"Original Error: {original_error}"
        )

    def __str__(self):
        return self.error_message
###Correct usage
#     except Exception as e:
#     logger.exception("Error during run process step saving processed data step..")
#     raise CustomException("Error while run processed data", e)


# class CustomException(Exception):

#     def __init__(self, error_message, error_details:sys):
#         super().__init__(error_message)
#         self.error_message = self.get_detailed_error_message(error_message, error_details)

#     @staticmethod
#     def get_detailed_error_message(error_message, error_details:sys):
#         _ , _ , exc_tb = error_details.exc_info()
#         filename = exc_tb.tb_frame.f_code.co_filename
#         line_number = exc_tb.tb_lineno

#         return f"Error Occurred in {filename} line numbers is:={line_number} Error Message: {error_message}"
    
#     def __str__(self):
#         return self.error_message
    