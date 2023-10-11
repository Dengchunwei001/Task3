import tkinter as tk


class LineDrawer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("画线段")

        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()  # 将画布放置到主窗口中，使其可见

        self.start_point = None
        self.line_color = "red"

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.root.mainloop()

    def on_left_click(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
        else:
            end_point = (event.x, event.y)
            self.draw_line_bresenham(self.start_point, end_point)
            #  draw_line_bresenham 自带划线函数
            self.start_point = None
            # 事件结束设置起始点为空，以便下次运行

    def on_right_click(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
        else:
            end_point = (event.x, event.y)
            self.draw_line_wu(self.start_point, end_point)
            self.start_point = None

    def put_pixel(self, x, y, color):
        #self.create_line(x, y, x+1, y+1,  fill=color, outline=color)
        self.canvas.create_rectangle(x, y, x + 1, y , fill=color)
        # 线段粗细

        # Bresenham算法的实现

    def draw_line_bresenham(self, p1, p2):
        x1, y1 = p1  # 提取起始点的坐标
        x2, y2 = p2  # 提取终止点的坐标

        dx = abs(x2 - x1)  # 计算x方向上的位移
        dy = abs(y2 - y1)  # 计算y方向上的位移
        delx = 1 if x2 > x1 else -1  # x方向的增量，1表示增加，-1表示减少
        dely = 1 if y2 > y1 else -1  # y方向的增量，1表示增加，-1表示减少
        error = dx - dy  # 误差的初始值，用于决定下一个像素点的位置
        x, y = x1, y1  # 初始化当前像素点的坐标为起始点

        while x != x2 or y != y2:  # 循环绘制线段，直到达到终止点
            self.put_pixel(x, y, self.line_color)  # 在当前像素点上绘制点
            error2 = error *2 # 误差的两倍值

            if error2 > -dy:  # 如果误差的两倍值大于负的y方向位移
                error -= dy  # 减去y方向的位移
                x += delx  # 增加x方向的位移

            if error2 < dx:  # 如果误差的两倍值小于x方向的位移
                error += dx  # 增加x方向的位移
                y += dely  # 增加y方向的位移

    # VU算法
    def draw_line_wu(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = abs(x2 - x1)  # 计算x方向上的位移
        dy = abs(y2 - y1)  # 计算y方向上的位移

        if dx > dy:  # 如果x方向的位移大于y方向的位移
            if x1 > x2:
                x1, x2, y1, y2 = x2, x1, y2, y1  # 确保x1是较小的x坐标
            gradient = dy / (dx)  # 计算斜率，用于渐变颜色
            xend = round(x1)  # 将x1四舍五入为整数
            yend = y1 + gradient * (xend - x1)  # 计算y结束坐标
            xpxl1 = xend  # 第一个x像素
            ypxl1 = int(yend)  # 第一个y像素
            self.put_pixel(xpxl1, ypxl1, self.line_color)  # 在第一个像素上绘制点
            self.put_pixel(xpxl1, ypxl1 + 1, self.line_color)  # 在下一个像素上绘制点
            intery = yend + gradient  # 初始化y插值

            xend = round(x2)  # 计算x结束坐标
            yend = y2 + gradient * (xend - x2)  # 计算y结束坐标
            xpxl2 = xend  # 最后一个x像素
            ypxl2 = int(yend)  # 最后一个y像素
            self.put_pixel(xpxl2, ypxl2, self.line_color)  # 在最后一个像素上绘制点
            self.put_pixel(xpxl2, ypxl2 + 1, self.line_color)  # 在下一个像素上绘制点

            for x in range(int(xpxl1 + 1), int(xpxl2)):  # 遍历x像素
                self.put_pixel(x, int(intery), self.line_color)  # 在当前像素上绘制点
                self.put_pixel(x, int(intery) + 1, self.line_color)  # 在下一个像素上绘制点
                intery += gradient  # 更新y插值
        else:  # 如果y方向的位移大于x方向的位移
            if y1 > y2:
                x1, x2, y1, y2 = x2, x1, y2, y1  # 确保y1是较小的y坐标
            gradient = dx / dy  # 计算斜率，用于渐变颜色
            yend = round(y1)  # 计算y结束坐标
            xend = x1 + gradient * (yend - y1)  # 计算x结束坐标
            ypxl1 = yend  # 第一个y像素
            xpxl1 = int(xend)  # 第一个x像素
            self.put_pixel(xpxl1, ypxl1, self.line_color)  # 在第一个像素上绘制点
            self.put_pixel(xpxl1, ypxl1 + 1, self.line_color)  # 在下一个像素上绘制点
            interx = xend + gradient  # 初始化x插值

            yend = round(y2)  # 计算y结束坐标
            xend = x2 + gradient * (yend - y2)  # 计算x结束坐标
            ypxl2 = yend  # 最后一个y像素
            xpxl2 = int(xend)  # 最后一个x像素
            self.put_pixel(xpxl2, ypxl2, self.line_color)  # 在最后一个像素上绘制点
            self.put_pixel(xpxl2, ypxl2 + 1, self.line_color)  # 在下一个像素上绘制点

            for y in range(int(ypxl1 + 1), int(ypxl2)):  # 遍历y像素
                self.put_pixel(int(interx), y, self.line_color)  # 在当前像素上绘制点
                self.put_pixel(int(interx) + 1, y, self.line_color)  # 在下一个像素上绘制点
                interx += gradient  # 更新x插值


if __name__ == "__main__":
    ld = LineDrawer()
