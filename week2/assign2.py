"""Assignment - Week 2 Python, 測試資料放在各任務程式碼後面"""

# ============================================================
# Task 1
# 1. 先把地圖上的角色整理成座標。
# 2. 每兩個角色之間的移動距離用「水平距離 + 垂直距離」計算。
# 3. 如果移動時需要到斜線另一側，再把距離加 2。
# 4. 對指定角色逐一計算到其他角色的距離。
# 5. 找出最大距離與最小距離，若有並列就全部印出。
# ============================================================

MAP_POINTS = {                                                                  # 建立地圖角色資料
    "辛巴": {"x": -3, "y": 3, "side": "left"},                                # 辛巴的座標與斜線側邊
    "丁滿": {"x": -1, "y": 4, "side": "right"},
    "貝吉塔": {"x": -4, "y": -1, "side": "left"},
    "悟空": {"x": 0, "y": 0, "side": "left"},
    "特南克斯": {"x": 1, "y": -2, "side": "left"},
    "弗利沙": {"x": 4, "y": -1, "side": "right"},
}


def format_names(names):                                                        # 定義名稱格式化函式
    return "、".join(names)                                                      # 用頓號連接多個角色名稱


def calculate_distance(start, end):                                             # 定義距離計算函式
    start_point = MAP_POINTS[start]                                             # 取得起點角色資料
    end_point = MAP_POINTS[end]                                                 # 取得終點角色資料
    distance = (                                                                # 計算水平距離加垂直距離
        abs(start_point["x"] - end_point["x"])
        + abs(start_point["y"] - end_point["y"])
    )                                                                           # 距離計算結束(距離=x座標差的abs+y座標差的abs)不能走斜
    if start_point["side"] != end_point["side"]:                                # 判斷是否跨越斜線另一側
        distance += 2                                                           # 跨越斜線時額外加 2
    return distance                                                             # 回傳最後距離


def func1(name):                                                                # Task 1 主函式
    distances = {}                                                              # 建立距離字典
    for person in MAP_POINTS:                                                   # 逐一檢查所有角色
        if person != name:                                                      # 排除自己
            distances[person] = calculate_distance(name, person)                # 計算指定角色到其他角色的距離

    farthest_distance = max(distances.values())                                 # 找出最大距離
    closest_distance = min(distances.values())                                  # 找出最小距離
    farthest = [                                                                # 建立最遠角色清單
        person                                                                  # 保留角色名稱
        for person, distance in distances.items()                               # 逐一讀取角色與距離
        if distance == farthest_distance                                        # 只保留最大距離角色
    ]
    closest = [                                                                 # 建立最近角色清單
        person                                                                  # 保留角色名稱
        for person, distance in distances.items()                               # 逐一讀取角色與距離
        if distance == closest_distance                                         # 只保留最小距離角色
    ]
    print("最遠" + format_names(farthest) + "；最近" + format_names(closest))    # 印出最遠與最近角色



func1("辛巴")                                                                   # print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空")                                                                   # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙")                                                                 # print 最遠辛巴；最近特南克斯
func1("特南克斯")                                                               # print 最遠丁滿；最近悟空



# ============================================================
# Task 2
# 1. 每次預約都按照呼叫順序處理，因為先預約成功的人會占用服務時段。
# 2. 用 bookings 字典記錄每個服務已被預約的時間。
# 3. 解析 criteria，分成欄位 field、運算符號 operator 和 value 值。
# 4. 先排除和現有預約重疊的服務。
# 5. 再排除不符合 criteria 的服務。
# 6. 若 criteria 是 >=，選符合條件中數值最小的服務。
# 7. 若 criteria 是 <=，選符合條件中數值最大的服務。
# 8. 若 criteria 是 =，選欄位值相等的服務。
# 9. 找到服務就印出名稱並記錄預約，否則印出 Sorry。
# ============================================================

bookings = {}                                                                   # 建立預約紀錄字典


def parse_criteria(criteria):                                                   # 定義條件解析函式
    if ">=" in criteria:                                                        # 判斷條件是否為大於等於
        field, value = criteria.split(">=")                                     # 拆出欄位名稱與條件值
                                                                                # field 可以代入 c(cost), r(rating), name
        return field, ">=", float(value)                                        # 回傳解析後的大於等於條件
    if "<=" in criteria:                                                        # 判斷條件是否為小於等於
        field, value = criteria.split("<=")                                     # 拆出欄位名稱與條件值
        return field, "<=", float(value)                                        # 回傳解析後的小於等於條件
    field, value = criteria.split("=")                                          # 拆出等於條件的欄位名稱與條件值
    return field, "=", value                                                    # 回傳解析後的等於條件


def has_overlap(service_name, start, end):                                      # 定義預約重疊檢查函式
    for booked_start, booked_end in bookings.get(service_name, []):             # 逐一讀取該服務已預約時段
        if start < booked_end and end > booked_start:                           # 判斷新時段是否與舊時段重疊
            return True                                                         # 有重疊就回傳 True(衝突)
    return False                                                                # 沒有重疊就回傳 False


