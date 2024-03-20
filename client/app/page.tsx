"use client";
import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button'

const redirectLogin = async(link: string) => {
  location.assign(link)
}

function loginPage() {

  console.log('in login func');
  const[link, setLink] = useState("Loading")

  useEffect(() => {
    fetch("http://localhost:8080/api/auth")
    .then((response) => response.json())
    .then((data) => {
      setLink(data.link);
    });
  }, []);

  const handleClick = async() => {
    redirectLogin(link)
  }

  return (
    <div className="loginWrapper">
      <div className="formWrapper">
        <div className="left">
          <h3 className="title">Hidden Gems</h3>
          <p>Spotify Song Recommendation App</p>
            <Button onClick={handleClick} className='border-zinc-500 text-zinc-300
            hover:border-zinc-200 hover:text-zinc-100
            transition-colors border rounded-full px-8'>
              Login with Spotify
            </Button>
        </div>
      </div>
    </div>
    
  )

}

export default loginPage