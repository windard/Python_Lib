# -*- coding: utf-8 -*-
import funcy as fc

if __name__ == '__main__':
    a = [1,3,4,5,2,5,1,5,2,5,1]
    print(fc.distinct(a))
    print(set(a))

    # 按个数分组,舍弃多余的元素
    print(fc.partition(2, range(10)))
    print(fc.partition(3, range(10)))
    # 按个数分组,多余的元素单列
    print(fc.chunks(2, range(10)))
    print(fc.chunks(3, range(10)))

    # 此处不能用 lstrip 或者 rstrip, 因为会将输入字符串当成字符数组
    print("open_api_enforce_interface".lstrip("open_api"))
    print("open_api_enforce_interface".rstrip("_interface"))
    print(fc.cut_prefix("open_api_test_interface", "open_api"))
    print(fc.cut_suffix("open_api_test_interface", "interface"))
