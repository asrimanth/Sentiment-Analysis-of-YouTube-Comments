"""Contains many errors which are to be handled in the UI modules.
"""
class InvalidURLException(Exception):
    
    def __init__(self, message):
        """Raised when the url by the user is wrong.

        Arguments:
            message {str} -- A message indicating the most possible cause of error.
        """
        if(message is None):
            message = "An unknown error. The video might have been taken down."

