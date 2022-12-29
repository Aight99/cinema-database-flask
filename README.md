# База фильмов с возможностью ведения пользовательских списков

Back-end: Python, Flask, Sqlite

Front-end: Jinja2, Tailwind

База составлена из топ-250 фильмов и топ-250 сериалов IMDB на лето 2022

Пример загрузки данных в бд:

https://colab.research.google.com/drive/1uSI44xLGgPAj4kv34eBq_qDPH1CqMEhT?usp=sharing

Пользователь может составлять списки просмотренного и запланированного к просмотру, а также писать рецензии на фильмы с возможностью оценить отдельно каждого члена съемочкой группы

Чтобы инициализировать tailwind:

```npx tailwindcss -i kino_app/static/style.css -o kino_app/static/css/main.css``` или ```npm start run```

Модель базы данных:

![db_model](https://user-images.githubusercontent.com/58304011/197353668-fd0d9909-0a51-43d6-bdd1-a2eb780ae8e9.png)
