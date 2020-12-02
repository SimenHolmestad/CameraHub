import React, { useState, useEffect } from 'react';
import { get_album_info, capture_image_to_album } from './../server'


function AlbumPage(props) {
  const albumName = props.match.params.albumName;
  const [imageUrls, setImageUrls] = useState(null);

  // Update the album image urls every second
  useEffect(() => {
    get_album_info(albumName).then((data) => setImageUrls(data.image_urls));
    const interval = setInterval(() => {
      get_album_info(albumName).then((data) => setImageUrls(data.image_urls));
    }, 5000);
    return () => clearInterval(interval);
  }, [albumName]);

  let albumImageList = null
  if (imageUrls) {
    console.log(imageUrls);
    albumImageList = imageUrls.map(url => {
      return <img src={url} alt="no description provided" key={url}/>
    })
  }

  const handleClick = async (e) => {
    e.preventDefault();
    const response = await capture_image_to_album(albumName)
    setImageUrls([response.image_url, ...imageUrls])
  }

  return (
    <div>
      <h1>{props.match.params.albumName}</h1>
      <button onClick={e => handleClick(e)}>Capture new image</button>
      <hr/>
      { albumImageList }
    </div>
  );
}

export default AlbumPage
