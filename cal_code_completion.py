import os
from fuzzywuzzy import fuzz
import numpy as np

# 定义文件夹路径
folder_path = os.path.join(os.getcwd(), "mutation")
# print(folder_path)

# 获取文件列表
file_list = os.listdir(folder_path)

def calculate_completion(file_list, T = len(file_list)-1):

    outliers = []

    # 初始化相似度矩阵
    num_files = len(file_list)
    similarity_matrix = [[0]*num_files for _ in range(num_files)]

    # 计算相似度矩阵
    for i in range(num_files):
        for j in range(i, num_files):
            file1_path = os.path.join(folder_path, file_list[i])
            file2_path = os.path.join(folder_path, file_list[j])

            # Read file content
            with open(file1_path, 'r', encoding='utf-8') as file1:
                content1 = file1.read()
            with open(file2_path, 'r', encoding='utf-8') as file2:
                content2 = file2.read()

            # calculate similarity score
            similarity_score = fuzz.ratio(content1, content2)

            similarity_matrix[i][j] = similarity_score
            similarity_matrix[j][i] = similarity_score

    # Normalize the similarity matrix
    max_value = np.max(similarity_matrix)
    min_value = np.min(similarity_matrix)
    normalized_matrix = (similarity_matrix - min_value) / (max_value - min_value)

    # #print file name and corresponding similarity matrix
    # for i in range(num_files):
    #     print(file_list[i], normalized_matrix[i])


    # Median of the normalized similarity matrix
    median_similarity = np.median(normalized_matrix)
    # print(median_similarity)

    # Calculate the outliers
    for i in range(num_files):
        count_o = 0
        for j in range(num_files):
            if normalized_matrix[i][j] < median_similarity:
                count_o += 1
                if count_o >= T:
                    outliers.append(file_list[i])
                    break
    print("Outliers: ", outliers)

    # Calculate mean pairwise similarity excluding outliers
    mean_similarity = 0
    count = 0
    for i in range(num_files):
        if file_list[i] not in outliers:
            for j in range(i, num_files):
                if file_list[j] not in outliers:
                    mean_similarity += normalized_matrix[i][j]
                    count += 1
    mean_similarity /= count



    #Find whose average pair-wise similarity scores with all other elements in file list is the closest to mean similarity.
    closest_file = ""
    closest_similarity_distance = 10

    for i in range(num_files):
        if file_list[i] not in outliers:
            similarity_distance = 0
            count = 0
            for j in range(num_files):
                if file_list[j] not in outliers:
                    similarity_distance += abs(normalized_matrix[i][j])
                    count += 1
            similarity_distance /= count

            if closest_similarity_distance >= abs(mean_similarity - similarity_distance):
                closest_similarity_distance = abs(mean_similarity - similarity_distance)
                closest_file = file_list[i]

    return closest_file


if __name__ == "__main__":
    print(calculate_completion(file_list))


    



