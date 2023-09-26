import { data } from 'autoprefixer';
import React, { useEffect, useState } from 'react';

function index() {
  const [message, setMessage] = useState('Loading');
  // const requestOptions = {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ Email: 'test.test@mail.ru', Name: 'test.test@mail.ru', Surname: "test", Password: '123' })
  // };
  // useEffect(() => {
  //   fetch('http://localhost:8080/api/register', requestOptions)
  //     .then((response) => response.json(""))
  //     .then((data) => {
  //       setMessage(data.message);
  //       console.log(data.message);
  //       setMessage("Вы зарегистрировались");
  //     })
  // }, []);
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  function POSTlogin() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: login, password: password })
    };

    fetch('http://localhost:8080/api/login', requestOptions)
      .then((response) => response.json())
      .then((data) => {
        console.log(data.status)
      })

  }
  return (
    <div>
      <div>{message}</div>
      <input type="text"
        value={login}
        onChange={e => setLogin(e.target.value)} />
      <input type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)} />
      <button onClick={POSTlogin}>Войти</button>
    </div>
  );
}

export default index; 