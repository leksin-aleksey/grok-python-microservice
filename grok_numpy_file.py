import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt



# Fitness Tracker

def grok_question() -> str:
    api_key = os.environ.get("grok_token")
    if not api_key:
        raise RuntimeError("Environment variable 'grok_token' not set.")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = (
        "Simulate the 24-hour activity data of a person wearing a fitness tracker. "
        "Generate a JSON array with 24 data points, one for each hour of the day (from 0 to 23).\n\n"
        "Each data point should include:\n"
        "- 'time_point': Integer from 0 to 23 representing the hour\n"
        "- 'steps_count': Integer representing the number of steps taken in that hour (higher during daytime, low or zero at night)\n"
        "- 'heart_rate': Float showing heart rate in bpm (fluctuates, higher during activity)\n"
        "- 'skin_temp': Float in °C showing skin temperature with slight variation\n"
        "- 'event_flag': One of: 'normal', 'sleep', 'workout' (e.g. at hour 7 or 18), 'resting', or 'idle'\n\n"
        "Include at least one 'workout' and one 'sleep' event.\n"
        "The output MUST be a valid JSON array with no markdown formatting or explanation. Only the pure JSON array."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        output = response.json()
        return output["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"Request failed: {response.status_code} {response.text}")


def clean_json(text: str) -> str:
    # Удаляем markdown-блоки ```json и ```
    lines = text.splitlines()
    cleaned = "\n".join(line for line in lines if not line.strip().startswith("```"))
    if not cleaned.strip().endswith("]"):
        cleaned += "]"  # если модель обрезала, просто закрываем массив
    return cleaned


# --- Основной вызов
if __name__ == "__main__":
    try:
        # Загрузка из файла или запрос
        if os.path.exists("experiment_output.json"):
            with open("experiment_output.json", "r") as f:
                result_json = json.load(f)
                print("🔁 Загружены сохранённые данные из файла.")
        else:
            result_str = grok_question()
            clean_str = clean_json(result_str)
            result_json = json.loads(clean_str)
            with open("experiment_output.json", "w") as f:
                json.dump(result_json, f, indent=4)
                print("✅ Данные получены от модели и сохранены в файл.")

        # Анализ
        df = pd.DataFrame(result_json)

        print('\n📊 Basic Statistics')
        print('Average by steps:', df['steps_count'].mean())
        print('Maximum by steps:', df['steps_count'].max())
        print('Minimum by steps:', df['steps_count'].min())
        print('Standard deviation of steps:', df['steps_count'].std())

        print("\n🔍 Specific data:")
        print("Hart rate at 5 o'clock:", df.loc[df["time_point"] == 5, "heart_rate"].values[0])
        print("Temperature at first 10 hours:\n", df.loc[df["time_point"] < 10, "skin_temp"].values)

        print("\n🧮 Elementary operations:")
        df["heart_rate_percent"] = (df["heart_rate"] - 40) / (180 - 40) * 100
        df["hr_minus_temp"] = df["heart_rate"] - df["skin_temp"]
        print(df[["time_point", "heart_rate_percent", "hr_minus_temp"]].head())

        print("\n✅ Filtering:")
        print("Пульс > 100:\n", df[df["heart_rate"] > 100][["time_point", "heart_rate"]])
        print("Workout часы:\n", df[df["event_flag"] == "workout"][["time_point", "event_flag"]])

        print('\n📊 Medium Statistics next page')





    except Exception as e:
        print("Error:", e)
