import traceback #
import sys

# #when you run a file with print(10/0) you would recevie Traceback error


# class CustomException(Exception): #inherit from python libary
#     #we need pre-defined expceptions from that libary + we fill define our own custom expections

#     def __init__(self,error_message, error_detail:sys):
#         super().__init__(error_message) #for inheriting. if this exception alreday comes from here, if not we will use ours
#         self.error_message = self.get_detailed_error_message(error_message, error_detail)

#     @staticmethod # we dont need to create custom exception lass again and again to show our custom exception
#     #with help of this method our functions and our methods becaome independent of class creation 
#     def get_detailed_error_message(error_message, error_detail:sys):

#         _,_,exc_tb= error_detail.exc_info()
#         file_name = exc_tb.tb_frame.f_code.co_filename
#         line_number = exc_tb.tb_lineno 

#         return f"Error in {file_name}, line {line_number} : {error_message}"
    
#     def __str__(self): #str gives you a exact representation of your error message whereever you will do str(e)
#         return self.error_message
    


import sys
import traceback  # şimdilik kullanmasan da durabilir

class CustomException(Exception):
    """
    Projede detaylı hata mesajı üretmek için kullanılan özel exception sınıfı.
    """

    def __init__(self, error_message, error_detail: object = None):
        # error_detail'ı artık kullanmayacağız ama
        # fonksiyon imzasında kalsın ki diğer dosyalar bozulmasın
        super().__init__(str(error_message))
        self.error_message = self.get_detailed_error_message(error_message)

    @staticmethod
    def get_detailed_error_message(error_message):
        """
        sys.exc_info() ile traceback bilgisini alıyoruz.
        """
        _, _, exc_tb = sys.exc_info()

        # Bazen CustomException manuel raise edilirse exc_tb None olabilir
        if exc_tb is None:
            return str(error_message)

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return f"Error in {file_name}, line {line_number}: {error_message}"

    def __str__(self):
        return self.error_message