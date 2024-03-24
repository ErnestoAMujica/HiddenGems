"use client";
import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button'
function loginPage() {
  const[link, setLink] = useState("Loading")

  //fetch auth link at page load
  
  useEffect(() => {
    fetch("http://localhost:8080/api/auth")
    .then((response) => response.json())
    .then((data) => {
      setLink(data.link);
    });
  }, []);
  

  //redirect with prefetched link on button click
  const handleClick = async() => {
    redirectLogin(link)
  }

  const redirectLogin = async(link: string) => {
    location.assign(link)
  }  

  return (
    <div className="loginWrapper">
      <div className="formWrapper">
        <div className="center">
          <div className="inner">
            <h3 className="title">Hidden Gems</h3>
            <p>Spotify Song Recommendation App</p>
            <Button onClick={handleClick} className='border-zinc-500 text-zinc-300
            hover:border-zinc-200 hover:text-zinc-100 text-center
            transition-colors border px-8 w-full '>
              Login with Spotify
            </Button>
          </div>
        </div>
      </div>
    </div>
    
  )

}

export default loginPage