def match_criteria(service, field, operator, value):                            # 定義條件比對函式
    if operator == "=":                                                         # 判斷是否為等於條件, operator 是運算符號
        return str(service[field]) == str(value)                                # 比較欄位值是否相同
    if operator == ">=":                                                        # 判斷是否為大於等於條件
        return service[field] >= value                                          # 比較欄位值是否大於等於條件值
    return service[field] <= value                                              # 比較欄位值是否小於等於條件值


def pick_best_service(candidates, field, operator):                             # 定義最佳服務選擇函式
    if operator == ">=":                                                        # 如果條件是大於等於
        return min(candidates, key=lambda service: service[field])              # 選符合條件中欄位值最小的服務
    if operator == "<=":                                                        # 如果條件是小於等於
        return max(candidates, key=lambda service: service[field])              # 選符合條件中欄位值最大的服務
    return candidates[0]                                                        # 等於條件直接選第一個符合的服務


def func2(ss, start, end, criteria):                                            # Task 2 主函式
    field, operator, value = parse_criteria(criteria)                           # 解析條件字串
    candidates = []                                                             # 建立候選服務清單
    for service in ss:                                                          # 逐一檢查服務
        if has_overlap(service["name"], start, end):                            # 判斷服務時段是否重疊
            continue                                                            # 重疊就跳過該服務
        if match_criteria(service, field, operator, value):                     # 判斷服務是否符合條件
            candidates.append(service)                                          # 符合就加入候選清單

    if len(candidates) == 0:                                                    # 判斷是否沒有候選服務
        print("Sorry")                                                          # 沒有服務可預約就印出 Sorry
        return

    best_service = pick_best_service(candidates, field, operator)               # 選出最佳服務
    bookings.setdefault(best_service["name"], []).append((start, end))          # 記錄成功預約時段
    print(best_service["name"])                                                 # 印出服務名稱



services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800},
]

func2(services, 15, 17, "c>=800")                                               # S3
func2(services, 11, 13, "r<=4")                                                 # S3
func2(services, 10, 12, "name=S3")                                              # Sorry
func2(services, 15, 18, "r>=4.5")                                               # S1
func2(services, 16, 18, "r>=4")                                                 # Sorry
func2(services, 13, 17, "name=S1")                                              # Sorry
func2(services, 8, 9, "c<=1500")                                                # S2



# ============================================================
# Task 3
# 1. 每一步的差值會重複出現：-2、-3、+1、+2。
# 2. answer 從 25 開始。for 迴圈搭配 range, 比如 range(stop)的話, stop 不包含在內。
# 3. index 代表從第 0 項 也就是 25 往後走幾步。i 是每一輪迴圈的索引值, for 迴圈依序自動賦值。
# 4. i = 0, answer += changes[0 % 4] 就是取 0 除以 4 的餘數 # changes[0] = -2, 依次帶入 i 。
# 5. 把差值依序加 index 次，就能得到答案。
# 6. 印出最後算出的數字。
# ============================================================

def func3(index):                                                               # Task 3 主函式
    changes = [-2, -3, 1, 2]                                                    # 建立循環變化量
    answer = 25                                                                 # 設定第 0 項為 25
    for i in range(index):                                                      # 依照 index 次數逐步計算
        answer += changes[i % len(changes)]                                     # 加上對應的循環變化量
    print(answer)                                                               # 印出答案



func3(1)                                                                        # print 23
func3(5)                                                                        # print 21
func3(10)                                                                       # print 16
func3(30)                                                                       # print 6



# ============================================================
# Task 4
# 1. sp 是每節車廂的空位數。
# 2. stat 是狀態字串，0 代表該車廂現在可以服務。
# 3. 只檢查 stat 為 0 的車廂。
# 4. 選出空位數和乘客數差距最小的車廂。
# 5. 如果差距一樣，保留比較早出現的車廂。
# 6. 印出最適合車廂的 index。
# ============================================================

def func4(sp, stat, n):                                                         # Task 4 主函式 sp空位數 stat狀態 n乘客
    best_index = -1                                                             # 設定預設車廂 index
    best_difference = None                                                      # 設定目前最佳差距, 先為空值

    for i in range(len(sp)):                                                    # 逐一檢查每節車廂
        if stat[i] != "0":                                                      # 判斷車廂是否不能服務, 如果是0才能繼續, 1就跳過換下一個
            continue

        difference = abs(sp[i] - n)                                             # 計算空位數和乘客數差距, abs是絕對值
        if best_difference is None or difference < best_difference:             # 判斷是否為目前最適合車廂
            best_difference = difference                                        # 更新最佳差距 difference 代入 best_difference
            best_index = i                                                      # 更新最佳車廂 index

    print(best_index)                                                           # 印出最佳車廂 index



func4([3, 1, 5, 4, 3, 2], "101000", 2)                                          # print 5
func4([1, 0, 5, 1, 3], "10100", 4)                                              # print 4
func4([4, 6, 5, 8], "1000", 4)                                                  # print 2
