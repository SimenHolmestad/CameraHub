import React from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import AlbumEmptyMessage from './AlbumEmptyMessage';
import Slideshow from './Slideshow';
import { get_album_info } from './../server'


function SlideshowPage(props) {
  const [imageUrls, setImageUrls] = React.useState(null);
  const albumName = props.match.params.albumName;

  // Update the album data from server every 3 minutes
  React.useEffect(() => {
    get_album_info(albumName).then((data) => {
      setImageUrls(data.image_urls);
    });
    const interval = setInterval(() => {
      get_album_info(albumName).then((data) => {
        setImageUrls(data.image_urls);
      });
    }, 180000);
    return () => clearInterval(interval);
  }, [albumName]);

  if (imageUrls === null) {
    return <CircularProgress/>
  }

  if (imageUrls.length === 0) {
    return <AlbumEmptyMessage/>
  }

  return (
    <Slideshow imageUrls={imageUrls}/>
  );
}

export default SlideshowPage
