import time
import random

class NeuralNetworkTrainer:
    def __init__(self):
        # Инициализация параметров модели
        self.model = None

    def train_model(self):
        # Имитация обучения модели
        print("Начало обучения модели...")
        time.sleep(2)  # Задержка для имитации процесса обучения
        if random.random() < 0.5:  # 50% шанс на ошибку
            raise ValueError("Произошла ошибка во время обучения!")
        print("Модель успешно обучена!")

def train_with_retries(trainer, max_retries=10000):
    retries = 0
    while retries < max_retries:
        try:
            trainer.train_model()
            print("Обучение завершено успешно.")
            break
        except Exception as e:
            retries += 1
            print(f"Ошибка: {e}. Перезапуск обучения ({retries}/{max_retries})...")
            time.sleep(1)  # Задержка перед повторной попыткой
    else:
        print("Превышено количество попыток обучения. Обучение не удалось.")

if __name__ == "__main__":
    trainer = NeuralNetworkTrainer()
    train_with_retries(trainer)
