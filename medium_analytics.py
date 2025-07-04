#🧠 Medium Tasks (Фитнес-Трекер)

# 1. Фильтрация по событиям (event_flag)
# Найди значения heart_rate, записанные в часы, когда событие — 'workout'.
# Посчитай среднее значение skin_temp в часы, когда событие — 'normal'.
# 2. Анализ изменений (steps_count)
# Вычисли изменение количества шагов по часам (разницу между текущим и предыдущим значением).
# Найди часы, когда steps_count вырос по сравнению с предыдущим.
# 3. Комбинирование данных
# Построй 2D-массив, где:
# 1-я колонка — time_point
# 2-я колонка — heart_rate
# Определи, в какой час heart_rate достиг максимума.
# 4. Обработка некорректных данных (event_flag == 'sleep')
# Считаем, что во время сна steps_count некорректен. Замени все такие значения на np.nan.
# Теперь пересчитай среднее steps_count, игнорируя NaN: np.nanmean(...).



import json
import pandas as pd
import numpy as np

# Upload JSON-file
with open("experiment_output.json", "r") as file:
    data = json.load(file)

# Make DataFrame
df = pd.DataFrame(data)

# 1.1 Calculate the average skin_temp value during the hours when the event is 'normal'.
avg_temp_normal = df.loc[df["event_flag"] == "normal", "skin_temp"].mean()
print("🌡 Average skin temperature at 'normal':", round(avg_temp_normal, 2), "°C")

# 1.2 Calculate the average skin_temp value during the hours when the event is 'normal'.
avg_temp_normal = df.loc[df["event_flag"] == "normal", "skin_temp"].mean()
print("🌡 Average skin temperature at 'normal':", round(avg_temp_normal, 2), "°C")

# 2.1 Calculate the change in the number of steps per hour (the difference between the current and previous value)
df["step_change"] = df["steps_count"].diff()
print("📈 Changing the number of steps by hour:")
print(df[["time_point", "steps_count", "step_change"]].head(10))

# 2.2 Find the hours when steps_count increased compared to the previous one.
increased_steps = df[df["step_change"] > 0]
print("🔼 Hours when the number of steps increased:")
print(increased_steps[["time_point", "steps_count", "step_change"]].to_string(index=False))

# 3.1 Step 1: Build a 2D array
hr_array = df[["time_point", "heart_rate"]].to_numpy()
print("📊 2D-array (time_point, heart_rate):")
print(hr_array[:5])  # покажем первые 5 строк

# 3.2 Step 2: Find your maximum heart rate hour
max_idx = df["heart_rate"].idxmax()
max_time = df.loc[max_idx, "time_point"]
max_hr = df.loc[max_idx, "heart_rate"]
print(f"💓 Maximum heart rate {max_hr} bpm был в {max_time}:00")

# 4.1 We believe that during sleep steps_count is incorrect. Replace all such values ​​with np.nan.
df["steps_cleaned"] = df["steps_count"].copy()
df.loc[df["event_flag"] == "sleep", "steps_cleaned"] = np.nan

# 4.2 Now recalculate the steps_count average, ignoring NaNs: np.nanmean(...).
avg_steps_cleaned = np.nanmean(df["steps_cleaned"])
print(f"🚶 Average number of steps (without sleep): {round(avg_steps_cleaned, 2)}")
