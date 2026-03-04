"""小红书页面 CSS 选择器常量。

所有 CSS 选择器集中管理，当小红书网页改版时只需修改此文件。
各模块通过 `from .selectors import XXX` 引用选择器。
"""

# ========== 登录 ==========
LOGIN_STATUS = ".main-container .user .link-wrapper .channel"
QRCODE_IMG = ".login-container .qrcode-img"

# ========== 首页 / 搜索 ==========
FILTER_BUTTON = "div.filter"
FILTER_PANEL = "div.filter-panel"

# ========== Feed 详情 ==========
COMMENTS_CONTAINER = ".comments-container"
PARENT_COMMENT = ".parent-comment"
NO_COMMENTS_TEXT = ".no-comments-text"
END_CONTAINER = ".end-container"
TOTAL_COMMENT = ".comments-container .total"
SHOW_MORE_BUTTON = ".show-more"
NOTE_SCROLLER = ".note-scroller"
INTERACTION_CONTAINER = ".interaction-container"

# 页面不可访问容器
ACCESS_ERROR_WRAPPER = ".access-wrapper, .error-wrapper, .not-found-wrapper, .blocked-wrapper"

# ========== 评论输入 ==========
COMMENT_INPUT_TRIGGER = "div.input-box div.content-edit span"
COMMENT_INPUT_FIELD = "div.input-box div.content-edit p.content-input"
COMMENT_SUBMIT_BUTTON = "div.bottom button.submit"
REPLY_BUTTON = ".right .interactions .reply"

# 评论查找（兼容多种评论容器结构）
COMMENT_VARIANTS = ".parent-comment, .comment-item, .comment"

# ========== 点赞 / 收藏 ==========
LIKE_BUTTON = ".interact-container .left .like-lottie"
COLLECT_BUTTON = ".interact-container .left .reds-icon.collect-icon"

# ========== 发布页 ==========
UPLOAD_CONTENT = "div.upload-content"
CREATOR_TAB = "div.creator-tab"
CREATOR_TAB_TITLE = "span.title"
UPLOAD_INPUT = ".upload-input"
FILE_INPUT = 'input[type="file"]'
TITLE_INPUT = "div.d-input input"
CONTENT_EDITOR = "div.ql-editor"
CONTENT_TEXTBOX = "[role='textbox']"
IMAGE_PREVIEW = ".img-preview-area .pr"
PUBLISH_BUTTON = ".publish-page-publish-btn button.bg-red"

# 标题/正文长度校验
TITLE_MAX_SUFFIX = "div.title-container div.max_suffix"
CONTENT_LENGTH_ERROR = "div.edit-container div.length-error"

# 可见范围
VISIBILITY_DROPDOWN = "div.permission-card-wrapper div.d-select-content"
VISIBILITY_OPTIONS = "div.d-options-wrapper div.d-grid-item div.custom-option"

# 定时发布
SCHEDULE_SWITCH = ".post-time-wrapper .d-switch"
DATETIME_INPUT = ".date-picker-container input"

# 原创声明
ORIGINAL_SWITCH_CARD = "div.custom-switch-card"
ORIGINAL_SWITCH = "div.d-switch"
CHECKBOX_INPUT = 'input[type="checkbox"]'
D_CHECKBOX_INPUT = 'div.d-checkbox input[type="checkbox"]'

# 通用按钮 / 弹窗
CUSTOM_BUTTON = "button.custom-button"
DIALOG_FOOTER = "div.footer"
POPOVER = "div.d-popover"

# 标签联想
TAG_TOPIC_CONTAINER = "#creator-editor-topic-container"
TAG_FIRST_ITEM = ".item"

# ========== 写长文模式 ==========
# 注意: 长文模式的按钮（写长文、新的创作、一键排版、下一步）通过文本匹配定位
LONG_ARTICLE_TAB_TEXT = "写长文"
NEW_CREATION_BUTTON_TEXT = "新的创作"
AUTO_FORMAT_BUTTON_TEXT = "一键排版"
NEXT_STEP_BUTTON_TEXT = "下一步"

LONG_ARTICLE_TITLE = 'textarea.d-text[placeholder="输入标题"]'
TEMPLATE_CARD = ".template-card"
TEMPLATE_TITLE = ".template-card .template-title"

# ========== 用户主页 ==========
SIDEBAR_PROFILE = "div.main-container li.user.side-bar-component a.link-wrapper span.channel"
SIDEBAR_PROFILE_LINK = "div.main-container li.user.side-bar-component a.link-wrapper"


# ========== 动态选择器构建 ==========


def make_filter_selector(filters_index: int, tags_index: int) -> str:
    """构建搜索筛选选项的 CSS 选择器。

    Args:
        filters_index: 筛选组序号（nth-child）。
        tags_index: 标签序号（nth-child）。
    """
    return (
        f"div.filter-panel div.filters:nth-child({filters_index}) "
        f"div.tags:nth-child({tags_index})"
    )


def make_comment_id_selector(comment_id: str) -> str:
    """构建评论 ID 选择器。"""
    return f"#comment-{comment_id}"


def make_reply_selector(comment_id: str) -> str:
    """构建评论回复按钮选择器。"""
    return f"#comment-{comment_id} {REPLY_BUTTON}"
