class AppBaseException(Exception):
    """
    AppBaseException are internal exception to propagate errors from source to the parent that handles the error,
    implying all AppBaseException must be resolved with correct user notifications (e.g. error box). And also implies
    these are not bugs, but errors that can also mean the users must resolved the error.
    """

    def __init__(self, *, msg, code=None):
        """
        code keyword arg are integer attributes that must be used within its respective class and its parent class.
        """

        super().__init__(f"[{code}] {msg}")
        self.code = code


class RuntimeAppError(AppBaseException):
    pass


class ProjectFileAppError(AppBaseException):
    PROJ_CREATION_DIR_EXIST = 1
    PROJ_FILE_DOESNT_EXIST = 2
    MDL_ID_GEN_DUPE_NAME = 3
    MDL_NAME_NON_EXISTENT = 4
    MDL_ID_INVALID = 5
    FILE_GEM_INVALID = 6


class ModelExecutionRuntimeError(AppBaseException):
    ERROR = 1


class ModelExecutionError(AppBaseException):
    DEBUG_ERROR = 1


class ModelRuntimeAppError(AppBaseException):
    pass
