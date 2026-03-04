"""登录管理，对应 Go xiaohongshu/login.go。"""

from __future__ import annotations

import base64
import json
import logging
import os
import tempfile
import time
from dataclasses import dataclass

from .cdp import Page
from .human import sleep_random
from .selectors import LOGIN_STATUS, QRCODE_IMG, SIDEBAR_PROFILE_LINK
from .urls import EXPLORE_URL

logger = logging.getLogger(__name__)


@dataclass
class CurrentUserInfo:
    """当前登录用户信息。"""

    user_id: str = ""
    nickname: str = ""
    red_id: str = ""

    def to_dict(self) -> dict:
        return {
            "userId": self.user_id,
            "nickname": self.nickname,
            "redId": self.red_id,
        }


def check_login_status(page: Page) -> bool:
    """检查登录状态。

    Returns:
        True 已登录，False 未登录。
    """
    page.navigate(EXPLORE_URL)
    page.wait_for_load()
    sleep_random(800, 1500)

    return page.has_element(LOGIN_STATUS)


def fetch_qrcode(page: Page) -> tuple[str, bool]:
    """获取登录二维码。

    Returns:
        (qrcode_src, already_logged_in)
        - 如果已登录，返回 ("", True)
        - 如果未登录，返回 (qrcode_base64_or_url, False)
    """
    page.navigate(EXPLORE_URL)
    page.wait_for_load()
    sleep_random(1500, 2500)

    # 检查是否已登录
    if page.has_element(LOGIN_STATUS):
        return "", True

    # 获取二维码图片 src
    src = page.get_element_attribute(QRCODE_IMG, "src")
    if not src:
        raise RuntimeError("二维码图片 src 为空")

    return src, False


def save_qrcode_to_file(src: str) -> str:
    """将二维码 data URL 保存为临时 PNG 文件。

    Args:
        src: 二维码图片的 data URL（data:image/png;base64,...）或普通 URL。

    Returns:
        保存的文件绝对路径。
    """
    prefix = "data:image/png;base64,"
    if src.startswith(prefix):
        img_data = base64.b64decode(src[len(prefix) :])
    elif src.startswith("data:image/"):
        # 处理其他 MIME 类型，如 data:image/jpeg;base64,...
        _, encoded = src.split(",", 1)
        img_data = base64.b64decode(encoded)
    else:
        # 不是 data URL，无法保存
        raise ValueError(f"不支持的二维码格式，需要 data URL: {src[:50]}...")

    qr_dir = os.path.join(tempfile.gettempdir(), "xhs")
    os.makedirs(qr_dir, exist_ok=True)
    filepath = os.path.join(qr_dir, "login_qrcode.png")

    with open(filepath, "wb") as f:
        f.write(img_data)

    logger.info("二维码已保存: %s", filepath)
    return filepath


def wait_for_login(page: Page, timeout: float = 120.0) -> bool:
    """等待扫码登录完成。

    Args:
        page: CDP 页面对象。
        timeout: 超时时间（秒）。

    Returns:
        True 登录成功，False 超时。
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if page.has_element(LOGIN_STATUS):
            logger.info("登录成功")
            return True
        time.sleep(0.5)
    return False


# JS: 从侧边栏 profile 链接提取 user_id
_EXTRACT_SIDEBAR_USER_ID_JS = f"""
(() => {{
    const link = document.querySelector({json.dumps(SIDEBAR_PROFILE_LINK)});
    if (!link) return null;
    const href = link.getAttribute('href') || '';
    const match = href.match(/\\/user\\/profile\\/([a-f0-9]+)/);
    return match ? match[1] : null;
}})()
"""

# JS: 从用户主页 __INITIAL_STATE__ 提取 basicInfo
_EXTRACT_CURRENT_USER_JS = """
(() => {
    if (window.__INITIAL_STATE__ &&
        window.__INITIAL_STATE__.user &&
        window.__INITIAL_STATE__.user.userPageData) {
        const data = window.__INITIAL_STATE__.user.userPageData;
        const val = data.value !== undefined ? data.value : data._value;
        if (val && val.basicInfo) {
            return JSON.stringify({
                nickname: val.basicInfo.nickname || '',
                redId: val.basicInfo.redId || '',
            });
        }
    }
    return '';
})()
"""


def get_current_user_info(page: Page) -> CurrentUserInfo | None:
    """获取当前登录用户的昵称和小红书号。

    流程：explore 页面侧边栏 → 提取 user_id → 跳转个人主页 → 读取 basicInfo。

    Returns:
        CurrentUserInfo 或 None（未登录/获取失败）。
    """
    # 确保在 explore 页面且已登录
    page.navigate(EXPLORE_URL)
    page.wait_for_load()
    sleep_random(800, 1500)

    if not page.has_element(LOGIN_STATUS):
        return None

    # 从侧边栏链接提取 user_id
    user_id = page.evaluate(_EXTRACT_SIDEBAR_USER_ID_JS)
    if not user_id:
        logger.warning("无法从侧边栏获取 user_id")
        return None

    logger.info("当前用户 ID: %s", user_id)

    # 跳转到个人主页
    profile_url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
    page.navigate(profile_url)
    page.wait_for_load()
    page.wait_dom_stable()

    # 等待 __INITIAL_STATE__
    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline:
        ready = page.evaluate("window.__INITIAL_STATE__ !== undefined")
        if ready:
            break
        time.sleep(0.5)

    # 提取用户信息
    raw = page.evaluate(_EXTRACT_CURRENT_USER_JS)
    if not raw:
        logger.warning("无法从个人主页提取用户信息")
        return CurrentUserInfo(user_id=user_id)

    info = json.loads(raw)
    result = CurrentUserInfo(
        user_id=user_id,
        nickname=info.get("nickname", ""),
        red_id=info.get("redId", ""),
    )
    logger.info("当前用户: %s (红薯号: %s)", result.nickname, result.red_id)
    return result
