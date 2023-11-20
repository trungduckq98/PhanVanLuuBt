import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Tạo các biến để lưu trữ hình ảnh gốc và hình ảnh đang xử lý
        self.original_image = None
        self.processed_image = None

        # Tạo các biến độ sáng và độ bão hòa màu mặc định
        self.brightness_factor = tk.DoubleVar(value=1.0)
        self.saturation_factor = tk.DoubleVar(value=1.0)
        self.zoom_factor = tk.DoubleVar(value=1.0)

        # Tạo thanh trượt để điều chỉnh độ sáng
        brightness_slider = tk.Scale(self.root, label="Brightness", from_=0.1, to=3.0, resolution=0.1,
                                     orient=tk.HORIZONTAL, variable=self.brightness_factor, command=self.process_image)
        brightness_slider.pack(pady=10)

        # Tạo thanh trượt để điều chỉnh độ bão hòa màu
        saturation_slider = tk.Scale(self.root, label="Saturation", from_=0.1, to=3.0, resolution=0.1,
                                     orient=tk.HORIZONTAL, variable=self.saturation_factor, command=self.process_image)
        saturation_slider.pack(pady=10)

        # Tạo nút để mở hình ảnh từ tệp tin
        open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        open_button.pack(pady=10)

        # Tạo Frame để chứa nút Zoom In và Zoom Out
        zoom_frame = tk.Frame(self.root)
        zoom_frame.pack()

        # Tạo nút Zoom In
        zoom_in_button = tk.Button(zoom_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_button.pack(side=tk.LEFT, padx=5)

        # Tạo nút Zoom Out
        zoom_out_button = tk.Button(zoom_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.pack(side=tk.LEFT, padx=5)

        # Tạo Canvas để hiển thị hình ảnh
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        # Tạo nút để lưu hình ảnh đã xử lý
        save_button = tk.Button(self.root, text="Save Processed Image", command=self.save_processed_image)
        save_button.pack(pady=10)

    def open_image(self):
        # Mở hình ảnh từ tệp tin
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            self.process_image()

    def process_image(self, *args):
        if self.original_image is not None:
            # Tạo bản sao của hình ảnh gốc để xử lý
            processed_image = self.original_image.copy()

            # Điều chỉnh độ sáng và độ bão hòa màu
            processed_image = self.adjust_brightness(processed_image, self.brightness_factor.get())
            processed_image = self.adjust_saturation(processed_image, self.saturation_factor.get())

            # Thay đổi kích thước hình ảnh theo tỷ lệ zoom
            processed_image = self.resize_image(processed_image, self.zoom_factor.get())

            # Hiển thị hình ảnh trên Canvas
            self.display_image(processed_image)

            # Lưu hình ảnh đang xử lý
            self.processed_image = processed_image

    def adjust_brightness(self, image, factor):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * factor, 0, 255)
        result_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result_image

    def adjust_saturation(self, image, factor):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
        result_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result_image

    def resize_image(self, image, factor):
        height, width, _ = image.shape
        new_height = int(height * factor)
        new_width = int(width * factor)
        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image

    def display_image(self, image):
        # Chuyển đổi hình ảnh OpenCV sang định dạng PIL để hiển thị trên Canvas
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)

        # Cập nhật hình ảnh trên Canvas
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def save_processed_image(self):
        if self.processed_image is not None:
            # Lưu hình ảnh đã xử lý vào tệp tin
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                print(f"Processed image saved to {file_path}")

    def zoom_in(self):
        self.zoom_factor.set(self.zoom_factor.get() + 0.1)
        self.process_image()

    def zoom_out(self):
        self.zoom_factor.set(max(0.1, self.zoom_factor.get() - 0.1))
        self.process_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
