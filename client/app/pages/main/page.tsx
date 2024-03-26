"use client";
import React, { useEffect, useState } from 'react';
import {Button} from '@/components/ui/button'
import { useToast } from "@/components/ui/use-toast"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'

function main() {
  const[playlistNames, setNames] = useState([]);
  const[playlistIDs, setIDs] = useState([]);
  const[imageLinks, setImageLinks] = useState([]);
  
  const[res, setPostResponse] = useState('');
  
  useEffect(() => {
    fetch("http://localhost:8080/api/get_playlists_details")
    .then((response) => response.json())
    .then((data) => {
      setNames(data.playlist_names)
      setIDs(data.playlist_ids)
      setImageLinks(data.playlist_imagelinks)
    });
  }, []);

  let playlistDetails = playlistNames.map((x, i) => [x, imageLinks[i]]);
  var selectedPlaylist = ''

  function checkPlaylistName(name: string){
    return name == selectedPlaylist
  }

  const onChange = async(value: string) => {
    selectedPlaylist = value
  }

  const onSubmit = async() => {
    var selectedPlaylistID = playlistIDs[playlistNames.findIndex(checkPlaylistName)]

    /*
    let sendData = { "selected_playlist_id": selectedPlaylistID }

    fetch("http://localhost:8080/api/receive_selected_playlist", {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(sendData)
    })
    .then((response) => response.json())
    .then((data) => {
      setPostResponse(data.message)
    });

    if(res == 'success'){
      location.assign('http://localhost:3000/pages/recs')
    }

    //console.log('Sent POST request with selected playlist id: ' + JSON.stringify(sendData))
    */

    location.assign('http://localhost:3000/pages/recs' + '?plid=' + selectedPlaylistID)
  }


  return(
    <div className="outerWrapper select-none">
      <div className="formWrapper">
        <div className="center">
          <div className="inner">

            <Card>
              <CardHeader className="pb-3">
                <CardTitle>Select Playlist</CardTitle>
                <CardDescription>
                  Choose source playlist for recommendations
                </CardDescription>
              </CardHeader>
              <CardContent className="grid gap-1">    
                <RadioGroup onValueChange={onChange} className="grid grid-rows gap-4">
                  {playlistDetails.map((values) => (
                      <div>
                        <RadioGroupItem value={values[0]} id={values[0]} className="peer sr-only" />
                        <Label htmlFor={values[0]}
                          className="-mx-2 flex items-start space-x-4 space-y-4 rounded-md 
                          p-3 transition-all hover:bg-accent hover:text-accent-foreground
                          peer-data-[state=checked]:border-primary 
                          [&:has([data-state=checked])]:border-primary 
                          border-2 border-muted ">
                          <img className="mt-px h-12 w-12" src={values[1]} alt=""/>
                          <div className="space-y-1">
                            <p className="text-sm font-heavy leading-none">{values[0]}</p>
                          </div>
                        </Label>
                      </div>
                    ))}
                </RadioGroup>
              </CardContent>
            </Card>
            <Button onClick={onSubmit} className='border-zinc-500 text-zinc-300
            hover:border-zinc-200 hover:text-zinc-100 text-center
            transition-colors border px-8 my-3 w-full '>
              Submit
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default main