import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.sans-serif"] = ["SimHei"] # Set font to SimHei
plt.rcParams["axes.unicode_minus"] = False # Fix for negative signs
def continuous_data_example():
    """连续型数值数据示例"""
    print("连续型数值数据示例")

    np.random.seed(1202)
    n_samples = 1000

    heights = np.random.normal(loc=170, scale=10, size=n_samples)
    weights = (heights * 0.7 + np.random.normal(loc=0, scale=5, size=n_samples))/2
    temperatures = np.random.normal(loc=36.5, scale=0.5, size=n_samples)

    # 创建数据格式
    continuous_data = pd.DataFrame({
        "身高(cm)" : heights,
        "体重(kg)" : weights,
        "体温(°C)" : temperatures,
        "年龄" : np.random.randint(18, 65, size=n_samples),

    })

    print("连续性数据示例:")
    print(continuous_data.head(5))
    print(f"\n数据统计信息 :")
    print(continuous_data.describe())

    # 可视化连续性数据分布
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.hist(continuous_data["身高(cm)"], bins=30,alpha=0.7,color="skyblue")
    plt.title('身高分布')
    plt.xlabel('身高 (cm)')
    plt.ylabel('频数')

    plt.subplot(2, 2, 2)
    plt.hist(continuous_data['体重(kg)'], bins=30, alpha=0.7, color='lightgreen')
    plt.title('体重分布')
    plt.xlabel('体重 (kg)')
    plt.ylabel('频数')

    plt.subplot(2, 2, 3)
    plt.hist(continuous_data['体温(°C)'], bins=30, alpha=0.7, color='salmon')
    plt.title('体温分布')
    plt.xlabel('体温 (°C)')
    plt.ylabel('频数')

    plt.subplot(2, 2, 4)
    plt.scatter(continuous_data['身高(cm)'], continuous_data['体重(kg)'], alpha=0.6)
    plt.title('身高 vs 体重')
    plt.xlabel('身高 (cm)')
    plt.ylabel('体重 (kg)')

    plt.tight_layout()
    plt.show()

    return continuous_data




if __name__ == '__main__':
    continuous_df = continuous_data_example()