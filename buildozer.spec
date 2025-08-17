[app]
title = Snake
package.name = snake
package.domain = com.example
source.dir = .
source.include_exts = py,kv,png,ttf,txt
version = 0.1.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
# برای عبور از گیر لایسنس‌ها در CI:
android.accept_sdk_license = True

# API هدف را روی 35 بگذار تا با قوانین جدید پلی‌استور سازگار باشد،
# و از Build-Tools 36 که هنوز همه‌جا آماده نیست اجتناب کنی.
android.api = 35
android.minapi = 24
# معمولاً NDK را خالی بگذار تا p4a نسخه توصیه‌شده را بگیرد.
# android.ndk =

# اگر آیکون/پرمیشن خاصی نداری، همین‌ها کافی است.
# android.permissions =

