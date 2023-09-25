import React, { useEffect, useState } from 'react';

function index() {
  const [message, setMessage] = useState('Loading');
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ Email: 'test.test@mail.ru', Name: 'test.test@mail.ru', Surname: "test", Password: '123' })
  };
  useEffect(() => {
    fetch('http://localhost:8080/api/register', requestOptions)
      .then((response) => response.json(""))
      .then((data) => {
        setMessage(data.message);
        console.log(data.message);
        setMessage("Вы зарегистрировались");
      })
  }, []);
  return (
    <div>{message}</div>

  );
}

export default index; 