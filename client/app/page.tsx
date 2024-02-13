"use client";
import React, { useEffect, useState } from 'react';
function page() {
  const [message, setMessage] = useState("Loading");
  const [list, setList] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => {
        //general flow:
        //message = loading
        //data retrieved
        //message = data.message, which is in server.py
        setMessage(data.message);
        setList(data.list);
        console.log(data.list);

      });
  },  []);

  return (
    <div>
      <div>{message}</div>

      
    {list.map((member, index) => (
      <div key = {index}>{member}</div>
      ))}
      </div>
    //List section is returning an array of stuff from server.py
    //Running client command is "npm run dev" just in client folder
    
  );
}

export default page