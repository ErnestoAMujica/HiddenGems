"use client";
import React, { useEffect, useState } from 'react';
import {Button} from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"

function recs() {
  const[trackNames, setTrackNames] = useState([]);
  const[trackArtists, setTrackArtists] = useState([]);
  const[trackImageLinks, setTrackImageLinks] = useState([]);
  const[trackIDs, setTrackIDs] = useState([]);

  const[newPlaylistLink, setNewPlaylistLink] = useState('');

  let selectedPlaylistID = window.location.href.substring(
    window.location.href.indexOf("?plid=") + 6,
  );

  let sendData = { "selected_playlist_id": selectedPlaylistID }

  useEffect(() => {
    fetch("http://localhost:8080/api/get_recommendations", {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(sendData)
    })
    .then((response) => response.json())
    .then((data) => {
      setTrackNames(data.track_names)
      setTrackArtists(data.track_artists)
      setTrackImageLinks(data.track_imagelinks)
      setTrackIDs(data.track_ids)
    });
  }, []);

  //N array zipping, written by Claude AI
  function zipArrays<T>(...arrays: T[][]): T[][] {
    const length = Math.min(...arrays.map(arr => arr.length));
    const zippedArray: T[][] = [];
  
    for (let i = 0; i < length; i++) {
      const tempArray: T[] = [];
      for (const arr of arrays) {
        tempArray.push(arr[i]);
      }
      zippedArray.push(tempArray);
    }
  
    return zippedArray;
  }
  
  let trackDetails = zipArrays(trackNames, trackImageLinks, trackArtists);

  const onChange = async(value: string) => {
    console.log()
  }

  const onSubmit = async() => {
    let playlistName = document.getElementById('playlistname').value
    let sendData = { "selected_tracks": trackIDs , "playlist_name": playlistName}

    const response = await fetch("http://localhost:8080/api/create_playlist_from_tracks", {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(sendData)
    })
    const data = await response.json()
    console.log(data)
    await setNewPlaylistLink(data.playlist_id)

    console.log(newPlaylistLink)

    //Add failure condition here and in server later
    location.assign('http://localhost:3000/pages/playlist_added' + '?plid=' + selectedPlaylistID)
  }

  return(
    <div className="outerWrapper select-none">
      <div className="formWrapper">
        <div className="center">
          <div className="inner">

            <Card>
              <CardHeader className="pb-3">
                <CardTitle>View Recommendations Playlist</CardTitle>
                <CardDescription>
                  Browse recommended songs and name new playlist
                </CardDescription>
              </CardHeader>
              <CardContent className="">
              <div className="scrollarea">
                <ScrollArea className="flex aspect-[3/4] rounded-lg w-[3/4] bg-accent text-accent-foreground transition-all">
                  {trackDetails.map((values) => (
                      <div className="-mx-2 flex items-start space-x-4 rounded-md bg-accent 
                                        p-2 text-accent-foreground transition-all px-4 mx-4 truncate text-ellipsis ...">
                        <img className="mt-px h-12 w-12" src={values[1]} alt=""/>
                        <div className="space-y-1">
                          <p className="text-sm font-medium leading-none">{values[0]}</p>
                          <p className="text-sm justify-left text-muted-foreground">
                            {values[2]}
                          </p>
                        </div>
                      </div>
                    ))}
                </ScrollArea>
              </div>
              </CardContent>
            </Card>
            <div className="text-sm p-2 font-light bg-accent text-accent-foreground transition-all">
              <Input type="playlistname" id="playlistname" placeholder="Name the playlist..." />
            </div>
            <Button onClick={onSubmit} className='border-zinc-500 text-zinc-300
            hover:border-zinc-200 hover:text-zinc-100 text-center
            transition-colors border px-8 my-3 w-full '
            style={{ backgroundColor: '#1DB954', color: 'white' }}>
              Add Playlist to Profile
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default recs