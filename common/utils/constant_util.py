# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: constant_util.py
# @Software: PyCharm
# @Desc : 工具类

# from core.env import DataBaseConfig


class CommonConstant:
    """通用常量"""
    WWW = "www."
    HTTP = "http://"
    HTTPS = "https://"

    LOOKUP_RMI = "rmi:"
    LOOKUP_LDAP = "ldap:"
    LOOKUP_LDAPS = "ldaps:"

    YES = "Y"
    NO = "N"

    DEPT_NORMAL = "0"
    DEPT_DISABLE = "1"

    UNIQUE = True
    NOT_UNIQUE = False


class HttpStatusConstant:
    """HTTP 响应状态码"""
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    MOVED_PERM = 301
    SEE_OTHER = 303
    NOT_MODIFIED = 304

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    BAD_METHOD = 405
    CONFLICT = 409
    UNSUPPORTED_TYPE = 415

    ERROR = 500
    NOT_IMPLEMENTED = 501
    WARN = 601


class JobConstant:
    """定时任务常量"""
    JOB_ERROR_LIST = [
        "app", "config", "exceptions", "import ",
        "middlewares", "module_admin", "open(", "os.",
        "server", "sub_applications", "subprocess.", "sys.",
        "utils", "while ", "__import__",
        '"', "'", ",", "?", ":", ";", "/", "|",
        "+", "-", "=", "~", "!", "#", "$", "%", "^", "&", "*",
        "<", ">", "(", ")", "[", "]", "{", "}", " "
    ]
    JOB_WHITE_LIST = ["module_task"]


class MenuConstant:
    """菜单常量"""
    TYPE_DIR = "M"
    TYPE_MENU = "C"
    TYPE_BUTTON = "F"

    YES_FRAME = 0
    NO_FRAME = 1

    LAYOUT = "Layout"
    PARENT_VIEW = "ParentView"
    INNER_LINK = "InnerLink"


class GenConstant:
    """代码生成器常量"""
    TPL_CRUD = "crud"
    TPL_TREE = "tree"
    TPL_SUB = "sub"

    TREE_CODE = "treeCode"
    TREE_PARENT_CODE = "treeParentCode"
    TREE_NAME = "treeName"

    PARENT_MENU_ID = "parentMenuId"
    PARENT_MENU_NAME = "parentMenuName"

    COLUMNNAME_NOT_ADD_SHOW = ["create_by", "create_time"]
    COLUMNNAME_NOT_EDIT_SHOW = ["update_by", "update_time"]
    COLUMNNAME_NOT_EDIT = ["id", "create_by", "create_time", "del_flag"]
    COLUMNNAME_NOT_LIST = ["id", "create_by", "create_time", "del_flag", "update_by", "update_time"]
    COLUMNNAME_NOT_QUERY = ["id", "create_by", "create_time", "del_flag", "update_by", "update_time", "remark"]

    BASE_ENTITY = ["createBy", "createTime", "updateBy", "updateTime", "remark"]
    TREE_ENTITY = ["parentName", "parentId", "orderNum", "ancestors", "children"]

    HTML_INPUT = "input"
    HTML_TEXTAREA = "textarea"
    HTML_SELECT = "select"
    HTML_RADIO = "radio"
    HTML_CHECKBOX = "checkbox"
    HTML_DATETIME = "datetime"
    HTML_IMAGE_UPLOAD = "imageUpload"
    HTML_FILE_UPLOAD = "fileUpload"
    HTML_EDITOR = "editor"

    TYPE_DECIMAL = "Decimal"
    TYPE_DATE = ["date", "time", "datetime"]

    QUERY_LIKE = "LIKE"
    QUERY_EQ = "EQ"
    REQUIRE = "1"



    # 通用数值类型
    COLUMNTYPE_NUMBER = [
        "tinyint", "smallint", "mediumint", "int", "integer",
        "bigint", "float", "double", "decimal", "number"
    ]


class UploadSettings:
    """
    上传配置
    """

    UPLOAD_PREFIX = '/profile'
    UPLOAD_PATH = 'static'
    UPLOAD_MACHINE = 'A'
    MAX_FILE_SIZE = 4096000
    DEFAULT_ALLOWED_EXTENSION = [
        # 图片
        'bmp',
        'gif',
        'jpg',
        'jpeg',
        'png',
        # word excel powerpoint
        'doc',
        'docx',
        'xls',
        'xlsx',
        'ppt',
        'pptx',
        'html',
        'htm',
        'txt',
        # 压缩文件
        'rar',
        'zip',
        'gz',
        'bz2',
        # 视频格式
        'mp4',
        'avi',
        'rmvb',
        # pdf
        'pdf',
    ]
    DOWNLOAD_PATH = 'static/download'
