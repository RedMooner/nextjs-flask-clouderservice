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
  function GETProfile() {
    if (isAuth == "") {
      return;
    }
    console.log(isAuth)
    // Default options are marked with *
    const response = fetch("http://localhost:8080/api/profile", {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "Authorization": "Bearer " + isAuth,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      //body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    return response.json()
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
      </AuthContext.Provider>
    </div>
  );
}

export default index; 