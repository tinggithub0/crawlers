import os
import sys
import traceback
from PySide2 import QtWidgets, QtCore, QtGui


class ImgTag(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('labeling tool')
        # 主控制元件和主控制元件佈局
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        # 影象展示控制元件
        self.img_widget = QtWidgets.QWidget()
        self.img_layout = QtWidgets.QHBoxLayout()
        self.img_widget.setLayout(self.img_layout)

        # 標籤佔位
        self.img_view = QtWidgets.QLabel("請選擇一個資料夾")
        self.img_view.setAlignment(QtCore.Qt.AlignCenter)
        self.img_layout.addWidget(self.img_view)
        
        # 影象標註控制元件
        self.img_input = QtWidgets.QLineEdit()
        
        # 控制按鈕控制元件
        self.opera_widget = QtWidgets.QWidget()
        self.opera_layout = QtWidgets.QVBoxLayout()
        self.opera_widget.setLayout(self.opera_layout)

        # 各個按鈕
        self.select_img_btn = QtWidgets.QPushButton("選擇目錄", self)
        self.previous_img_btn = QtWidgets.QPushButton("上一張")
        self.previous_img_btn.setEnabled(False)
        self.next_img_btn = QtWidgets.QPushButton("下一張")
        self.next_img_btn.setEnabled(False)
        self.save_img_btn = QtWidgets.QPushButton("儲存")
        self.save_img_btn.setEnabled(False)

        # 新增按鈕到佈局
        self.opera_layout.addWidget(self.select_img_btn)
        self.opera_layout.addWidget(self.previous_img_btn)
        self.opera_layout.addWidget(self.next_img_btn)
        self.opera_layout.addWidget(self.save_img_btn)
        
        # 將控制元件新增到主控制元件佈局層
        self.main_layout.addWidget(self.img_widget, 1, 1)
        self.main_layout.addWidget(self.opera_widget, 1, 2)
        self.main_layout.addWidget(self.img_input, 2, 1)
        
        # 狀態列
        self.img_total_current_label = QtWidgets.QLabel()
        self.img_total_label = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.img_total_current_label)
        self.statusBar().addPermanentWidget(self.img_total_label, stretch=0) # 在狀態列新增永久控制元件
        
        # 設定UI介面核心控制元件
        self.setCentralWidget(self.main_widget)

        self.start()

    # 讀圖
    def load_image(self, img_list_len=''):
        # 當前圖片檔案路徑
        self.current_filename = os.path.join(
            self.dir_path, self.img_index_dict[self.current_index]
        )

        # 例項化一個影象
        image = QtGui.QImage(self.current_filename)
        self.img_width = image.width() # 圖片寬度
        self.img_height = image.height() # 圖片高度
        self.img_scale = 1
        self.image = image.scaled(
            self.img_width*self.img_scale, self.img_height*self.img_scale
        )
        
        # 在img_view控制元件中顯示影象
        self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image))
        
        # 設定img_input控制元件文字內容
        self.img_input.setText('')
        self.img_input.setFocus() # 獲取輸入框焦點
        
        # 設定狀態列
        self.img_total_current_label.setText(str(self.current_index))
        if img_list_len:
            self.img_total_label.setText(f'/{img_list_len}')

    # 修改當前影象檔名
    def rename_img(self):
        new_tag = self.img_input.text() # 獲取當前輸入框內容
        if new_tag != '':
            current_img = self.img_index_dict[self.current_index] # 獲取當前圖片名稱
            new_name = f'{new_tag}_{self.current_index}.{current_img.split(".")[-1]}'
            try:
                os.rename(
                    os.path.join(self.dir_path, current_img), 
                    os.path.join(self.dir_path, new_name)
                ) # 修改檔名
                self.img_index_dict[self.current_index] = new_name
            except FileExistsError as e: # 同名檔案異常
                print(repr(e))
                QtWidgets.QMessageBox.information(
                    self, '提示','已存在同名檔案', QtWidgets.QMessageBox.Ok
                )

    # 選擇目錄按鈕
    def select_img_click(self):
        self.dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, '選擇資料夾')
        # print(self.dir_path)

        # 整理編號 & 檔名到 dict: {1:'1.jpg', 2:'2.jpg', ...}
        dir_list = os.listdir(self.dir_path)
        img_list = []
        no_list = []
        for dir in dir_list:
            no, suf = dir.split('.')
            suffix_list = ['jpg','png','jpeg','bmp',]
            if suf.lower() in suffix_list:
                img_list.append(dir)
                no_list.append(int(no))
        
        # 影象檔案索引字典
        self.img_index_dict = {}
        for no, img in zip(no_list, img_list):
            self.img_index_dict[no] = img
        self.current_index = 1 # 當前的影象索引 = 編號
        
        # 讀圖 & 設定 label
        self.load_image(len(img_list))

        # 按鈕亮起來
        self.previous_img_btn.setEnabled(True)
        self.next_img_btn.setEnabled(True)
        self.save_img_btn.setEnabled(True)

    # 下一張圖片
    def next_img_click(self):
        # 修改當前影象檔名
        self.rename_img()

        # 當前影象索引加1
        self.current_index += 1
        if self.current_index in self.img_index_dict.keys():
            # 讀圖
            self.load_image()
        else:
            self.current_index -=1
            QtWidgets.QMessageBox.information(
                self, '提示', '所有圖片已標註完', QtWidgets.QMessageBox.Ok
            )

    # 上一張圖片
    def previous_img_click(self):
        # 修改當前影象檔名
        self.rename_img()

        # 當前影象索引減1
        self.current_index -= 1
        if self.current_index in self.img_index_dict.keys():
            # 讀圖
            self.load_image()
        else:
            self.current_index += 1
            QtWidgets.QMessageBox.information(
                self, '提示', '圖片列表到頂了', QtWidgets.QMessageBox.Ok
            )

    # 重寫滑鼠滾輪事件
    def wheelEvent(self,event):
        # 如果按住了Ctrl
        if event.modifiers() == QtCore.Qt.ControlModifier:
            try:
                delta = event.angleDelta().y()
                if delta > 0:
                    self.img_scale += 0.25
                    self.image_scaled = self.image.scaled(
                        self.img_width * self.img_scale, self.img_height * self.img_scale
                    )
                    self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image_scaled))
                    self.statusBar().showMessage(
                        f'當前圖片縮放比例為: {self.img_scale * 100}%'
                    )
                elif delta < 0:
                    if self.img_scale > 0.25:
                        self.img_scale -= 0.25
                        self.image_scaled = self.image.scaled(
                            self.img_width * self.img_scale, self.img_height * self.img_scale
                        )
                        self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image_scaled))
                        self.statusBar().showMessage(
                            f'當前圖片縮放比例為: {self.img_scale * 100}%'
                        )
            except Exception as e:
                print(traceback.print_exc())
                print(repr(e))

    def start(self):
        self.select_img_btn.clicked.connect(self.select_img_click)
        self.next_img_btn.clicked.connect(self.next_img_click)
        self.save_img_btn.clicked.connect(self.next_img_click)
        self.img_input.returnPressed.connect(self.next_img_click) # 回車事件繫結
        self.previous_img_btn.clicked.connect(self.previous_img_click)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = ImgTag()
    gui.show()    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# todo
# 輸入框加長度限制
