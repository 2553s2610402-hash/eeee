import streamlit as st
st.title('천안오성고등학교 화이팅')
st.write('바이브 코딩 재미있다!!')

import os
import shutil


folder = "downloads"
types = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Videos": [".mp4", ".mov"],
    "Documents": [".pdf", ".txt", ".docx"],
}

for file in os.listdir(folder):
    file_path = os.path.join(folder, file)

    if os.path.isfile(file_path):
        ext = os.path.splitext(file)[1].lower()

        for category, extensions in types.items():
            if ext in extensions:
                new_folder = os.path.join(folder, category)

                os.makedirs(new_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(new_folder, file))
                print(f"{file} -> {category}")
