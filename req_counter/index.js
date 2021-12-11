import express from "express";
import { hostname } from "os";
import { argv, exit } from "process";

// Серверное приложение.
const app = express();

// Глобальный счётчик входящих запросов.
let requests = 0;

// Обработка входящего запроса.
app.get("*", (req, res) => {
  // Увеличиваем глобальный счётчик запросов.
  requests += 1;
  // Логгируем входящий запрос.
  console.log(`${req.method} ${req.url}`);
  // Возвращаем информацию о текущем хосте и количестве запросов.
  res.json({
    requests: requests,
    hostname: hostname(),
  });
});

// Аргументы командной строки.
// Напрмиер yarn run server 127.0.0.1 8000
const args = argv.slice(2);

// Если передано неверное количество аргументов.
if (args.length != 2) {
  console.error("Usage: yarn run server {host} {port}");
  exit(1);
}

// Простейший "парсинг" аргументов командной строки.
const host = args[0];
const port = args[1];

// Старт сервера.
app.listen(port, host, () => {
  console.log(`Server listening at http://${host}:${port}`);
});
