def get_index(x, y):
    def get_i(num):
        if 0 <= num < 0.33:
            return 0
        elif 0.33 <= num < 0.66:
            return 1
        elif 0.66 <= num <= 1:
            return 2

    # 结界图片偏移
    _offset_x = -94
    _offset_y = -93
    _w = 626
    _h = 249

    _rate_x = round((x + _offset_x) / _w, 3)
    _rate_y = round((y + _offset_y) / _h, 3)
    print(f"{x},{y} = ", end="")
    return get_i(_rate_x) + get_i(_rate_y) * 3


print(get_index(465, 105))
