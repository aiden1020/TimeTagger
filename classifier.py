import os
import shutil
import streamlit as st
from preprocess import process_images
from PIL import Image


def copy_processed_images_from_folders(input_directory, output_directory='output'):
    subfolders = [folder for folder in os.listdir(
        input_directory) if os.path.isdir(os.path.join(input_directory, folder))]

    st.write(f"Total {len(subfolders)} folders")

    for subfolder in subfolders:
        subfolder_path = os.path.join(input_directory, subfolder)
        st.write(f"Processing folder: {subfolder}")

        # 使用 process_images 來處理圖像
        processed_filenames = process_images(input_directory=subfolder_path)

        output_subfolder = os.path.join(output_directory, subfolder)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        for filename in processed_filenames:
            source_path = os.path.join(subfolder_path, filename)
            destination_path = os.path.join(output_subfolder, filename)
            shutil.copy(source_path, destination_path)

        st.write(f"Done processing folder: {subfolder_path}")


def display_and_select_images_for_deletion(output_directory):
    # 顯示每個資料夾中的圖像
    for folder_name in os.listdir(output_directory):
        folder_path = os.path.join(output_directory, folder_name)

        # 印出目前資料夾的名稱
        st.write(f"Folder: {folder_name}")

        # 取得該資料夾中的所有圖像
        output_images = os.listdir(folder_path)
        image_paths = [os.path.join(folder_path, image_name)
                       for image_name in output_images]

        # 用來保存要刪除的圖像列表
        images_to_delete = []

        with st.form(key=f"delete_form_{folder_name}"):  # 確保每個表單的 key 是唯一的
            cols = st.columns(5)
            for i, image_path in enumerate(image_paths[:10]):  # 限制顯示前 10 張圖像
                image = Image.open(image_path)
                cols[i % 5].image(image, use_column_width=True)

                # 在每張圖像下方放置一個 checkbox
                if cols[i % 5].checkbox(f"Delete {os.path.basename(image_path)}", key=image_path):
                    images_to_delete.append(image_path)
            delete = st.form_submit_button(
                f"Delete Selected Images from {folder_name}")
            # 使用 form_submit_button 並給予唯一的 key
        if delete:
            for image_path in images_to_delete:
                if os.path.exists(image_path):
                    os.remove(image_path)  # 刪除文件
                    st.write(
                        f"{os.path.basename(image_path)} has been deleted.")
            st.success(f"Selected images deleted from {folder_name}.")


# Streamlit UI
st.title("Image Processing Tool")

input_directory = st.text_input("Input Directory", value='dataset/')

output_directory = st.text_input("Output Directory", value='output/')

if st.button("Start Processing"):
    if os.path.exists(input_directory):
        copy_processed_images_from_folders(input_directory, output_directory)
        st.success("Processing complete!")

    else:
        st.error("The specified input directory does not exist.")
if os.path.exists(output_directory):
    st.header("Delete From Output Folder")
    for folder_name in os.listdir(output_directory):
        folder_path = os.path.join(output_directory, folder_name)

        st.write(f"Folder: {folder_name}")

        output_images = os.listdir(folder_path)
        image_paths = [os.path.join(folder_path, image_name)
                       for image_name in output_images]

        images_to_delete = []

        with st.form(key=f"delete_form_{folder_name}"):
            cols = st.columns(5)
            for i, image_path in enumerate(image_paths):
                image = Image.open(image_path)
                cols[i % 5].image(image, use_column_width=True)

                if cols[i % 5].checkbox(f"Delete {os.path.basename(image_path)[-6:]}", key=image_path):
                    images_to_delete.append(image_path)
            if st.form_submit_button(
                    f"Delete Selected Images"):
                for image_path in images_to_delete:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        st.write(
                            f"{os.path.basename(image_path)} has been deleted.")
                st.success(f"Selected images deleted from {folder_name}.")
                st.rerun()

if os.path.exists(output_directory) and st.button("Clear Output Direactory"):
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
        st.write(
            f"output directory has been deleted.")
