# -*- coding: utf-8 -*-

import cv2

if __name__ == '__main__':
    file_path = ["NationalHoliday/10-01.png", "NationalHoliday/10-02.png", "NationalHoliday/10-03.png"]
    img = cv2.vconcat(list(map(cv2.imread, file_path)))
    cv2.imshow("Joint Image", img)
    key = cv2.waitKey(0)

    # 按 q 键则直接退出
    if key == 27:
        cv2.destroyAllWindows()
    # 按 s 键则保存退出
    elif key == ord('s'):
        cv2.imwrite("horizontal_joint.png", img)
        cv2.destroyAllWindows()
