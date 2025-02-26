# DummyMessenger

<!-- TOC -->
* [DummyMessenger](#dummymessenger)
* [Инструкция запуска](#инструкция-запуска)
  * [Установка/запуск виртуального окружения](#установказапуск-виртуального-окружения)
  * [Запуск](#запуск)
<!-- TOC -->
# Инструкция запуска
## Установка/запуск виртуального окружения

Для установки виртуального окружения выполните в командной строке:
```commandline
pipenv install --ignore-pipfile
```

Для активации виртуального окружения выполните в командной строке:
```commandline
pipenv shell
```

Откройте терминал для запуска программы и перейдите в раздел src.
```commandline
cd src
```

Создайте и заполните файл `.env` согласно `.env_example`.

## Запуск
Откройте три терминала. В первом и во втором выполните запуск серверов
```commandline
uvicorn server:app --host 0.0.0.0 --port 8009
```

```commandline
uvicorn server:app --host 0.0.0.0 --port 8008
```
В третьем терминале выполните команду
```commandline
python client.py
```