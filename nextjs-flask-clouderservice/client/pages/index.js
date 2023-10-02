import { AuthContext } from '@/context';
import { data } from 'autoprefixer';
import React, { useEffect, useState } from 'react';

function index() {
  // Сообщение 
  const [message, setMessage] = useState('Loading');
  // Пользователь
  const [login, setLogin] = useState('');
  // Пароль
  const [password, setPassword] = useState('');
  // отправка запроса на сервер
  const [isAuth, setIsAuth] = useState('');
  // Папка
  const [folder, setFolder] = useState('');

  function getFiles() {
    if (isAuth == "") {
      return;
    }
    fetch("http://localhost:8080/api/getfiles/root", {
      method: "GET",
      mode: "cors",
      credentials: "same-origin",
      headers: {
        "Authorization": "Bearer " + isAuth,
      },
    })
      .then(response => response.json())
      .then(data => {
        // тут вы можете работать с данными в формате JSON
        console.log(data);
      })
      .catch(error => {
        // обработка ошибок
        console.error("Произошла ошибка:", error);
      });

  }
  function GETProfile() {
    if (isAuth == "") {
      return;
    }
    fetch("http://localhost:8080/api/profile", {
      method: "GET",
      mode: "cors",
      credentials: "same-origin",
      headers: {
        "Authorization": "Bearer " + isAuth,
      },
    })
      .then(response => response.json())
      .then(data => {
        // тут вы можете работать с данными в формате JSON
        console.log(data);
      })
      .catch(error => {
        // обработка ошибок
        console.error("Произошла ошибка:", error);
      });

  }
  function POSTlogin() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: login, password: password })
    };

    fetch('http://localhost:8080/api/login', requestOptions)
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "Invalid Credentials") {
          setIsAuth('');
          setMessage(data.status);

        } else {
          setIsAuth(data.status);
          setMessage(data.status);
          if (data.status != "") {
            console.log(GETProfile());
          }
          console.log(isAuth)
        }
      })

  }
  function GetFilesFromFolder() {
    if (isAuth == "") {
      return;
    }
    fetch("http://localhost:8080/api/getfiles/" + folder, {
      method: "GET",
      mode: "cors",
      credentials: "same-origin",
      headers: {
        "Authorization": "Bearer " + isAuth,
      },
    })
      .then(response => response.json())
      .then(data => {
        // тут вы можете работать с данными в формате JSON
        console.log(data);
      })
      .catch(error => {
        // обработка ошибок
        console.error("Произошла ошибка:", error);
      });
  }
  return (
    <div>
      <AuthContext.Provider value={{
        isAuth,
        setIsAuth
      }}>
        <div>{message}</div>
        <input type="text"
          value={login}
          onChange={e => setLogin(e.target.value)} />
        <input type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)} />
        <button onClick={POSTlogin}>Войти</button>
        <button onClick={getFiles}>Получить файлы</button>

        <input type="text"
          value={folder}
          onChange={e => setFolder(e.target.value)} />
        <button onClick={GetFilesFromFolder}>Получить файлы из папки, указанной выше</button>
      </AuthContext.Provider>
    </div>
  );
}

export default index; 