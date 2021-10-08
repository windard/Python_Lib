# -*- coding: utf-8 -*-

import cv2

if __name__ == '__main__':
    img = cv2.imread("NationalHoliday/10-01.png")
    img = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    cv2.imshow("Extend Border Image", img)

    key = cv2.waitKey(0)
    # 按 q 键则直接退出
    if key == 27:
        cv2.destroyAllWindows()
    # 按 s 键则保存退出
    elif key == ord('s'):
        cv2.imwrite("extend_border.png", img)
        cv2.destroyAllWindows()
