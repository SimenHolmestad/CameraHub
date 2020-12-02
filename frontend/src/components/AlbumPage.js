import React, { useState, useEffect } from 'react';
import { get_album_info } from './../server'

const useAlbumInfo = (albumName) => {
  const [albumInfo, setAlbumInfo] = useState(null);
  useEffect(() => {
    get_album_info(albumName).then((data) => setAlbumInfo(data));
  }, [albumName]);
  return albumInfo;
};

function AlbumPage(props) {
  const albumInfo = useAlbumInfo(props.match.params.albumName);
  let albumList = null
  if (albumInfo) {
    albumList = albumInfo.image_urls.map(url => {
      return <img src={url} alt="no description provided" key={url}/>
    })
  }

  return (
    <div>
      <h1>{props.match.params.albumName}</h1>
      { albumList }
    </div>
  );
}

export default AlbumPage
