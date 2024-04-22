"use client";
import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button'
function playlist_added() {
  const[link, setLink] = useState("Loading")

  //fetch auth link at page load
  /*
  useEffect(() => {
    fetch("http://localhost:8080/api/auth")
    .then((response) => response.json())
    .then((data) => {
      setLink(data.link);
    });
  }, []);
  */

  //redirect with prefetched link on button click
  const handleClick = async() => {
    let plid = window.location.href.substring(
      window.location.href.indexOf("?plid=") + 6,
    );
    let link = 'https://open.spotify.com/playlist/' + plid
    redirectLogin(link)
  }

  const redirectLogin = async(link: string) => {
    window.open(link, '_blank');
  }  

  return (
    <div className="loginWrapper">
      <div className="formWrapper">
        <div className="center">
          <div className="inner">
            <h3 className="title">Playlist Created</h3>
            <Button onClick={handleClick} className='bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full'
            style={{ backgroundColor: '#1DB954', color: 'white' }}>
              Go to Created Playlist!
            </Button>
          </div>
        </div>
      </div>
    </div>
    
  )

}

export default playlist_added