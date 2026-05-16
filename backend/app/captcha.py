"""
图形验证码服务模块
"""
import random
import string
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import os


class CaptchaService:
    """图形验证码服务"""

    def __init__(self):
        self.width = 150
        self.height = 50
        self.code_length = 5
        # 简单的字体路径，生产环境应该使用系统字体
        self.font_path = None

    def _generate_code(self) -> str:
        """生成随机验证码"""
        # 使用数字、大写字母和小写字母，去除容易混淆的字符
        chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
        # 去除容易混淆的字符
        exclude = '0O1IlI'
        chars = ''.join(c for c in chars if c not in exclude)
        return ''.join(random.choices(chars, k=self.code_length))

    def _create_image(self, code: str) -> Image.Image:
        """创建验证码图片"""
        # 创建图片
        img = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # 绘制干扰线
        for _ in range(3):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            draw.line([(x1, y1), (x2, y2)], fill=self._random_color(180, 250))

        # 绘制干扰点
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=self._random_color(150, 200))

        # 绘制验证码文字
        font_size = 22
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                # Windows 系统字体
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # 使用默认字体
                font = ImageFont.load_default()

        text_width = font.getlength(code) if hasattr(font, 'getlength') else len(code) * font_size // 2
        start_x = (self.width - text_width) // 2
        start_y = (self.height - font_size) // 2

        for i, char in enumerate(code):
            # 每个字符略微旋转
            x = start_x + i * (font_size + 3)
            y = start_y + random.randint(-3, 3)
            
            # 随机颜色
            color = self._random_color(20, 80)
            draw.text((x, y), char, font=font, fill=color)

        # 添加波浪效果（简化处理）
        # 这里简单添加一些噪点效果
        pixels = img.load()
        for _ in range(50):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pixels[x, y] = self._random_color(100, 200)

        return img

    def _random_color(self, start: int, end: int) -> tuple:
        """生成随机颜色"""
        return (random.randint(start, end),
                random.randint(start, end),
                random.randint(start, end))

    def generate_captcha(self) -> dict:
        """
        生成验证码

        Returns:
            dict: 包含验证码图片base64和验证码key
        """
        code = self._generate_code()
        image = self._create_image(code)

        # 转换为 base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return {
            'code': code,
            'image': f"data:image/png;base64,{img_base64}"
        }


# 全局验证码服务实例
captcha_service = CaptchaService()
