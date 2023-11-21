# Проект "Screen recorder"

Проект "Screen recorder" представляет собой приложение для записи экрана компьютера с использованием библиотеки GStreamer и библиотеки tkinter для создания графического интерфейса пользователя (GUI).

Этот проект является рефакторингом популярной записывалки:
- [Kazam](https://github.com/henrywoo/kazam)

Был оставлен функционал для VP8

## Описание

Приложение позволяет пользователям выполнять следующие действия:

- **Start Recording**: Запускает запись экрана компьютера.
- **Pause Recording**: Приостанавливает запись.
- **Resume Recording**: Возобновляет запись.
- **Stop Recording**: Завершает запись и сохраняет видеофайл.

## Требования

Для успешной работы проекта необходимы следующие зависимости:

- Python 3
- GStreamer
- pycairo
- PyGObject

## Установка и запуск

1. Убедитесь, что у вас установлен Python 3.

2. Установите библиотеку GStreamer, если она не установлена, следуя инструкциям для вашей операционной системы.

- [Установка GStreamer](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c)
- [Установка PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html)

3. Запустите приложение, выполнив файл `main.py`:

'''bash
python3 main.py
'''

4. В графическом интерфейсе выберите параметры записи, нажмите "Start Recording" для начала записи и используйте другие кнопки для управления записью.

- Файл с записью появится в рабочей дирректории приложения

## Исходный код:

Исходный код: (https://github.com/henrywoo/kazam)

## Автор

Автор проекта: [Sergey Nikiforov]
