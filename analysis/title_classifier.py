def detect_model(title):
    t = title.lower().replace(" ", "")

    if "iphone14" in t:
        return "iphone14"
    if "iphone13" in t:
        return "iphone13"
    if "iphone12" in t:
        return "iphone12"
    if "iphone11" in t:
        return "iphone11"

    return None


def detect_damage(title):
    t = title.lower()

    if "カメラガラス" in t or "カメラ ガラス" in t:
        return "camera_glass"

    if "カメラ" in t:
        return "camera"

    if "バッテリー" in t or "電池" in t:
        return "battery"

    if "画面" in t or "液晶" in t or "割れ" in t or "表示不良" in t or "タッチ不良" in t:
        return "screen"

    return "unknown"
