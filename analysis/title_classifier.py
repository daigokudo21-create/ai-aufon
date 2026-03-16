def detect_model(title):
    t = title.lower().replace(" ", "").replace("-", "")

    # SE
    if "iphonese3" in t or "iphonese(第3世代)" in t or "iphonese第3世代" in t:
        return "iphone se3"

    if "iphonese2" in t or "iphonese(第2世代)" in t or "iphonese第2世代" in t:
        return "iphone se2"

    # 12系
    if "iphone12promax" in t:
        return "iphone 12 pro max"
    if "iphone12pro" in t:
        return "iphone 12 pro"
    if "iphone12mini" in t:
        return "iphone 12 mini"
    if "iphone12" in t:
        return "iphone 12"

    # 11系
    if "iphone11promax" in t:
        return "iphone 11 pro max"
    if "iphone11pro" in t:
        return "iphone 11 pro"
    if "iphone11" in t:
        return "iphone 11"

    # X系
    if "iphonexsmax" in t:
        return "iphone xs max"
    if "iphonexs" in t:
        return "iphone xs"
    if "iphonexr" in t:
        return "iphone xr"
    if "iphonex" in t:
        return "iphone x"

    # その他も拾う
    if "iphone13promax" in t:
        return "iphone 13 pro max"
    if "iphone13pro" in t:
        return "iphone 13 pro"
    if "iphone13mini" in t:
        return "iphone 13 mini"
    if "iphone13" in t:
        return "iphone 13"

    if "iphone14promax" in t:
        return "iphone 14 pro max"
    if "iphone14pro" in t:
        return "iphone 14 pro"
    if "iphone14plus" in t:
        return "iphone 14 plus"
    if "iphone14" in t:
        return "iphone 14"

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
